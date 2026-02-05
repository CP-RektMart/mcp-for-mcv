from fastmcp.server.dependencies import get_access_token
from mcv.helper import mcv_get

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
    return await mcv_get("/public/get/user/info")


async def get_user_gradeletter(courseId: str):
    """Get user's letter grade for a specific course."""
    return await mcv_get(f"/public/get/user/gradeletter?cv_cid={courseId}")
