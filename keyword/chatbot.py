from langchain.chat_models import init_chat_model
from state import KeywordState
from tools import get_tools

def chatbot(state: KeywordState):
    llm = init_chat_model("openai:gpt-4.1")
    tools = get_tools()
    llm_with_tools = llm.bind_tools(tools)
    message = llm_with_tools.invoke(state["messages"])
    assert len(message.tool_calls) <= 1
    return {"messages": [message]}    