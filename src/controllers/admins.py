from fastmcp import FastMCP
from fastmcp.server.dependencies import get_access_token
from utils.mcv import mcv

import httpx


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
