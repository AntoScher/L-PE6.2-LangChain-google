from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities import OpenWeatherMapAPIWrapper
from langchain.tools import Tool
from utils.config import TAVILY_API_KEY, OPENWEATHERMAP_API_KEY


def setup_tools():
    # Используем tavily_api_key вместо api_key
    tavily_tool = TavilySearchResults(
        tavily_api_key=TAVILY_API_KEY,  # Ключевое исправление!
        max_results=7
    )

    # Инструмент погоды
    weather = OpenWeatherMapAPIWrapper(
        openweathermap_api_key=OPENWEATHERMAP_API_KEY
    )
    weather_tool = Tool(
        name="Weather",
        func=weather.run,
        description="Get current weather information"
    )

    return [tavily_tool, weather_tool]