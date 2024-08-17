```bash
conda create -n GPTAudio python=3.10
conda activate GPTAudio
```

GPT_SoVITs example response:

```json
{
  "三月七": ["default", "calm", "advertisement_upbeat"],
  "daniel": ["default", "calm", "depressed", "cheerful", "angry"]
}
```

ChatGPT example response:
```b
ChatCompletion(id='chatcmpl-9wPy6ZIzWWkCHnW3CKYs8fgQJgDHV', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='今天天氣真好：開心\n但是我被車撞了：難過', role='assistant', function_call=None, tool_calls=None, refusal=None))], created=1723709874, model='gpt-3.5-turbo-0125', object='chat.completion', service_tier=None, system_fingerprint=None, usage=CompletionUsage(completion_tokens=27, prompt_tokens=97, total_tokens=124))
```
