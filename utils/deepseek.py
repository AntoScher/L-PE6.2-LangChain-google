from langchain_core.language_models import BaseLanguageModel
from langchain_core.callbacks import CallbackManagerForLLMRun, AsyncCallbackManagerForLLMRun
from langchain_core.outputs import ChatResult, ChatGeneration, LLMResult
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptValue
from typing import Optional, List, Dict, Any, Union
import requests
from utils.config import DEEPSEEK_API_KEY


class DeepSeekChat(BaseLanguageModel):
    """Полная реализация модели DeepSeek для LangChain"""

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        # Преобразуем сообщения LangChain в формат DeepSeek
        formatted_messages = [
            {"role": "user" if isinstance(msg, HumanMessage) else "assistant", "content": msg.content}
            for msg in messages
        ]
        response = self._call_api(formatted_messages)
        return ChatResult(generations=[ChatGeneration(message=AIMessage(content=response))])

    def _call_api(self, messages: List[Dict]) -> str:
        """Вызов API DeepSeek"""
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "deepseek-chat",
            "messages": messages,
            "temperature": 0.7
        }
        response = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=payload)
        return response.json()["choices"][0]["message"]["content"]

    # Реализация недостающих методов
    def generate_prompt(
        self,
        prompts: List[ChatPromptValue],
        stop: Optional[List[str]] = None,
        callbacks: CallbackManagerForLLMRun = None,
        **kwargs: Any,
    ) -> LLMResult:
        generations = []
        for prompt in prompts:
            result = self._generate(prompt.messages, stop, callbacks)
            generations.append([gen.text for gen in result.generations])
        return LLMResult(generations=generations)

    def invoke(self, input: Union[str, ChatPromptValue], **kwargs) -> Union[str, BaseMessage]:
        if isinstance(input, str):
            return self.predict(input, **kwargs)
        return self.predict_messages(input.messages, **kwargs)

    def predict(self, text: str, **kwargs: Any) -> str:
        return self._generate([HumanMessage(content=text)]).generations[0].message.content

    def predict_messages(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> BaseMessage:
        return self._generate(messages, stop).generations[0].message

    @property
    def _llm_type(self) -> str:
        return "deepseek-chat"

    # Заглушки для асинхронных методов
    async def _agenerate(self, *args, **kwargs):
        raise NotImplementedError("Async не поддерживается")

    async def agenerate_prompt(self, *args, **kwargs):
        raise NotImplementedError("Async не поддерживается")

    async def apredict(self, *args, **kwargs):
        raise NotImplementedError("Async не поддерживается")

    async def apredict_messages(self, *args, **kwargs):
        raise NotImplementedError("Async не поддерживается")