from fastmcp import FastMCP
from controllers.users import get_me

def register(mcp: FastMCP): 
    mcp.tool(name="get me")(get_me)
