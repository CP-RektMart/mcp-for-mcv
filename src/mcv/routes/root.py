# src/routes/root.py
from starlette.requests import Request
from starlette.responses import HTMLResponse, PlainTextResponse
from fastmcp import FastMCP

def register(mcp: FastMCP):
    @mcp.custom_route("/", methods=["GET"])
    async def root(request: Request) -> HTMLResponse:
        html = """
        <!doctype html>
        <html>
        <head><meta charset="utf-8"/><title>MyCourseVille MCP</title></head>
        <body><h1>MyCourseVille — MCP Server</h1><p>Demo MCP Service Running!</p></body>
        </html>
        """
        return HTMLResponse(content=html)

    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> PlainTextResponse:
        return PlainTextResponse("OK")
