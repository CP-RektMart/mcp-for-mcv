from mcv.helper import mcv_get

async def get_student_roster(courseId: str):
    """Get list of all students enrolled in a course."""
    return await mcv_get(f"/public/get/course/roster?cv_cid={courseId}")
