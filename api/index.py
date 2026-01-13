import os
import sys
from pathlib import Path

# Add src directory to Python path
root_dir = Path(__file__).parent.parent
src_dir = root_dir / "src"
sys.path.insert(0, str(root_dir))
sys.path.insert(0, str(src_dir))

try:
    from fastmcp import FastMCP

    from auth.mcv import MCVProvider
    from routes import admins, courses, root, users

    # Get environment variables
    APP_NAME = os.getenv("APP_NAME", "mcv-mcp-server")
    MCV_CLIENT_ID = os.getenv("MCV_CLIENT_ID", "")
    MCV_CLIENT_SECRET = os.getenv("MCV_CLIENT_SECRET", "")
    MCV_REDIRECT_PATH = os.getenv("MCV_REDIRECT_PATH", "/callback")

    # Determine base URL
    base_url = os.getenv("VERCEL_URL")
    if base_url:
        base_url = f"https://{base_url}"
    else:
        base_url = os.getenv("BASE_URL", "http://localhost:8000")

    # Initialize auth provider
    auth = MCVProvider(
        client_id=MCV_CLIENT_ID,
        client_secret=MCV_CLIENT_SECRET,
        client_storage=None,
        base_url=base_url,
        redirect_path=MCV_REDIRECT_PATH,
        allowed_client_redirect_uris=[
            "http://localhost:*",
            "http://127.0.0.1:*",
            "https://claude.ai/api/mcp/auth_callback",
            "https://*.vercel.app/*",
        ],
    )

    # Create FastMCP instance
    mcp = FastMCP(APP_NAME, auth=auth)

    # Register routes
    root.register(mcp)
    users.register(mcp)
    courses.register(mcp)
    admins.register(mcp)

    # Export app for Vercel
    app = mcp.app

except Exception as e:
    # Fallback simple app for debugging
    from fastapi import FastAPI

    app = FastAPI()

    @app.get("/")
    def health():
        return {
            "status": "error",
            "message": str(e),
            "python_path": sys.path,
            "cwd": os.getcwd(),
        }

    @app.get("/health")
    def health_check():
        return {"status": "error", "details": str(e)}
