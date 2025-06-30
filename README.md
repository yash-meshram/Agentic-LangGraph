# Agentic-LangGraph

A comprehensive project demonstrating advanced AI agent development using LangGraph, LangChain, and Model Context Protocol (MCP). This project showcases various agent architectures, from basic chatbots to complex multi-server systems with human-in-the-loop capabilities.

## 🚀 Project Overview

This project explores the cutting-edge capabilities of LangGraph for building sophisticated AI agents with features like:
- **Multi-Server MCP Integration**: Connect to multiple Model Context Protocol servers
- **Tool Integration**: Seamless integration with external tools and APIs
- **Memory Management**: Persistent conversation memory across sessions
- **Human-in-the-Loop**: Interactive human intervention capabilities
- **Graph-based Workflows**: Complex agent workflows using LangGraph's state management

## 📁 Project Structure

```
Agentic-LangGraph/
├── MCP_Demo_LangChain/          # Model Context Protocol demonstrations
│   ├── client.py                # Multi-server MCP client
│   ├── math_server.py           # Math operations MCP server
│   └── weather_server.py        # Weather API MCP server
├── ChatBot_Agent/               # Advanced chatbot implementations
│   ├── basicChatbot.ipynb       # Comprehensive Jupyter tutorial
│   ├── basic_chatbot.py         # Simple chatbot with LangGraph
│   ├── chatbot_with_tools.py    # Chatbot with tool integration
│   ├── memory_in_graph.py       # Chatbot with memory persistence
│   └── human_in_loop.py         # Human-in-the-loop chatbot
├── requirements.txt             # Python dependencies
├── notes.txt                    # Project notes and concepts
└── README.md                    # This file
```

## 🛠️ Features

### 1. Model Context Protocol (MCP) Integration
- **Multi-Server Client**: Connect to multiple MCP servers simultaneously
- **Transport Protocols**: Support for stdio and HTTP transport methods
- **Tool Abstraction**: Unified interface for different server capabilities

### 2. Advanced Chatbot Architectures
- **Basic Chatbot**: Simple conversation flow with LangGraph
- **Tool-Enhanced Chatbot**: Integration with search and custom tools
- **Memory-Persistent Chatbot**: Conversation memory across sessions
- **Human-in-the-Loop**: Interactive human intervention capabilities

### 3. LangGraph Workflows
- **State Management**: Typed state with message reducers
- **Graph Visualization**: Visual representation of agent workflows
- **Conditional Edges**: Dynamic routing based on tool requirements
- **Streaming Support**: Real-time response streaming

## 📋 Prerequisites

- Python 3.8+
- Groq API key (for LLM access)
- Tavily API key (for search functionality)
- Environment variables setup

## 🚀 Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Agentic-LangGraph
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file with your API keys:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   ```

## 🎯 Usage Examples

### 1. Basic Chatbot

```python
from ChatBot_Agent.basic_chatbot import graph

# Simple conversation
response = graph.invoke({'messages': 'Hi, how are you?'})
print(response['messages'][-1].content)
```

### 2. Multi-Server MCP Client

```python
# Run the MCP demo
cd MCP_Demo_LangChain
python client.py
```

This will:
- Start math and weather servers
- Create a multi-server client
- Demonstrate tool usage across different servers

### 3. Chatbot with Tools

```python
from ChatBot_Agent.chatbot_with_tools import graph

# Search for information
response = graph.invoke({'messages': 'What is the latest AI news?'})

# Perform calculations
response = graph.invoke({'messages': 'What is 89 multiplied by 67?'})
```

### 4. Memory-Persistent Chatbot

```python
from ChatBot_Agent.memory_in_graph import graph

# Create a conversation thread
config = {'configurable': {'thread_id': '1'}}

# First message
response = graph.invoke({'messages': 'My name is Yash'}, config=config)

# Follow-up (remembers previous context)
response = graph.invoke({'messages': 'What is my name?'}, config=config)
```

### 5. Human-in-the-Loop Chatbot

```python
from ChatBot_Agent.human_in_loop import graph

# Start conversation with human intervention
events = graph.stream({
    'messages': 'I need expert guidance for building an AI agent.'
}, config=config, stream_mode='values')

# Human provides input
human_response = "Look into langgraph documentation"
human_command = Command(resume={'data': human_response})

# Continue after human intervention
events = graph.stream(human_command, config=config, stream_mode='values')
```

## 🔧 MCP Server Development

### Creating a Math Server

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add the numbers"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply the numbers"""
    return a * b

if __name__ == '__main__':
    mcp.run(transport="stdio")
```

### Creating a Weather Server

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")

@mcp.tool()
async def get_weather(location: str) -> str:
    """Get the weather for the given location"""
    return "28 deg. Celsius"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
```

## 📚 Key Concepts

### LangGraph Components
- **State**: Typed dictionary that persists across nodes
- **Nodes**: Functions that process state and return updates
- **Edges**: Connections between nodes defining workflow
- **Reducers**: Functions that determine how state is updated

### MCP Protocol
- **Transport Methods**: stdio (local) and HTTP (remote)
- **Tool Registration**: Automatic tool discovery and registration
- **Multi-Server Support**: Connect to multiple servers simultaneously

### Memory Management
- **Thread-based**: Separate conversation threads
- **Persistent**: Memory persists across sessions
- **Configurable**: Customizable memory storage backends

## 🎨 Advanced Features

### Graph Visualization
```python
# Visualize the graph structure
from IPython.display import Image, display

display(Image(graph.get_graph().draw_mermaid_png()))
```

### Streaming Responses
```python
# Stream responses in real-time
for event in graph.stream({'messages': 'Hello'}, stream_mode='values'):
    if 'messages' in event:
        print(event['messages'][-1].content)
```

### Conditional Tool Usage
```python
# Tools are automatically selected based on user input
response = graph.invoke({
    'messages': 'Search for AI news and calculate 5 * 10'
})
```

## 🔍 Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure all required API keys are set in `.env`
2. **Import Errors**: Verify all dependencies are installed
3. **MCP Server Connection**: Check server URLs and transport methods
4. **Memory Issues**: Ensure thread IDs are consistent across sessions

### Debug Mode
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)
```
