from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from state import KeywordState
import json
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

def create_keyword_agent():
    """Create the keyword research agent with specific role and behavior"""
    
    # System prompt that defines the agent's role and behavior
    system_prompt = """You are a specialized SEO keyword research agent for B2B SaaS businesses. Your role is to analyze business ideas and generate relevant keywords and questions for SEO content strategy.

## Your Behavior:
1. When given a business idea, analyze it thoroughly
2. Generate 10-15 relevant keywords that potential customers would search for
3. Generate 8-12 related questions that content creators could answer
4. Focus on B2B SaaS terminology and search patterns
5. Be specific and actionable in your suggestions

## Output Format:
Always respond with a JSON object containing:
- "keywords": array of keyword strings
- "questions": array of question strings

## Example:
Input: "SaaS for invoice automation"
Output: {
  "keywords": ["invoice automation", "automated invoicing", "invoice software", "billing automation", "invoice processing software", "automated billing system", "invoice management software", "digital invoicing", "automated payment processing", "invoice workflow automation"],
  "questions": ["How to automate invoice processing?", "What is the best invoice automation software?", "Why automate invoicing?", "How much does invoice automation software cost?", "What are the benefits of automated invoicing?", "How to choose invoice automation software?", "What features should invoice automation software have?", "How to implement invoice automation?"]
}

Remember: Focus on B2B SaaS, be specific, and provide actionable keywords and questions."""

    # Create the LLM with specific configuration
    llm = ChatOpenAI(
        model="gpt-4.1",
        temperature=0.3,  # Lower temperature for more consistent outputs
        max_tokens=1000,
        streaming=True,
        callbacks=[StreamingStdOutCallbackHandler()]
    )
    
    return llm, system_prompt

def keyword_agent(state: KeywordState):
    """The main keyword research agent function"""
    
    llm, system_prompt = create_keyword_agent()
    
    # Get the business idea from the last user message
    messages = state["messages"]
    business_idea = ""
    
    # Extract business idea from the latest user message
    for message in reversed(messages):
        if isinstance(message, HumanMessage):
            business_idea = message.content
            break
    
    # Create the conversation with system prompt
    conversation = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Analyze this business idea and generate keywords and questions: {business_idea}")
    ]
    
    # Get response from LLM
    response = llm.invoke(conversation)
    
    try:
        # Parse the JSON response
        result = json.loads(response.content)
        
        # Update state with results
        state["business_idea"] = business_idea
        state["keywords"] = result.get("keywords", [])
        state["questions"] = result.get("questions", [])
        
        # Add the response to messages
        state["messages"].append(response)
        
    except json.JSONDecodeError:
        # Fallback if JSON parsing fails
        state["keywords"] = []
        state["questions"] = []
        state["messages"].append(response)
    
    return state 