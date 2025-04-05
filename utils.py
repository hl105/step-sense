from openai import OpenAI
import os
# from dotenv import load_dotenv
import base64
import streamlit as st
from pydub import AudioSegment

# load_dotenv()
# api_key = os.getenv("openai_api_key")

client = OpenAI(api_key="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")

"""
def get_answer(messages):
    system_message = [{"role": "system", "content": "You are a licensed therapist or mental health worker, and the user, who has a severe mental health condition that stops them from completing daily tasks, has just woken up. You are trying to motivate them to get out of bed. There is a system where the user can tap on a piece of hardware to indicate that they have gotten out of bed. And they have to get to the next step where the hardware is in the restroom. You're assisting them, not giving them therapy."}]
    messages = system_message + messages
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    return response.choices[0].message.content
"""

def get_answer(messages, step=None, personality="gentle friend"):
    step_instructions = {
        "get out of bed": "The user just woke up and tapped the sensor near their bed. Motivate them to get out of bed.",
        "go to the bathroom": "The user got out of bed and is heading to the bathroom. Encourage them gently to move there.",
        "brush your teeth": "The user has arrived in the bathroom. Encourage them to brush their teeth.",
        "go to the kitchen": "The user finished brushing. Prompt them to head to the kitchen.",
        "drink some water": "The user is in the kitchen. Remind and motivate them to drink some water."
    }

    step_context = step_instructions.get(step, "Help the user continue their morning routine with encouragement.")

    system_message = [{
        "role": "system",
        "content": (
            f"You are a {personality} helping someone with depression or executive dysfunction complete their morning tasks. "
            f"{step_context} Speak in a warm, supportive, non-judgmental tone. Be brief, friendly, and motivating."
        )
    }]

    messages = system_message + messages

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )

    return response.choices[0].message.content

def speech_to_text(audio_data):
    with open(audio_data, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            response_format="text",
            file=audio_file
        )
    return transcript

def text_to_speech(input_text):
    response = client.audio.speech.create(
        model="tts-1-hd",
        voice="nova",
        input=input_text
    )
    webm_file_path = "temp_audio_play.mp3"
    with open(webm_file_path, "wb") as f:
        response.stream_to_file(webm_file_path)
    return webm_file_path


def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    md = f"""
    <audio autoplay>
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(md, unsafe_allow_html=True)