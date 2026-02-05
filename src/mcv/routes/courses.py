from fastmcp import FastMCP

from utils.tool_decorator import *

from mcv.tools.courses import *
from mcv.tag import *

def register(mcp: FastMCP):
    mcp.tool(
        tags={COURSE_TAG},
        version=API_V1,
        annotations=TOOL_READ,
    )(list_all_courses)

    mcp.tool(
        tags={COURSE_TAG, INFO_TAG},
        version=API_V1,
        annotations=TOOL_READ,
    )(get_course_infos)

    mcp.tool(
        tags={COURSE_TAG, MATERIAL_TAG},
        version=API_V1,
        annotations=TOOL_READ,
    )(get_course_materials)

    mcp.tool(
        tags={COURSE_TAG, ASSIGNMENT_TAG},
        version=API_V1,
        annotations=TOOL_READ,
    )(get_course_assignments)

    mcp.tool(
        tags={COURSE_TAG, ASSIGNMENT_TAG},
        version=API_V1,
        annotations=TOOL_READ,
    )(get_assignment)

    mcp.tool(
        tags={COURSE_TAG, MEDIA_TAG},
        version=API_V1,
        annotations=TOOL_READ,
    )(get_playlist)

    mcp.tool(
        tags={COURSE_TAG, SCHEDULE_TAG},
        version=API_V1,
        annotations=TOOL_READ,
    )(get_course_schedule)

    mcp.tool(
        tags={COURSE_TAG, ANNOUNCEMENT_TAG},
        version=API_V1,
        annotations=TOOL_READ_LIVE,
    )(get_course_announcements)

    mcp.tool(
        tags={COURSE_TAG, MEETING_TAG},
        version=API_V1,
        annotations=TOOL_READ_LIVE,
    )(get_online_meetings)
