from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from utils.tools import setup_tools
from utils.deepseek import DeepSeekClient


def run_react_agent():
    tools = setup_tools()
    model = DeepSeekClient()

    prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(model, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    response = executor.invoke({"input": "Назови 3 популярных музея в Париже"})
    print("Ответ:", response["output"])


if __name__ == "__main__":
    run_react_agent()