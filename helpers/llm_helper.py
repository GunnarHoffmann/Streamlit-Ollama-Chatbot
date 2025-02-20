"""
Orignal Author: DevTechBytes
https://www.youtube.com/@DevTechBytes
"""

import ollama
import os
from config import Config

system_prompt = Config.SYSTEM_PROMPT

# Specify the API endpoint
os.environ['OLLAMA_HOST'] = 'http://172.205.182.197:11434'


from ollama import Client
client = Client(
  host='http://172.205.182.197:11434',
  headers={'x-some-header': 'some-value'}
)

def chat(user_prompt, model):
    stream = client.chat(
        model=model,
        messages=[{'role': 'assistant', 'content': system_prompt},
                  {'role': 'user', 'content': f"Model being used is {model}.{user_prompt}"}],
        stream=True,
    )

    return stream

# handles stream response back from LLM
def stream_parser(stream):
    for chunk in stream:
        yield chunk['message']['content']
