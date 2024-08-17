from openai import OpenAI
class OpenAIClient:
    def __init__(self, api_key, model="gpt-3.5-turbo-0125"):
        self.api_key = api_key
        print(self.api_key)
        self.client = OpenAI(
            api_key=self.api_key
        )
        self.model = model

    def get_emotion(self, prompt):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content