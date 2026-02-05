from mcp.types import ToolAnnotations, Annotations

# =============================
# Tool annotations (LLM hints)
# =============================

# Authenticated, read-only, safe to repeat
TOOL_READ = ToolAnnotations(
    readOnlyHint=True,
    openWorldHint=True,
    idempotentHint=True,
)

# Read-only but time-sensitive (live / frequently changing)
TOOL_READ_LIVE = ToolAnnotations(
    readOnlyHint=True,
    openWorldHint=True,
    idempotentHint=False,
)

# Write / mutate state (submit, create, update)
TOOL_WRITE = ToolAnnotations(
    readOnlyHint=False,
    openWorldHint=True,
    idempotentHint=False,
)