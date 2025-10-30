# src/tools/course.py
from fastmcp import FastMCP
from data.memory import departments_data, courses_data

def register_course_tools(mcp: FastMCP):
    @mcp.tool()
    async def get_departments() -> dict:
        """Get the list of available departments."""
        return {"departments": departments_data, "next_suggestion": "You can filter courses by providing a department name."}

    @mcp.tool()
    async def get_courses(search: str = "", department: str = "") -> dict:
        """Get courses with optional filtering."""
        if department and department not in departments_data:
            return {
                "courses": [],
                "next_suggestion": f"Department '{department}' not found. Try one of: {', '.join(departments_data)}"
            }

        filtered = [
            c for c in courses_data
            if (not department or c["department"] == department)
            and (not search or search.lower() in c["name"].lower())
        ]
        return {"courses": filtered, "next_suggestion": "You can search by course name or filter by department."}
