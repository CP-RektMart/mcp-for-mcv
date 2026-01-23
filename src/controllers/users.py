from fastmcp import FastMCP
from fastmcp.server.dependencies import get_access_token
import httpx

async def get_me() -> dict:
    """Get the user's information."""
    token = get_access_token()
    return {
        "user": token.claims,
    }

async def get_user_gradeletter(courseId: str):
    token = get_access_token()
    access_token = token.token

    headers = {"Authorization": f"Bearer {access_token}"}
    url = mcv(f"/public/get/user/gradeletter?cv_cid={courseId}")

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        gradeletter = resp.json()
        return toonParse(gradeletter)
