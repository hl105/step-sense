from openai import OpenAI
import os
# from dotenv import load_dotenv
import base64
import streamlit as st
from pydub import AudioSegment

# load_dotenv()
# api_key = os.getenv("openai_api_key")

client = OpenAI(api_key="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")


def get_answer(messages):
    system_message = [{"role": "system", "content": "You are mental health social worker. "}]
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
        voice="onyx",
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