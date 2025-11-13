from fastmcp import FastMCP
from fastmcp.server.dependencies import get_access_token
import httpx

async def list_all_course():
    token = get_access_token()
    access_token = token.token  

    headers = {"Authorization": f"Bearer {access_token}"}
    url = "https://www.mycourseville.com/api/v1/public/get/user/courses?detail=1"

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        courses = resp.json()
        return courses
    

async def get_course_info(courseId: str):
    token = get_access_token()
    access_token = token.token 

    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"https://www.mycourseville.com/api/v1/public/get/course/info?cv_cid={courseId}"

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        courses = resp.json()
        return courses
    
async def get_course_material(courseId: str):
    token = get_access_token()
    access_token = token.token 

    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"https://www.mycourseville.com/api/v1/public/get/course/materials?cv_cid={courseId}&detail=1&published=1"

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        courses = resp.json()
        return courses