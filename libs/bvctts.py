import streamlit as st
import dashscope
from dashscope.audio.tts import SpeechSynthesizer

def tts(text, model):

    dashscope.api_key= st.secrets['dashscope_api_key']

    speech = SpeechSynthesizer.call(model=model,
                                        text=text,
                                        sample_rate=48000)
    return speech.get_audio_data()

