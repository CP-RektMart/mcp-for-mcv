# src/server.py
from fastmcp import FastMCP
from tools.info import register_info_tools
from tools.profile import register_profile_tools
from tools.course import register_course_tools
from routes.root import register_routes

mcp = FastMCP("mcv-mcp-server")

# Register tools and routes
register_info_tools(mcp)
register_profile_tools(mcp)
register_course_tools(mcp)
register_routes(mcp)

if __name__ == "__main__":
    print("🚀 Starting MyCourseVille MCP Server on http://127.0.0.1:8001")
    mcp.run(transport="http", host="127.0.0.1", port=8001)
