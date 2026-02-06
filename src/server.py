from fastmcp import FastMCP


from config.env import (
    APP_NAME,
    HOST,
    PORT,
    TRANSPORT,
)
from mcv.routes import admins, courses, root, users
from mcv.auth.mcv import MCVProvider
from mcv.env import (
    MCV_CLIENT_ID,
    MCV_CLIENT_SECRET,
    MCV_REDIRECT_PATH   
)

auth = MCVProvider(
    client_id=MCV_CLIENT_ID,
    client_secret=MCV_CLIENT_SECRET,
    # client_storage = FernetEncryptionWrapper(
    #     key_value=RedisStore(host="localhost", port=6379),
    #     fernet=Fernet(key)
    # ),
    client_storage=None,
    base_url="http://localhost:8000",
    redirect_path=MCV_REDIRECT_PATH,
    allowed_client_redirect_uris=[
        "http://localhost:*",
        "http://127.0.0.1:*",
        "https://claude.ai/api/mcp/auth_callback",
    ],
)

mcp = FastMCP(APP_NAME, auth=auth)

root.register(mcp)
users.register(mcp)
courses.register(mcp)
admins.register(mcp)

if __name__ == "__main__":
    # When running under Cursor via Docker, we use stdio transport.
    # FastMCP's stdio mode must not receive host/port, and stdout must be pure MCP JSON.
    if TRANSPORT == "stdio":
        mcp.run(transport="stdio", show_banner=False)
    else:
        print(f"🚀 Starting {APP_NAME} on {TRANSPORT}://{HOST}:{PORT}")
        mcp.run(transport=TRANSPORT, host=HOST, port=PORT)
