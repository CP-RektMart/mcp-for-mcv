from utils.mcv import mcv_get


async def list_all_courses():
    """List all courses the user is enrolled in."""
    return await mcv_get("/public/get/user/courses?detail=1")


async def get_course_infos(courseId: str):
    """Get detailed information about a course."""
    return await mcv_get(f"/public/get/course/info?cv_cid={courseId}")


async def get_course_materials(courseId: str):
    """Get all published materials for a course."""
    return await mcv_get(
        f"/public/get/course/materials?cv_cid={courseId}&detail=1&published=1"
    )


async def get_course_assignments(courseId: str):
    """Get all published assignments for a course."""
    return await mcv_get(
        f"/public/get/course/assignments?cv_cid={courseId}&detail=1&published=1"
    )


async def get_course_announcements(courseId: str):
    """Get all announcements for a course."""
    return await mcv_get(
        f"/public/get/course/announcements?cv_cid={courseId}&detail=1&published=1"
    )


async def get_assignment(itemID: str):
    """Get details of a specific assignment."""
    return await mcv_get(f"/public/get/item/assignment?item_id={itemID}")


async def get_playlist(courseId: str):
    """Get YouTube playlists for a course."""
    return await mcv_get(
        f"/public/get/course/playlists?cv_cid={courseId}",
        suggestion="Add the youtube link for the ready-to-use, from the youtube playlist field",
    )


async def get_online_meetings(courseId: str):
    """Get scheduled online meetings for a course."""
    return await mcv_get(f"/public/get/course/onlinemeetings?cv_cid={courseId}")


async def get_course_schedule(courseId: str):
    """Get the schedule of a course."""
    return await mcv_get(f"/public/get/course/schedule?cv_cid={courseId}")
