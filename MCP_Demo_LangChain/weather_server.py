from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")

@mcp.tool()
# code that will call teh 3rd part weather api
async def get_weather(location: str) -> str:
    """Get the weather for the given location in degree celcius"""
    return "28 deg. Celcius"

if __name__ == "__main__":
    mcp.run(transport = "streamable-http")
    
    
# Here we used transport = "streamable-http"
