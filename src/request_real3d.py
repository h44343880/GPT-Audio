import requests
import os
from dotenv import load_dotenv

load_dotenv()
def request_real3d(audio_file_path, emotion, user_id, access_token): 
    url = "http://140.123.97.203:8001/real3d/"
    data = {
        "drv_aud": audio_file_path,
        "emotion": emotion,
        "user_id": user_id,
    }
    requests.post(url, json=data, headers={"Authorization": f"Bearer {access_token}"}).json()