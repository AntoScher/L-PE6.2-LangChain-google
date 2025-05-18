from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from utils.tools import setup_tools
from utils.deepseek import DeepSeekClient


def run_react_agent():
    tools = setup_tools()
    model = DeepSeekClient()  # Кастомный клиент

    # ReAct промпт
    react_prompt = hub.pull("hwchase17/react")

    # Создаем агента
    agent = create_react_agent(model, tools, react_prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # Пример запроса
    response = executor.invoke({
        "input": "Назови 3 самых популярных музея в Париже",
        "chat_history": []  # Поддержка истории
    })
    print("Ответ:", response["output"])


if __name__ == "__main__":
    run_react_agent()