from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

# defining State
class State(TypedDict):
    messages: Annotated[list, add_messages]
    

# defining llm
llm = init_chat_model("groq:llama3-8b-8192")


# Node
def chatbot(state: State):
    return {
        "messages": [llm.invoke(state['messages'])]
    }


# building Graph
graph_builder = StateGraph(State)

# adding Node
graph_builder.add_node(node = "ChatBot", action = chatbot)

# adding Edge
graph_builder.add_edge(start_key = START, end_key = "ChatBot")
graph_builder.add_edge(start_key = "ChatBot", end_key = END)

# compile teh graph
graph = graph_builder.compile()


# running the Graph
response = graph.invoke({'messages': 'Hi, what is your full model name?'})
print(response['messages'])
print(response['messages'][-1].content)

# running using stream
for event in graph.stream({'messages': 'Hi, how are you, what is your model name?'}):
    print(event)