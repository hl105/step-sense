# import streamlit as st 
# import os
# from utils import get_answer, text_to_speech, autoplay_audio, speech_to_text
# from audio_recorder_streamlit import audio_recorder 
# from streamlit_float import * 

# # Float feature initialization
# float_init() 

# # Define the routine steps
# routine_steps = ["Get out of bed", "Go to the bathroom", "Brush your teeth", "Drink water"]

# # Session state setup
# def initialize_session_state():
#     if "messages" not in st.session_state:
#         st.session_state.messages = [
#             {"role": "assistant", "content": "Good morning Anna. How did you sleep last night?"}
#         ]
#     if "current_step_idx" not in st.session_state:
#         st.session_state.current_step_idx = 0

# initialize_session_state()

# st.title("StepSense")

# # Show the current step
# if st.session_state.current_step_idx < len(routine_steps):
#     current_step = routine_steps[st.session_state.current_step_idx]
#     st.subheader(f"✨ Next step: **{current_step}**")
#     st.info("Tap the button or use your voice when you're ready to move on!")
# else:
#     st.success("You completed all your steps today! 🎉")
#     st.stop()

# # Audio input
# footer_container = st.container()
# with footer_container:
#     audio_bytes = audio_recorder(
#         pause_threshold=3.0,
#         text="Click to respond",
#         recording_color="#E34234",
#         neutral_color="#6aa36f",
#         icon_name="microphone",
#         icon_size="10x"
#     )

# # Show previous messages
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.write(message["content"])

# # Handle speech input
# if audio_bytes:
#     with st.spinner("Transcribing..."):
#         webm_file_path = "temp_audio.mp3"
#         with open(webm_file_path, "wb") as f:
#             f.write(audio_bytes)
#         transcript = speech_to_text(webm_file_path)
#         if transcript:
#             st.session_state.messages.append({"role": "user", "content": transcript})
#             with st.chat_message("user"):
#                 st.write(transcript)
#         os.remove(webm_file_path)

# # If last message was from user, respond
# if st.session_state.messages[-1]["role"] != "assistant":
#     with st.chat_message("assistant"):
#         with st.spinner("Thinking 🤔..."):
#             final_response = get_answer(st.session_state.messages)
#         with st.spinner("Generating audio response..."):    
#             audio_file = text_to_speech(final_response)
#             autoplay_audio(audio_file)
#         st.write(final_response)
#         st.session_state.messages.append({"role": "assistant", "content": final_response})
#         os.remove(audio_file)

# # Step completion button
# if st.button("✅ I did this step!"):
#     if st.session_state.current_step_idx < len(routine_steps) - 1:
#         st.session_state.current_step_idx += 1
#         st.rerun()
#     else:
#         st.session_state.current_step_idx += 1
#         st.rerun()

# # Float the footer container and provide CSS to target it with
# footer_container.float("bottom: 0rem;")
