from fastmcp.server.dependencies import get_access_token
import httpx

from utils.toon import toonParse

from mcv.helper import mcv

async def get_student_roster(courseId: str):
    token = get_access_token()
    access_token = token.token

    headers = {"Authorization": f"Bearer {access_token}"}
    url = mcv("/public/get/course/roster?cv_cid={courseId}")

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        roster = resp.json()
        return toonParse(roster)
