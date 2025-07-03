from langchain.chat_models import init_chat_model
from state import State

llm = init_chat_model("openai:gpt-4.1")

def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}