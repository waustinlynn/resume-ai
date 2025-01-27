from abc import ABC, abstractmethod
from typing import List

import openai

from app.domain.models.chat_completion import ChatCompletionMessage
from app.infrastructure.settings import Settings

settings = Settings()

openai.api_key = settings.openai_api_key


class AbstractChatCompletion(ABC):
    @abstractmethod
    def complete(self, chat_completion_messages: List[ChatCompletionMessage]) -> str:
        pass


class ChatCompletionService(AbstractChatCompletion):
    def complete(self, chat_completion_messages: List[ChatCompletionMessage]) -> str:
        try:
            # Call the OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[vars(msg) for msg in chat_completion_messages],
                temperature=0.7,  # Adjust creativity
            )

            # Extract the response text
            return response["choices"][0]["message"]["content"]

        except Exception as e:
            return f"An error occurred: {e}"
