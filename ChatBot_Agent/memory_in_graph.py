# Chatbot with tools

from langchain_tavily import TavilySearch
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()

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
graph = builder.compile(checkpointer = memory)

# creating a thread
config = {'configurable': {'thread_id': '1'}}

# running the graph
response = graph.invoke({'messages': 'My name is Yash'}, config = config)
for m in response['messages']:
    m.pretty_print()
    
response = graph.invoke({'messages': 'what is my name'}, config = config)
for m in response['messages']:
    m.pretty_print()
    
response = graph.invoke({'messages': 'what does my name mean in different languages especially in marathi'}, config = config)
for m in response['messages']:
    m.pretty_print()