# src/tools/info.py
from fastmcp import FastMCP

def register_info_tools(mcp: FastMCP):
    @mcp.tool()
    async def get_mcv_info(topic: str = "") -> dict:
        """Provides general knowledge or guidance about MyCourseVille."""
        knowledge_base = {
            "mcv": "MyCourseVille (MCV) is the student portal used at Chulalongkorn University to access course information, registration, and profile management.",
            "courses": "Courses contain information like course ID, name, department, and syllabus. You can filter courses by name or department.",
            "profile": "You can fetch a student's profile using their user ID. The profile includes their name, email, and suggested next actions.",
            "departments": "Departments categorize courses. You can list all available departments and filter courses accordingly."
        }

        info = knowledge_base.get(topic.lower(), "MCV is the student portal at Chulalongkorn University for accessing courses, profiles, and departments.")
        return {"info": info, "next_suggestion": "You can ask about courses, departments, or fetch your profile using user ID."}

    @mcp.tool()
    async def get_help() -> dict:
        """List all available MCP tools/functions with a short description."""
        functions_info = [
            {"name": "get_myprofile", "description": "Fetch a student's profile information using their user ID."},
            {"name": "get_courses", "description": "Get courses, optionally filtered by course name or department."},
            {"name": "get_departments", "description": "List all available departments."},
            {"name": "get_mcv_info", "description": "Get general knowledge or guidance about MyCourseVille."},
            {"name": "get_help", "description": "List all available functions with descriptions."}
        ]
        return {"functions": functions_info, "next_suggestion": "You can try calling any of these functions with appropriate parameters."}
