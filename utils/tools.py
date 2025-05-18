from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities import OpenWeatherMapAPIWrapper
from langchain.tools import Tool
from .config import TAVILY_API_KEY, OPENWEATHERMAP_API_KEY  # Импорт из config.py


def setup_tools():
    # Инструмент Tavily
    tavily_tool = TavilySearchResults(
        tavily_api_key=TAVILY_API_KEY,  # Ключ берется из config.py
        max_results=7
    )

    # Инструмент OpenWeatherMap
    weather = OpenWeatherMapAPIWrapper(
        openweathermap_api_key=OPENWEATHERMAP_API_KEY  # Ключ из config.py
    )
    weather_tool = Tool(
        name="Weather",
        func=weather.run,
        description="Useful for getting weather information"
    )

    return [tavily_tool, weather_tool]