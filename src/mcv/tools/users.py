from fastmcp.server.dependencies import get_access_token
import httpx

from utils.toon import toonParse

from mcv.helper import mcv

async def get_me() -> dict:
    """
    Get the current user's basic identity from access token.

    Returns user claims including ID, English/Thai names, and auth provider.
    """
    token = get_access_token()
    return {
        "user": token.claims,
    }


async def get_user_info() -> dict:
    """
    Get the authenticated user's detailed profile information.

    Returns student details (ID, Thai/English names, degree) and account info (UID, profile picture URL).
    """

    token = get_access_token()
    access_token = token.token

    headers = {"Authorization": f"Bearer {access_token}"}
    url = mcv("/public/get/user/info")

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        user_info = resp.json()
        return toonParse(user_info.json)


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
