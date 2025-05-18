from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.prompts import ChatPromptTemplate
from utils.tools import setup_tools
from utils.deepseek import DeepSeekChat


def run_tool_calling_agent():
    tools = setup_tools()
    model = DeepSeekChat()  # Теперь совместим с LangChain

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant"),
        ("user", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    agent = create_tool_calling_agent(model, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    response = executor.invoke({"input": "Будет ли дождь в Москве завтра?"})
    print("Ответ:", response["output"])


if __name__ == "__main__":
    run_tool_calling_agent()