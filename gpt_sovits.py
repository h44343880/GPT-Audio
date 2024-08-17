import requests
from dotenv import load_dotenv
import os
from urllib import parse


# TODO: export this function to chatgpt.py
def get_audio(sentence, emotion=None):
    load_dotenv()
    character_list_endpoint = os.getenv('GPT_SOVITS_ENDPOINT')+"character_list"
    response = requests.get(character_list_endpoint).json()
    character_name = response['daniel'] # TODO: need to change to get variable
    sentence = parse.quote(sentence) # format chinese characters to url format
    audio = requests.get(f"{os.getenv('GPT_SOVITS_ENDPOINT')}tts?text={sentence}&character={character_name}").content
    emotion_data = {
        "character": f"${character_name}",
        "emotion": "default" if emotion==None else f"${emotion}",
        "text": f"${sentence}",
    }
    audio = requests.post(f"{os.getenv('GPT_SOVITS_ENDPOINT')}tts", json=emotion_data).content
    audio_file_path = "./audio" # TODO: get audio file path from env
    with open(audio_file_path, 'wb') as audio_file:
        audio_file.write(audio)
    
get_audio("你好嗎？") # testing purposes