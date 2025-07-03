from langgraph.types import Command

from dotenv import load_dotenv
import sys

load_dotenv()

from graph import build_graph

graph = build_graph()

thread_id = sys.argv[1] if len(sys.argv) > 1 else "1"
config = {"configurable": {"thread_id": thread_id}}

while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    # Start the conversation
    events = graph.stream(
        {"messages": [{"role": "user", "content": user_input}]},
        config,
        stream_mode="values",
    )
    # Process the initial response
    for event in events:
        if "messages" in event:
            event["messages"][-1].pretty_print()
    # Check if we need human input for a tool
    while True:
        snapshot = graph.get_state(config)
        if snapshot.next and snapshot.next[0] == 'tools':
            # Tool is waiting for human input
            human_response = input("Human: ")
            if human_response.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                sys.exit(0)
            # Resume the tool execution with human response
            human_command = Command(resume={"data": human_response})
            events = graph.stream(human_command, config, stream_mode="values")
            # Process the response after human input
            for event in events:
                if "messages" in event:
                    event["messages"][-1].pretty_print()
        else:
            # No more tools waiting, break out of the inner loop
            break
