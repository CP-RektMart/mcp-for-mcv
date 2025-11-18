from fastmcp import FastMCP
from fastmcp.server.dependencies import get_access_token
import httpx


async def list_all_courses():
    token = get_access_token()
    access_token = token.token

    headers = {"Authorization": f"Bearer {access_token}"}
    url = "https://www.mycourseville.com/api/v1/public/get/user/courses?detail=1"

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        courses = resp.json()
        return courses


async def get_course_infos(courseId: str):
    token = get_access_token()
    access_token = token.token

    headers = {"Authorization": f"Bearer {access_token}"}
    url = (
        f"https://www.mycourseville.com/api/v1/public/get/course/info?cv_cid={courseId}"
    )

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        courses = resp.json()
        return courses


async def get_course_materials(courseId: str):
    token = get_access_token()
    access_token = token.token

    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"https://www.mycourseville.com/api/v1/public/get/course/materials?cv_cid={courseId}&detail=1&published=1"

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        courses = resp.json()
        return courses


async def get_course_assignments(courseId: str):
    token = get_access_token()
    access_token = token.token

    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"https://www.mycourseville.com/api/v1/public/get/course/assignments?cv_cid={courseId}&detail=1&published=1"

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        courses = resp.json()
        return courses


async def get_course_announcements(courseId: str):
    token = get_access_token()
    access_token = token.token

    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"https://www.mycourseville.com/api/v1/public/get/course/announcements?cv_cid={courseId}&detail=1&published=1"

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        courses = resp.json()
        return courses


async def get_assignment(itemID: str):
    token = get_access_token()
    access_token = token.token

    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"https://www.mycourseville.com/api/v1/public/get/item/assignment?item_id={itemID}"

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        courses = resp.json()
        return courses


async def get_playlist(courseId: str):
    token = get_access_token()
    access_token = token.token

    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"https://www.mycourseville.com/api/v1/public/get/course/playlists?cv_cid={courseId}"

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        playlist = resp.json()
        return {
            "suggestion": "Add the youtube link for the ready-to-use, from the youtube playlist field",
            "data": playlist,
        }


async def get_online_meetings(courseId: str):
    token = get_access_token()
    access_token = token.token

    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"https://www.mycourseville.com/api/v1/public/get/course/onlinemeetings?cv_cid={courseId}"

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        meetings = resp.json()
        return meetings