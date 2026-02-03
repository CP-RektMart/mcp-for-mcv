from config import MCV_BASE_URL
from fastmcp.server.dependencies import get_access_token
from utils.toon import toonParse

import httpx


def mcv(path: str) -> str:
    """Build MCV API URL from path."""
    return MCV_BASE_URL + path


def get_auth_headers() -> dict:
    """Get authorization headers with Bearer token from current access token."""
    token = get_access_token()
    return {"Authorization": f"Bearer {token.token}"}


async def mcv_get(path: str, suggestion: str = None) -> dict:
    """
    Make an authenticated GET request to MCV API.

    Handles token retrieval, authorization headers, and response parsing.
    If suggestion is provided, returns {"suggestion": ..., "data": ...}.
    """
    headers = get_auth_headers()
    url = mcv(path)

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        data = toonParse(resp.json())

        if suggestion is not None:
            return {"data": data, "suggestion": suggestion}

        return data
