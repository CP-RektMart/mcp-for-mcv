from fastmcp import FastMCP
from controllers.admins import get_student_roster


def register(mcp: FastMCP):
    mcp.tool()(get_student_roster)
