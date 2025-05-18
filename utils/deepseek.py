import requests
from typing import List, Dict, Optional
from .config import DEEPSEEK_API_KEY


class DeepSeekClient:
    def __init__(self):
        self.api_key = DEEPSEEK_API_KEY
        # Актуальный URL из документации DeepSeek (пример)
        self.base_url = "https://api.deepseek.com/v1/chat/completions"

    def generate(
            self,
            messages: List[Dict],
            model: str = "deepseek-chat",
            temperature: float = 0.7,
            max_tokens: Optional[int] = 300,  # Добавлен параметр длины ответа
            stream: bool = False,  # Потоковый режим
            **kwargs  # Доп. параметры
    ) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream,
            **kwargs  # Остальные параметры из документации
        }

        try:
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()  # Проверка на HTTP-ошибки
            return response.json()["choices"][0]["message"]["content"]

        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP Error: {e.response.status_code} - {e.response.text}"
            raise Exception(error_msg)
        except KeyError:
            raise Exception("Invalid API response format")