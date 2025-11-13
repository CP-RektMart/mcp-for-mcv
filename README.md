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

## Features

- Fetch course data from MyCourseVille
- Retrieve student profiles
- Access department information
- Built with [FastMCP](https://github.com/your-org/fastmcp) for performance and extensibility

## Installation

1. Ensure you have **Python 3.10+** installed.
2. Install required packages and initialize the environment:

   ```bash
   pip install uv
   ```

## Usage

Start the server with:

```bash
uv run src/server.py
```

The server will run at [http://127.0.0.1:8001](http://127.0.0.1:8000).

## Project Structure

```
mcp-for-mcv/
├── src/
│   ├── server.py
│   ├── tools/
│   └── routes/
├── README.md
└── ...
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## License

This project is for educational purposes.
