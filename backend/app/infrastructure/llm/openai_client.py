from typing import List, Optional, Dict
from openai import OpenAI


class OpenAIClient:
    """Wrapper for OpenAI API"""

    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        if not api_key:
            raise ValueError("OpenAI API key is required")
        
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def chat(
        self,
        system_prompt: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """
        Send chat request to OpenAI.
        
        Args:
            system_prompt: System role message
            messages: List of messages with 'role' and 'content'
            temperature: Sampling temperature (0-1)
            max_tokens: Max tokens in response
        
        Returns:
            Response text from assistant
        """
        
        # Build messages with system prompt
        all_messages = [
            {"role": "system", "content": system_prompt}
        ] + messages
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=all_messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return response.choices[0].message.content
