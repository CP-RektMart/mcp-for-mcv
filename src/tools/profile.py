# src/tools/profile.py
from fastmcp import FastMCP
from data.memory import profiles_data

def register_profile_tools(mcp: FastMCP):
    @mcp.tool()
    async def get_myprofile(user_id: str) -> dict:
        """Get the user's profile information."""
        profile = profiles_data.get(user_id)
        if not profile:
            return {
                "error": f"Profile with user_id '{user_id}' not found.",
                "next_suggestion": "Try a valid user_id such as 6530414821 or 1234567890."
            }
        return {**profile, "next_suggestion": "You can now fetch courses or check departments."}
