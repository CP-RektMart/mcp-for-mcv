from fastmcp import FastMCP
from config.contants import APP_NAME, HOST, PORT, TRANSPORT, MCV_CLIENT_ID, MCV_CLIENT_SECRET, MCV_REDIRECT_PATH
from routes import root, users, courses
from auth.mcv import MCVProvider

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
    ]
)

mcp = FastMCP(APP_NAME, auth=auth)

root.register(mcp)
users.register(mcp)
courses.register(mcp)

if __name__ == "__main__":
    print(f"🚀 Starting {APP_NAME} on {TRANSPORT}://{HOST}:{PORT}")
    mcp.run(transport=TRANSPORT, host=HOST, port=PORT)