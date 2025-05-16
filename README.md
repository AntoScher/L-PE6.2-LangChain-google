# L-PE6.2-LangChain-google

## Описание
Проект демонстрирует интеграцию LangChain с Vertex AI API и FastAPI для создания REST-сервисов.

В данном проекте используются следующие основные компоненты:
- **FastAPI** — для создания REST API.
- **Vertex AI API** — для генерации текста, реализованной в модуле `gemini_client.py`. 
- **LangChain** — для организации цепочек (chains) и агентов. 

## Требования
- Python 3.9+
- Установленный Google Cloud SDK
- API-ключи для Tavily и OpenWeatherMap

Эндпоинты
/translate — Перевод текста
/agent — Агент с инструментами (поиск, погода)

## Установка
```bash
pip install -r requirements.txt

##запуск проекта
uvicorn app:app --reload