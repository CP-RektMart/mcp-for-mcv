from fastmcp.server.dependencies import get_access_token
import httpx

from utils.toon import toonParse

from mcv.helper import mcv

async def list_all_courses():
    """List all courses for the authenticated user."""

    token = get_access_token()
    access_token = token.token

    headers = {"Authorization": f"Bearer {access_token}"}
    url = mcv("/public/get/user/courses")

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json()


async def get_course_infos(courseId: str):
    """Get detailed information for a specific course."""
    token = get_access_token()
    access_token = token.token

    headers = {"Authorization": f"Bearer {access_token}"}
    url = mcv(f"/public/get/course/info?cv_cid={courseId}")

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        return toonParse(resp.json())


async def get_course_materials(courseId: str):
    """Retrieve published learning materials for a course."""
    token = get_access_token()
    access_token = token.token

    headers = {"Authorization": f"Bearer {access_token}"}
    url = mcv(f"/public/get/course/materials?cv_cid={courseId}&detail=1&published=1")

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        return toonParse(resp.json())


async def get_course_assignments(courseId: str):
    """Retrieve published assignments for a course."""
    token = get_access_token()
    access_token = token.token

    headers = {"Authorization": f"Bearer {access_token}"}
    url = mcv(f"/public/get/course/assignments?cv_cid={courseId}&detail=1&published=1")

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        return toonParse(resp.json())


async def get_course_announcements(courseId: str):
    """Retrieve published announcements for a course."""
    token = get_access_token()
    access_token = token.token

    headers = {"Authorization": f"Bearer {access_token}"}
    url = mcv(
        f"/public/get/course/announcements?cv_cid={courseId}&detail=1&published=1"
    )

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        return toonParse(resp.json())


async def get_assignment(itemID: str):
    """Get detailed information for a specific assignment."""
    token = get_access_token()
    access_token = token.token

    headers = {"Authorization": f"Bearer {access_token}"}
    url = mcv(f"/public/get/item/assignment?item_id={itemID}")

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        return toonParse(resp.json())


async def get_playlist(courseId: str):
    """Retrieve video playlists for a course."""
    token = get_access_token()
    access_token = token.token

    headers = {"Authorization": f"Bearer {access_token}"}
    url = mcv(f"/public/get/course/playlists?cv_cid={courseId}")

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        return {
            "suggestion": "Add the YouTube link from the playlist field for ready-to-use playback.",
            "data": toonParse(resp.json()),
        }


async def get_online_meetings(courseId: str):
    """Retrieve online meeting links for a course."""
    token = get_access_token()
    access_token = token.token

    headers = {"Authorization": f"Bearer {access_token}"}
    url = mcv(f"/public/get/course/onlinemeetings?cv_cid={courseId}")

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        return toonParse(resp.json())


async def get_course_schedule(courseId: str):
    """Retrieve the schedule for a course."""
    token = get_access_token()
    access_token = token.token

    headers = {"Authorization": f"Bearer {access_token}"}
    url = mcv(f"/public/get/course/schedule?cv_cid={courseId}")

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        return toonParse(resp.json())
