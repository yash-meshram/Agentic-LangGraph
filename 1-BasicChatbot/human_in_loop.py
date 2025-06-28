from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from langchain_tavily import TavilySearch
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

from langgraph.types import Command, interrupt              # interrupt = interript teh work flow
from langchain_core.tools import tool

load_dotenv()

# defining state
class State(TypedDict):
    messages: Annotated[list, add_messages]

# defining llm
llm = init_chat_model('groq:llama3-8b-8192')

# search tool
travily_search = TavilySearch(max_results = 2)

# human assistant
@tool
def human_assistant(query: str) -> str:
    """Request assistant from a human"""
    human_response = interrupt({'query': query})
    return human_response['data']

# defining custom function
def multiply(a: int, b:int) -> int:
    """Multiply a and b

    Args:
        a (int): first int
        b (int): second int

    Returns:
        int: output int
    """
    return a*b

# defining tools
tools = [travily_search, human_assistant]

# binding llm with tools
llm_with_tools = llm.bind_tools(tools)

# Node
def chatbot(state: State):
    return {
        'messages': [llm_with_tools.invoke(state['messages'])]
    }

# memory
memory = MemorySaver()

# building graph
builder = StateGraph(State)

# adding nodes
builder.add_node("chatbot", chatbot)
tool_node = ToolNode(tools = tools)
builder.add_node('tools', tool_node)

# adding edges
builder.add_edge(START, 'chatbot')
builder.add_conditional_edges('chatbot', tools_condition)
builder.add_edge('tools', 'chatbot')

# graph
graph = builder.compile(checkpointer = memory)

# creating a threas
config = {'configurable': {'thread_id': '1'}}

# running the graph
events = graph.stream({'messages': 'I need some expert guidance and assistance for building an AI agent. Can you please request assistant for me?'}, config = config, stream_mode = 'values')
for event in events:
    if 'messages' in event:
        event['messages'][-1].pretty_print()

# human intervention
human_response = (
    "Look into langgraph documentation",
    "Check n8n also - its pretty cool"
)
human_command = Command(resume = {'data': human_response})

# run after human intervention
events = graph.stream(human_command, config = config, stream_mode = 'values')
for event in events:
    if 'messages' in event:
        event['messages'][-1].pretty_print()