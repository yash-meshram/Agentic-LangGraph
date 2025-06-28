from mcp.server.fastmcp import FastMCP

# Initilizing the MCP server
mcp = FastMCP("Math")
# Math = server name

# creating tool present inside mcp server
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add the numbers"""
    return a+b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply the numbers"""
    return a*b

# stdio = std + i + o = standard input output
# The transport = "stdio" tells the server to:
# Use standard input/output (stdin and stdout) to receive and response to tool function calls.
if __name__ == '__main__':
    mcp.run(transport = "stdio")
    
    
# if client is ineracting with this server then in we are using transport = "stdio", then
# we will run this file directly in command prompt and get input and output there itself

# clinet ---> give input in cmd ---> our server run in cmd itself ---> output given in cmd ---> clinet can easily read output from cmd
# help when running locally