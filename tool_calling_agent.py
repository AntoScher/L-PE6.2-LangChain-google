from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from utils.tools import setup_tools
from utils.deepseek import DeepSeekClient

def run_tool_calling_agent():
    tools = setup_tools()
    model = DeepSeekClient()  # Используем кастомный клиент

    # Промпт для обработки запросов
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Use tools when needed."),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    # Создаем цепочку
    agent = create_tool_calling_agent(model, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # Пример запроса с историей чата
    response = executor.invoke({
        "input": "Будет ли завтра дождь в Москве?",
        "chat_history": [
            HumanMessage(content="Привет!"),
            AIMessage(content="Здравствуйте! Чем могу помочь?")
        ]
    })
    print("Ответ:", response["output"])

if __name__ == "__main__":
    run_tool_calling_agent()
