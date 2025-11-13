from fastmcp import FastMCP
from fastmcp.server.dependencies import get_access_token

async def get_me() -> dict:
    """Get the user's information."""
    token = get_access_token()
    print(token)
    return {
        "user": token.claims,
    }
