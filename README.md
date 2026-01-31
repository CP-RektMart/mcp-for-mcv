# mcp-for-mcv

Capstone Project 2025

## Created By

- [Chanatip Kowsurat](https://github.com/NhongSun)
- [Siriwid Thongon](https://github.com/tin2003tin)
- [Phumsiri Sumativit](https://github.com/Phumsirii)
- [Chanatpakorn Sirintronsopon](https://github.com/ChanatpakornS)

---

## Project Overview

**mcp-for-mcv** is a lightweight MyCourseVille MCP (MyCourseVille Control Panel) server.  
It provides tools for fetching course data, student profiles, and department information using FastMCP.

This project is designed for extensibility, performance, and ease of integration with MCP-enabled clients such as Cursor, Claude, and internal MCP inspectors.

## Features

- Fetch course data from MyCourseVille
- Retrieve student profiles
- Access department information
- Built with [FastMCP](https://github.com/your-org/fastmcp) for performance and extensibility
- Supports MCP tools, inspectors, and external agents

## Installation

1. Ensure you have **Python 3.10+** installed.
2. Install uv

   ```bash
   pip install uv
   ```
3. Install dependencies.
You can install FastAPI and FastMCP individually:
   ```
   uv add fastapi
   uv add fastmcp
   ```
   Or install everything from pyproject.toml:
   ```
   uv run
   ```

4. Start the server
   ```
   uv run src/server.py
   ```
   Default MCP server URL:
   ```
   http://localhost:8000/mcp
   ```
## MCP Inspector
   To run the MCP Inspector: 
   ```
   uv run fastmcp dev --ui-port 3000 .\src\server.py
   ```
   - Select Transport Type: Streamable HTTP
   - Set the URI to your server URL (default: http://localhost:8000/mcp)

## Integration Guide  
### Cursor
1. Press Ctrl + P → search: `>Open MCP Settings`
2. Click Add New MCP Server
3. Add the following to your `mcp.json`:
   ```
   {
      "mcpServers": {
         "mcv-mcp-server-2123": {
            "command": "npx mcp-remote http://localhost:8000/mcp 6274"
            }
      }
   }

   ```
4. If successful, Cursor will open a browser window for MCV login.

### Claude (Anthropic)
(TODO — integration instructions will be added soon.)

### Other MCP Clients
(Coming soon.)

## Available Tools

Below are the MCP tools available for use with MCP clients (Cursor, Claude, MCP Inspector, etc.) once the server is connected to MyCourseVille.

### 🧑‍💻 User

| Tool | Parameters | Description |
|------|------------|-------------|
| `get_me` | — | Get current user's basic identity from access token |
| `get_user_info` | — | Get user's detailed profile (student details, account info) |
| `get_user_gradeletter` | `courseId: str` | Get user's letter grade for a specific course |

### 📚 Course

| Tool | Parameters | Description |
|------|------------|-------------|
| `list_all_courses` | — | List all courses the user is enrolled in |
| `get_course_infos` | `courseId: str` | Get detailed information about a course |
| `get_course_materials` | `courseId: str` | Get all published materials for a course |
| `get_course_assignments` | `courseId: str` | Get all published assignments for a course |
| `get_course_announcements` | `courseId: str` | Get all announcements for a course |
| `get_assignment` | `itemID: str` | Get details of a specific assignment |
| `get_playlist` | `courseId: str` | Get YouTube playlists for a course |
| `get_online_meetings` | `courseId: str` | Get scheduled online meetings for a course |
| `get_course_schedule` | `courseId: str` | Get the schedule of a course |

### 👨‍🏫 Staff

| Tool | Parameters | Description |
|------|------------|-------------|
| `get_student_roster` | `courseId: str` | Get list of all students enrolled in a course |


## Project Structure

```
mcp-for-mcv/
├── src/
│   ├── server.py              # Main entry point - registers all routes
│   ├── controllers/
│   │   ├── users.py           # User tool implementations
│   │   ├── courses.py         # Course tool implementations
│   │   └── admins.py          # Admin tool implementations
│   ├── routes/
│   │   ├── root.py            # HTTP endpoints (/, /health)
│   │   ├── users.py           # Registers user-related tools
│   │   ├── courses.py         # Registers course-related tools
│   │   └── admins.py          # Registers admin-related tools
│   ├── config/
│   │   └── constants.py       # Environment configuration
│   ├── auth/
│   │   └── mcv.py             # MyCourseVille OAuth provider
│   └── utils/
│       ├── mcv.py             # MCV API URL builder
│       └── toon.py            # Response parser utility
├── .env
├── pyproject.toml
├── README.md
└── uv.lock
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## License

This project is for educational purposes.
