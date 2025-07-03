from dotenv import load_dotenv
import sys
import json

load_dotenv()

from graph import build_keyword_graph

def main():
    """Run the keyword research system"""
    
    # Build the graph
    graph = build_keyword_graph()
    
    print("🤖 B2B SaaS Keyword Research Agent")
    print("=" * 50)
    print("Enter a business idea to get keywords and questions for SEO content strategy.")
    print("Type 'quit' to exit.\n")
    
    while True:
        # Get business idea from user
        business_idea = input("💡 Business Idea: ")
        if business_idea.lower() in ["quit", "exit", "q"]:
            print("Goodbye! 👋")
            break
        if not business_idea.strip():
            print("Please enter a business idea.")
            continue
        print("\n🔍 Analyzing your business idea...")
        # Run the graph with the business idea
        inputs = {
            "messages": [{"role": "user", "content": business_idea}],
            "business_idea": "",
            "keywords": [],
            "questions": []
        }
        # Stream tokens for real-time feedback
        print("\n📊 Streaming Results:")
        print("=" * 50)
        final_state = None
        for chunk in graph.stream(inputs):
            # Print streaming tokens for user feedback
            if hasattr(chunk, 'get') and isinstance(chunk, dict):
                # This is a state update, store the final state
                final_state = chunk
            elif isinstance(chunk, str):
                print(chunk, end='', flush=True)
        print("\n" + "=" * 50)
        # After streaming ends, print final results cleanly
        # The data is nested inside final_state['keyword_agent']
        agent_state = final_state.get('keyword_agent', {}) if final_state else {}
        
        if agent_state and "keywords" in agent_state and "questions" in agent_state:
            print("\n🎯 KEYWORDS:")
            for i, keyword in enumerate(agent_state["keywords"], 1):
                print(f"  {i}. {keyword}")
            print("\n❓ QUESTIONS:")
            for i, question in enumerate(agent_state["questions"], 1):
                print(f"  {i}. {question}")
        else:
            print("\n⚠️ Could not extract keywords/questions from result.")
            print(f"Agent state: {agent_state}")
        
        # Save output to json file
        if agent_state:
            # Extract only the data we want to save (avoid LangChain message objects)
            output_data = {
                "business_idea": agent_state.get("business_idea", business_idea),
                "keywords": agent_state.get("keywords", []),
                "questions": agent_state.get("questions", [])
            }
            with open(f"outputs/{'_'.join(business_idea.split())}.json", "w") as f:
                json.dump(output_data, f, indent=2)

if __name__ == "__main__":
    main()
