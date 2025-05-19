import os
import requests
from utils.config import TAVILY_API_KEY, OPENWEATHERMAP_API_KEY
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")
# Получаем API ключи из переменных окружения
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

def check_tavily_api_key():
    if not TAVILY_API_KEY:
        print("TAVILY_API_KEY не установлен.")
        return False
    try:
        # Пример запроса к Tavily API
        url = "https://api.tavily.com/v1/search"
        params = {
            "q": "test query",
            "apiKey": TAVILY_API_KEY,
            "limit": 1
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get("results"):
            print("TAVILY_API_KEY действителен.")
            return True
        else:
            print("TAVILY_API_KEY недействителен или не возвращает результатов.")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при проверке TAVILY_API_KEY: {e}")
        return False

def check_openweathermap_api_key():
    if not OPENWEATHERMAP_API_KEY:
        print("OPENWEATHERMAP_API_KEY не установлен.")
        return False
    try:
        # Пример запроса к OpenWeatherMap API
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": "London",
            "appid": OPENWEATHERMAP_API_KEY,
            "units": "metric"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get("name"):
            print("OPENWEATHERMAP_API_KEY действителен.")
            return True
        else:
            print("OPENWEATHERMAP_API_KEY недействителен или не возвращает результатов.")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при проверке OPENWEATHERMAP_API_KEY: {e}")
        return False

if __name__ == "__main__":
    check_tavily_api_key()
    check_openweathermap_api_key()