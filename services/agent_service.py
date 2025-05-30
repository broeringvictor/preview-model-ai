
import os
from openai import OpenAI

class AgentService:
    def get_agent_response(self, messages, api_key, model='gpt-3.5-turbo', temperature=0, stream=False):
        """
        This method is designed to be easily replaceable.
        For an OpenAI agent, it calls the OpenAI API.
        For a custom agent, you would replace the logic here.
        """
        
        client = OpenAI(api_key=api_key)
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                stream=stream
            )
            if stream:
                for chunk in response:
                    if chunk.choices:
                        content = chunk.choices[0].delta.content
                        if content:
                            yield content
            else:
                yield response.choices[0].message.content
        except Exception as e:
            yield f"Error: {e}"