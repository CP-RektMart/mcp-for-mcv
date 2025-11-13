from fastmcp import FastMCP
from config.contants import APP_NAME, HOST, PORT, TRANSPORT, MCV_CLIENT_ID, MCV_CLIENT_SECRET, MCV_REDIRECT_PATH
from routes import root, users, courses
from auth.mcv import MCVProvider

auth = MCVProvider(
    client_id=MCV_CLIENT_ID,
    client_secret=MCV_CLIENT_SECRET,
    base_url="http://localhost:8000",
    redirect_path=MCV_REDIRECT_PATH,
    jwt_signing_key="my-super-secret-32-byte-key"
)

mcp = FastMCP(APP_NAME, auth=auth)

root.register(mcp)
users.register(mcp)
courses.register(mcp)

if __name__ == "__main__":
    print(f"🚀 Starting {APP_NAME} on {TRANSPORT}://{HOST}:{PORT}")
    mcp.run(transport=TRANSPORT, host=HOST, port=PORT)