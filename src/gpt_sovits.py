import requests
from dotenv import load_dotenv
import os
from urllib import parse
from datetime import datetime

def get_character_list():
    character_list_endpoint = os.getenv('GPT_SOVITS_ENDPOINT')+"character_list"
    response = requests.get(character_list_endpoint).json()
    return response

def get_audio(sentence, emotion=None):
    load_dotenv()
    character_list_endpoint = os.getenv('GPT_SOVITS_ENDPOINT')+"character_list"
    response = requests.get(character_list_endpoint).json()
    
    character_name = 'daniel' # TODO: need to change to get variable
    emotion_data = {
        "character": f"${character_name}",
        "emotion": "default" if emotion==None else f"${emotion}",
        "text": f"${sentence}",
        "text_language": "zh",
        "format": "mp3"
    }
    audio = requests.post(f"{os.getenv('GPT_SOVITS_ENDPOINT')}tts", json=emotion_data).content
    date = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    audio_file_path = f"../audio/{character_name}_{sentence}_{date}.mp3" # TODO: get audio file path from env
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(audio_file_path), exist_ok=True)

    # Open the file in binary write mode and write audio data
    with open(audio_file_path, 'wb') as audio_file:
        audio_file.write(audio)
    return audio_file_path