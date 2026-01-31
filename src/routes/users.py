from fastmcp import FastMCP
from controllers.users import get_me, get_user_gradeletter, get_user_info


def register(mcp: FastMCP):
    mcp.tool()(get_me)
    mcp.tool()(get_user_info)
    mcp.tool()(get_user_gradeletter)
