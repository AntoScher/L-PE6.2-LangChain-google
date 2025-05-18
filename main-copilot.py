import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env (если он есть)
load_dotenv()

# Пример строки в .env:
# GOOGLE_APPLICATION_CREDENTIALS=/абсолютный/путь/до/your-service-account-key.json

################################################################################
# Инициализация Vertex AI
################################################################################
import vertexai
from vertexai.preview.language_models import TextGenerationModel

# Инициализируем Vertex AI.
# Замените "your-project-id" на ваш идентификатор проекта,
# а также укажите регион, в котором доступна нужная модель (например, europe-west4).
vertexai.init(project="zc-dodiddone-431113", location="europe-west4")

def generate_response(prompt: str) -> str:
    """
    Функция для генерации ответа с использованием модели Vertex AI.
    Здесь используется модель 'text-bison@001' как пример (уточните актуальное имя модели).
    """
    model = TextGenerationModel.from_pretrained("text-bison@001")
    parameters = {"temperature": 0.7, "max_output_tokens": 256}
    response = model.predict(prompt, **parameters)
    return response.text

################################################################################
# Создаем класс-обертку для LLM, совместимый с LangChain, на базе Vertex AI
################################################################################
from langchain.llms.base import LLM

class VertexAILLM(LLM):
    @property
    def _llm_type(self) -> str:
        return "vertex_ai"

    def _call(self, prompt: str, stop=None, **kwargs) -> str:
        # Принимаем дополнительные аргументы, такие как 'functions', чтобы избежать ошибки.
        return generate_response(prompt)

################################################################################
# Импорт библиотек и настройка инструментов для агента (аналог вашего Function calling.txt)
################################################################################
from langchain.agents import AgentExecutor, create_openai_functions_agent, create_react_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities import OpenWeatherMapAPIWrapper
from langchain.tools import Tool
from langchain.prompts import ChatPromptTemplate

# Устанавливаем API-ключи для Tavily и OpenWeatherMap.
# Их также можно задать в файле .env, например:
# TAVILY_API_KEY=your_tavily_api_key
# OPENWEATHERMAP_API_KEY=your_openweathermap_api_key
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY", "your_tavily_api_key")
os.environ["OPENWEATHERMAP_API_KEY"] = os.getenv("OPENWEATHERMAP_API_KEY", "your_openweathermap_api_key")

# Шаблон диалога для агента
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant"),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

# Создаем инструмент для получения информации о погоде через OpenWeatherMap API
weather = OpenWeatherMapAPIWrapper()
weather_tool = Tool(
    name="Weather",
    func=weather.run,  # Функция для получения прогноза погоды
    description="Useful for getting weather information"
)

# Создаем инструмент для поиска через Tavily API
tools = [TavilySearchResults(max_results=7), weather_tool]

# Используем нашу обертку LLM на базе Vertex AI
llm = VertexAILLM()

# Создаем агента для function calling (аналог вашего примера)
agent = create_openai_functions_agent(llm, tools, prompt_template)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

################################################################################
# Демонстрация работы агентов
################################################################################
def function_calling_demo():
    print("Пример 1: Запрос прогноза погоды")
    response = agent_executor.invoke({"input": "будет ли в Москве дождь?"})
    print("Ответ агента:", response)

    print("\nПример 2: Запрос о месте для путешествия")
    response = agent_executor.invoke({"input": "Какие интересные места для отдыха в Италии?"})
    print("Ответ агента:", response)

    print("\nПример 3: Философский вопрос")
    response = agent_executor.invoke({"input": "Есть ли в жизни счастье?"})
    print("Ответ агента:", response)

def react_agent_demo():
    # Демонстрация ReAct агента с использованием шаблона из LangChain Hub.
    from langchain import hub
    react_prompt = hub.pull("hwchase17/react")
    react_agent = create_react_agent(llm, tools, react_prompt)
    react_executor = AgentExecutor(agent=react_agent, tools=tools, verbose=True)
    print("\nReAct Agent Демонстрация: Запрос прогноза погоды")
    response = react_executor.invoke({"input": "будет ли в Москве дождь?"})
    print("Ответ ReAct агента:", response)

if __name__ == "__main__":
    function_calling_demo()
    react_agent_demo()