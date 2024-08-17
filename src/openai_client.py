from openai import OpenAI
import re
class OpenAIClient:
    def __init__(self, api_key, model="gpt-3.5-turbo-0125"):
        self.api_key = api_key
        print(self.api_key)
        self.client = OpenAI(
            api_key=self.api_key
        )
        self.model = model

    def get_emotion(self, prompt, max_retries=100):
        retries = 0
        while retries < max_retries:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            if self.is_response_format_correct():
                return response.choices[0].message.content
            retries += 1
        raise ValueError("Failed to get a valid response after multiple retries.")
                    
    def is_response_format_correct(response):
        lines = response.split('\n')
        for line in lines:
            match = re.match(r".+ @.+", line)
            if(match == None):
                return False
        return True
        
            
        