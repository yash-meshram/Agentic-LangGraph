# Chatbot with tools

from langchain_tavily import TavilySearch
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.prebuilt import ToolNode, tools_condition

load_dotenv()

# defining tavily search tool
tavily_search = TavilySearch(max_results = 2)

# defining custom function
def multiply(a: int, b: int) -> int:
    """Multiply a and b

    Args:
        a (int): first int
        b (int): second int

    Returns:
        int: output int
    """
    return a*b

# defining tools
tools = [tavily_search, multiply]

# defining state
class State(TypedDict):
    messages: Annotated[list, add_messages]
    
# defining llm
llm = init_chat_model('groq:llama3-8b-8192')

# Node
def tool_calling_llm(state: State):
    return {
        'messages': [llm.invoke(state['messages'])]
    }
    
# building graph
builder = StateGraph(State)

# adding Node
builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_node("tools", ToolNode(tools))

# adding edges
builder.add_edge(START, "tool_calling_llm")
builder.add_conditional_edges(
    "tool_calling_llm",
    tools_condition
)
builder.add_edge("tools", END)

# compile graph
graph = builder.compile()

# running the graph
response = graph.invoke({'messages': 'What is the latest AI news regarding agentic AI'})
for m in response['messages']:
    m.pretty_print()
    
response = graph.invoke({'messages': 'WHat is 89 multiply by 67'})
for m in response['messages']:
    m.pretty_print()
    
response = graph.invoke({'messages': 'What is thh latest AI news regarding AGI and what is 8 multiply by 7'})
for m in response['messages']:
    m.pretty_print()