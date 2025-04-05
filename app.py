import streamlit as st 
import os
from utils import get_answer, text_to_speech, autoplay_audio, speech_to_text
from audio_recorder_streamlit import audio_recorder 
from streamlit_float import * 

# Float feature initialization
float_init() 

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Good morning Anna. How did you sleep last night?"}
        ]
    # if "audio_initialized" not in st.session_state:
    #     st.session_state.audio_initialized = False

initialize_session_state()


st.title("StepSense")


# Create footer container for the microphone
footer_container = st.container()
with footer_container:
    audio_bytes = audio_recorder(pause_threshold=3.0,
                                text="Click to respond",
                                recording_color="#E34234",
                                neutral_color="#6aa36f",
                                icon_name="microphone",
                                icon_size="10x")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if audio_bytes:
    # Write the audio bytes to a file
    with st.spinner("Transcribing..."):
        webm_file_path = "temp_audio.mp3"
        with open(webm_file_path, "wb") as f:
            f.write(audio_bytes)

        transcript = speech_to_text(webm_file_path)
        if transcript:
            st.session_state.messages.append({"role": "user", "content": transcript})
            with st.chat_message("user"):
                st.write(transcript)
            os.remove(webm_file_path)


if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("..."):
            final_response = get_answer(st.session_state.messages)
        with st.spinner("Generating audio response..."):    
            audio_file = text_to_speech(final_response)
            autoplay_audio(audio_file)
        st.write(final_response)
        st.session_state.messages.append({"role": "assistant", "content": final_response})
        os.remove(audio_file)

# Float the footer container and provide CSS to target it with
footer_container.float("bottom: 0rem;")

routine_steps = [
    "get out of bed",
    "brush your teeth",
    "take medication"
]
current_step = routine_steps[st.session_state.current_step_idx]
st.subheader(f"Current Task: {current_step}")

if st.button("I did it!"):
    # Generate AI response
    response = get_answer(st.session_state.messages, step=current_step)
    st.session_state.messages.append({"role": "user", "content": f"I finished: {current_step}"})
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Play voice
    audio_path = text_to_speech(response)
    autoplay_audio(audio_path)

    # Move to the next step
    if st.session_state.current_step_idx < len(routine_steps) - 1:
        st.session_state.current_step_idx += 1
    else:
        st.success("You've completed your whole routine! 🎉")

if st.session_state.messages:
    st.markdown("### Encouragement")
    st.markdown(st.session_state.messages[-1]["content"])
