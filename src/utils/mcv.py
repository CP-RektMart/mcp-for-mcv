from config import MCV_BASE_URL
from fastmcp.server.dependencies import get_access_token
from utils.toon import toonParse

import httpx


def mcv(path: str) -> str:
    """Build MCV API URL from path."""
    return MCV_BASE_URL + path


async def mcv_get(path: str) -> dict:
    """
    Make an authenticated GET request to MCV API.

    Handles token retrieval, authorization headers, and response parsing.
    """
    token = get_access_token()
    access_token = token.token

    headers = {"Authorization": f"Bearer {access_token}"}
    url = mcv(path)

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        return toonParse(resp.json())
