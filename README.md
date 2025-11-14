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

## Tool Usage Examples
Below are example MCP tool calls that can be used by MCP clients (Cursor, Claude, MCP Inspector, etc.) once the server is connected to MyCourseVille.

#### 1. Get User Profile
Natural Language Examples:
```
Get my user profile in mycourseville
```
```
Get me mcv
```
Example Response:
```
{
  "id": "123",
  "display_name": "Siriwid Thongon",
  "student_id": "6530414821",
  "department": "Computer Engineering",
  "email": "student@example.com"
}
```

#### 2. Get All User Courses
Natural Language Examples:
```
List all my courses on MyCourseVille
```
```
Show my classes this semester
```

### 3. Another
```
Get material of course id 
Get announcement
Check my deadline 
Check my instructor of this course
Get Syllabus of this course
Get courses order by ...
```


## Project Structure

```
mcp-for-mcv/
├── src/
│   ├── server.py
│   ├── controllers/
│   ├── routes/
│   ├── config/
│   └──  auth/
├── .env    
├── README.md
└── ...
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## License

This project is for educational purposes.
