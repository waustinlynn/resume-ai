from abc import ABC, abstractmethod
from typing import List

from app.domain.models.chat_completion import ChatCompletionMessage


class AbstractChatCompletion(ABC):
    @abstractmethod
    def complete(self, chat_completion_messages: List[ChatCompletionMessage]) -> str:
        pass


class ChatCompletionService(AbstractChatCompletion):
    def complete(self, chat_completion_messages: List[ChatCompletionMessage]) -> str:
        pass
