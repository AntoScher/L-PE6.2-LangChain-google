import os
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities import OpenWeatherMapAPIWrapper
from langchain.tools import Tool
from langchain_google_vertexai import VertexAI
from langchain import hub
from dotenv import load_dotenv

# Загрузка переменных из .env
load_dotenv(dotenv_path=".env")

# Проверка наличия API-ключей
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

if not TAVILY_API_KEY or not OPENWEATHERMAP_API_KEY:
    raise ValueError("API-ключи не найдены в .env файле")

# Настройка инструментов
weather = OpenWeatherMapAPIWrapper()
weather_tool = Tool(name="Weather", func=weather.run, description="Получение информации о погоде")
tavily_tool = TavilySearchResults(max_results=7)

# Используем поддерживаемую модель и регион
try:
    # Модель Gemini 1.5 Flash в поддерживаемом регионе
    model = VertexAI(model_name="gemini-1.5-flash-001", location="europe-west4")
except Exception as e:
    print(f"Ошибка инициализации модели: {e}")
    print("Попробуйте использовать модель с Hugging Face")
    # Резервная модель
    from langchain_community.llms import HuggingFacePipeline
    model = HuggingFacePipeline.from_model_id(model_id="google/flan-t5-xl", task="text2text-generation")

# Загрузка шаблона ReAct
prompt = hub.pull("hwchase17/react")

# Создание агента
tools = [tavily_tool, weather_tool]
agent = create_react_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Пример использования
response = agent_executor.invoke({"input": "Какая погода в Москве?"})
print(response["output"])