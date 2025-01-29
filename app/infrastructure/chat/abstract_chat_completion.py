import json
from abc import ABC, abstractmethod
from typing import List

from openai import OpenAI

from app.domain.models.chat_completion import ChatCompletionMessage
from app.domain.models.chat_response import ChatResponse


class AbstractChatCompletion(ABC):
    @abstractmethod
    def complete(self, chat_completion_messages: List[ChatCompletionMessage]) -> str:
        pass


class ChatCompletionService(AbstractChatCompletion):
    def __init__(self, openai_client: OpenAI):
        self.openai_client = openai_client

    def complete(
        self, chat_completion_messages: List[ChatCompletionMessage]
    ) -> ChatResponse:
        # Call the OpenAI API
        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[vars(msg) for msg in chat_completion_messages],
            temperature=1,
        )

        content = response.choices[0].message.content

        # Extract the response text
        return ChatResponse(**json.loads(content))
