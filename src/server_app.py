from dotenv import load_dotenv
import os
from src.gpt_sovits_client import GPTSoVITSClient
from src.openai_client import OpenAIClient
import json
from datetime import datetime
import re
import pika

def read_file(file_path):
    with open(file_path, 'r', encoding='UTF-8') as f:
        return f.read()
    
# there may be a better way to do this
def append_article_to_prompt(prompt, article, emotions_list):
    placeholder_emotions_text = "replace_with_emotion_list" # maybe put this in env?
    new_prompt = prompt+article # append article to prompt
    replace_index = new_prompt.find(placeholder_emotions_text)
    new_prompt = new_prompt[:replace_index]+','.join(emotions_list)+new_prompt[replace_index+len(placeholder_emotions_text)-1:]
    return new_prompt

def export_to_json(export_path, response): # TODO: need to change the "response" variable name?
    json_string = json.dumps({"content": response}, ensure_ascii=False, indent=4)
    print(json_string)
    with open(export_path, 'w+', encoding='UTF-8') as f:
        f.write(json_string)
        
def get_sentence_emotion_array(response, emotions_list):
    lines = response.split('\n')
    sentence_emotion_array = []
    for line in lines:
        if '@' in line:
            sentence, emotion = line.split(' @')
            sentence = sentence.replace("\'", "") # remove ' from sentence
            sentence_emotion_array.append({
                'sentence': sentence,
                'emotion': next(filter(lambda emo: emo in emotion, emotions_list), "default") # match emotion from emotions_list
                # 'emotion': "default"
            })
    return sentence_emotion_array

def get_audio_path(file_path, character_name, sentence):
    date = datetime.today().strftime('%m-%d-%H-%M-%S-%f')    
    sanitized_sentence = re.sub(r'[^a-zA-Z0-9_]', '', sentence)[:10]

    filename = f"{character_name}_{sanitized_sentence}_{date}.mp3"
    audio_file_path = f"{file_path}/{filename}"

    return audio_file_path

def publish_audio_to_queue(audio_file_path, emotion, user_id, queue_name, channel, access_token, sentence):
    data = {
        "sentence": sentence,
        "emotion": emotion,
        "user_id": user_id,
        "access_token": access_token,
        "audio_file_path": audio_file_path
    }
    channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(data))
    print(f" [x] Sent audio {data} to {queue_name}")

def publish_video_to_queue(audio_file_path, emotion, user_id, queue_name, channel, access_token):
    data = {
        "drv_aud": audio_file_path,
        "emotion": emotion,
        "user_id": user_id,
        "access_token": access_token
    }
    channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(data))
    print(f" [x] Sent video {data} to {queue_name}")

def get_audio_for_each_sentence(sentence_emotion_list, CHARACTER_NAME, AUDIO_PATH, user_id, access_token, channel, audio_queue_name, video_queue_name):
    for sentence_emotion in sentence_emotion_list:
        print(f"Processing sentence: {sentence_emotion['sentence']} with emotion: {sentence_emotion['emotion']}")
        
        # save audio to audio directory
        audio_file_path = get_audio_path( AUDIO_PATH, CHARACTER_NAME, sentence_emotion['sentence'])
        # save audio file path to sentence_emotion
        sentence_emotion['audio_file_path'] = audio_file_path
                
        publish_audio_to_queue(sentence_emotion['audio_file_path'], sentence_emotion['emotion'], user_id, audio_queue_name, channel, access_token, sentence_emotion['sentence'])
        publish_video_to_queue(audio_file_path, sentence_emotion['emotion'], user_id, video_queue_name, channel, access_token)

def get_broker_connection(rabbitmq_url, audio_queue_name, video_queue_name):
    connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
    channel = connection.channel()

    channel.queue_declare(queue=audio_queue_name, durable=True)
    channel.queue_declare(queue=video_queue_name, durable=True)
    return connection, channel

def main(user_question, user_id, access_token):
    load_dotenv(dotenv_path=".env", override=True)
    LOG_PATH = os.getenv("LOG_DIR")
    absolute_path = os.getcwd() # TODO
    # logging.basicConfig(filename="test.log", level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', stream='stdout')
    
    # load env vars
    PROMPT_PATH = os.getenv("PROMPT_PATH")
    ARTICLE_PATH = os.getenv("ARTICLE_PATH")
    TEXT_PATH = os.getenv("TEXT_PATH")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GPT_SOVITS_ENDPOINT = os.getenv("GPT_SOVITS_ENDPOINT")
    CHARACTER_NAME = os.getenv("CHARACTER_NAME")
    AUDIO_PATH = os.getenv("AUDIO_DIR").format(user_id)
    OUTPUT_PATH = os.getenv("OUTPUT_DIR")
    RABBITMQ_URL = os.getenv("RABBITMQ_URL")
    AUDIO_QUEUE = os.getenv("AUDIO_QUEUE")
    VIDEO_QUEUE = os.getenv("VIDEO_QUEUE")
    print(f"Loaded env vars, {LOG_PATH}, {PROMPT_PATH}, {ARTICLE_PATH}, {TEXT_PATH}, {OPENAI_API_KEY}, {GPT_SOVITS_ENDPOINT}, {CHARACTER_NAME}, {AUDIO_PATH}, {OUTPUT_PATH}, {RABBITMQ_URL}, {AUDIO_QUEUE}, {VIDEO_QUEUE}")
    
    broker_connection, channel = get_broker_connection(RABBITMQ_URL, AUDIO_QUEUE, VIDEO_QUEUE)

    # pre-processing prompt
    prompt = read_file(PROMPT_PATH)
    # user_question = read_file(TEXT_PATH)
    
    # get emotions list
    gpt_sovits_client = GPTSoVITSClient(GPT_SOVITS_ENDPOINT)
    character_list = gpt_sovits_client.get_character_list()
    emotions_list = character_list[CHARACTER_NAME]
    # emotions_list = ["開心", "難過"]

    # generate article
    openai_client = OpenAIClient(api_key=OPENAI_API_KEY)
    article = openai_client.generate_article(user_question)
    # with open(ARTICLE_PATH, 'w', encoding='UTF-8') as f:
    #     f.write(response)
    # article = read_file(ARTICLE_PATH)
    
    # finalize prompt
    finalized_prompt = append_article_to_prompt(prompt=prompt, emotions_list=emotions_list, article=article)
    
    print("Finalized prompt: ", finalized_prompt)
    
    # get emotions for each sentence
    openai_client = OpenAIClient(api_key=OPENAI_API_KEY)
    try:
        response = openai_client.get_emotion(prompt=finalized_prompt)
    except ValueError as e:
        # TODO: add to log
        pass
    
    # gpt_sovits_client.close()
    
    # return response
    
    # parse response
    sentence_emotion_list = get_sentence_emotion_array(response, emotions_list)
    
    # get audio for each sentence
    get_audio_for_each_sentence(sentence_emotion_list, CHARACTER_NAME, AUDIO_PATH, user_id, access_token, channel, AUDIO_QUEUE, VIDEO_QUEUE) # TODO: maybe there's a better way?
    
    gpt_sovits_client.close()
    broker_connection.close()
    
    return sentence_emotion_list
        
    # export to json
    # export_to_json(f'{OUTPUT_PATH}/output.json', sentence_emotion_list)

    # close gpt sovits connection    
    gpt_sovits_client.close()
    
if __name__ == '__main__':
    main()