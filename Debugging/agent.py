from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages
from langchain_tavily import TavilySearch
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import BaseMessage
from langchain_core.tools import tool

import os
from dotenv import load_dotenv
load_dotenv("../.env")

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGSMITH_TRACING"] = os.getenv("LANGSMITH_TRACING")
os.environ["LANGSMITH_PROJECT"] = os.getenv("LANGSMITH_PROJECT")


def make_tool_graph():
    # LLM
    llm = init_chat_model("groq:llama3-8b-8192")

    # Tools
    @tool
    def add(a: int, b: int) -> int:
        """Add two numbers"""
        return a + b

    @tool
    def multiply(a: int, b: int) -> int:
        """Multiply two numbers"""
        return a * b

    tavily_search = TavilySearch(max_result = 2)

    tools = [add, multiply, tavily_search]

    # Bind LLM with Tools
    llm_with_tools = llm.bind_tools(tools)

    # Defining State class
    class State(TypedDict):
        messages: Annotated[list[BaseMessage], add_messages]

    # Node definition

    # chatbot (contains llm) node
    def chatBot(state: State):
        return {
            'messages': [llm_with_tools.invoke(state['messages'])]
        }
        
    # tools node
    tools_node = ToolNode(tools)

    # building graph
    builder = StateGraph(State)

    # adding node
    builder.add_node("chatBot", chatBot)
    builder.add_node("tools", tools_node)

    # adding edge
    builder.add_edge(START, "chatBot")
    builder.add_conditional_edges("chatBot", tools_condition)
    builder.add_edge("tools", "chatBot")

    # compile
    graph = builder.compile()
    
    return graph


tool_agent = make_tool_graph()

