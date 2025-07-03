from langgraph.checkpoint.memory import MemorySaver

def get_memory():
    return MemorySaver() # in memory storage, para persistance usar SQL or similar https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/#2-compile-the-graph