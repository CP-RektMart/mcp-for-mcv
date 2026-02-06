from fastmcp import FastMCP

from utils.tool_decorator import *

from mcv.tools.users import *
from mcv.tag import *


def register(mcp: FastMCP):
    mcp.tool(
        tags={USER_TAG},
        version=API_V1,
        annotations=TOOL_READ,
    )(get_me)
    mcp.tool(
        tags={USER_TAG, INFO_TAG},
        version=API_V1,
        annotations=TOOL_READ,
    )(get_user_info)
    mcp.tool(
        tags={USER_TAG},
        version=API_V1,
        annotations=TOOL_READ_LIVE,
    )(get_user_gradeletter)
