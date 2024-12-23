import anthropic
import os
from dotenv import load_dotenv
load_dotenv()

class llmCall:
    def __init__(self, model):
        self.model = model
    def get_completion(self, content, model):
        if model in ("claude-3-5-sonnet-20241022", "claude-3-haiku-20240307"):
            self._get_sonnet(model, content)
        elif model in ("claude-3-5-sonnet-20241022", "claude-3-haiku-20240307"):
            self._get_sonnet(model, content)


    def _get_sonnet(self, model, content):
        client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        response = client.messages.create(
            model=model,
            max_tokens=1024,
            messages=[
                {"role": "user", "content": content}
            ]
        )
        return response





"""
"gemini-2.0-flash-thinking-exp"
"""