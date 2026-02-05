from fastmcp import FastMCP

from utils.tool_decorator import *

from mcv.tools.admins import *
from mcv.tag import *

def register(mcp: FastMCP):
    mcp.tool(
        tags={ADMIN_TAG},
        version=API_V1,
        annotations=TOOL_READ_LIVE,
    )(get_student_roster)
