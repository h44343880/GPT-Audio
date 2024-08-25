from fastapi import APIRouter
from fastapi.responses import FileResponse
from server.dto import GPTAudioRequest

import src.app 
router = APIRouter()

@router.post("/GPTAudio/")
async def create_live_portrait(req: GPTAudioRequest) -> FileResponse:
    src.app.main()    
    audio_path = "/mnt/Nami/users/Jason0411202/ml/GPT-Audio/audio/daniel_豬八戒：我也希望能吃到好東西 多謝師父提供的保護_08-24-20-01-23.mp3"
    
    response = FileResponse(audio_path)

    return response
