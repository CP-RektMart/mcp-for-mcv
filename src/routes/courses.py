from fastmcp import FastMCP
from controllers.courses import list_all_courses, get_course_infos, get_course_materials, get_course_assignments, get_course_announcements, get_assignment

def register(mcp: FastMCP): 
    mcp.tool()(list_all_courses)
    mcp.tool()(get_course_infos)
    mcp.tool()(get_course_materials)
    mcp.tool()(get_course_assignments)
    mcp.tool()(get_course_announcements)
    mcp.tool()(get_assignment)