from fastapi import APIRouter
from fastapi.responses import FileResponse
from server.dto import GPTAudioRequest
from fastapi.responses import StreamingResponse
from typing import List

from dotenv import load_dotenv
import os
import json
from src.app import main
router = APIRouter()

def file_generator(file_paths: List[str]):
    for file_path in file_paths:
        with open(file_path, "rb") as file:
            yield file.read()

@router.post("/GPTAudio/")
async def generate_audio(req: GPTAudioRequest) -> StreamingResponse:
    text_path = os.getenv('TEXT_PATH')
    with open(f"{text_path}", "w") as f:
        f.write(req.question)
    load_dotenv(dotenv_path=".env", override=True)
    main()

    # load audio file paths from output.json
    output_json_folder = os.getenv('OUTPUT_DIR')
    with open(f"{output_json_folder}/output.json", 'r') as f:
        dict = json.load(f)
    print(dict)
    audio_paths = list()
    for item in dict["content"]:
        audio_paths.append(item["audio_file_path"])

    return StreamingResponse(content=file_generator(audio_paths), media_type="audio/mpeg")
