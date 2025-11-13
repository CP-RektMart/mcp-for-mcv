from fastmcp import FastMCP
from controllers.courses import list_all_course, get_course_info, get_course_material

def register(mcp: FastMCP): 
    mcp.tool()(list_all_course)
    mcp.tool()(get_course_info)
    mcp.tool()(get_course_material)
