# client shoudl be able to interact with both the servers
# math_server and weather_server

# for creating clinet which will interact wth multi servers
from langchain_mcp_adapters.client import MultiServerMCPClient

# for creating agents
from langgraph.prebuilt import create_react_agent

# for llm
from langchain_groq import ChatGroq

import asyncio
from dotenv import load_dotenv

load_dotenv()

async def main():
    # creating client. Multi server mcp client
    client = MultiServerMCPClient(
        {
            'math': {
                'command': 'python',
                'args': ['math_server.py'],  # give correct absolute path
                'transport': 'stdio'
            },
            'weather': {
                'url': 'http://localhost:8000/mcp',  # Ensure server is running. weather is running in this url
                'transport': 'streamable_http'
            }
        }
    )
    
    # defining tools
    tools = await client.get_tools()
    
    # llm we will use
    llm = ChatGroq(model = 'qwen-qwq-32b')
    
    # creating agent
    agent = create_react_agent(
        model = llm,
        tools = tools
    )
    
    # running the agent
    math_response = await agent.ainvoke(
        {'messages': [{'role': 'user', 'content': "what is (3 + 9) x 10?"}]}
    )
    print(f"Math response: {math_response['messages'][-1].content}")
    
    weather_response = await agent.ainvoke(
        {'messages': [{'role': 'user', 'content': "what is the temperature in Delhi?"}]}
    )
    print(f"Weather response: {weather_response['messages'][-1].content}")
    

asyncio.run(main())