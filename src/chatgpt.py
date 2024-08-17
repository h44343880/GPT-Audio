from openai import OpenAI
import json
import os
from dotenv import load_dotenv


def read_prompt_file(file_path):
    pass


def sentence_to_audio():
    pass


def get_emotion():
    pass


def export_to_json(file_path, response): # TODO: need to change the "response" variable name?
    json_string = json.dumps(response, ensure_ascii=False, indent=4)
    print(json_string)
    with open(file_path, 'w+') as f:
        f.write(json_string)


def main():
    load_dotenv()
    client = OpenAI(
        api_key=os.getenv('OPENAI_API_KEY')
    )
    file_path = "prompt.txt"  # input file path
    with open(file_path, 'r') as f:
        prompt = f.read()
    emotion_set = set(['開心', '難過']) # TODO: grab emotions from gpt sovits api
    article = {}

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user",
                "content": f"請將下列文章內容逐句選擇對應的情緒，可選擇的情緒有: {','.join(list(emotion_set))}，並且以下格式回傳結果: '句子 @對應情緒'。文章: 「我從不主動跟其他失業的朋友聊（失業相關的話題），我發現每個人都像易碎玻璃一樣，非常脆弱。」去年夏天，32歲的方成文（化名）離開工作3年的一家杭州的知名互聯網公司後，至今仍在找工作。 「她在我心目中永遠是最厲害的！」看到女兒拿下奧運拳擊金牌，林郁婷的母親廖秀宸難掩激動。"}
        ]
    )
    # print(response)

    message = response.choices[0].message.content
    # print(message)

    # s = message.split('\n')
    # print(s)

    sentence_emotion_array = []  # need to rename

    lines = message.split('\n')

    for line in lines:
        if '@' in line:
            sentence, emotion = line.split(' @')
            sentence_emotion_array.append({
                'sentence': sentence,
                "emotion": emotion.strip()
            })
            os.system("")  # TODO:  add python path_to_file

    json_output = {
        "content": sentence_emotion_array
    }
    
    export_to_json(file_path, json_output)


if __name__ == "__main__":
    main()
