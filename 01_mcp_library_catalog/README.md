# Campus Library Catalog (MCP)

A small Model Context Protocol (MCP) server that lets a client search a sample library catalog and check whether a book is available.

## Run the demo

Open a terminal in this folder. Use Python 3.10 or newer. On Windows, use `py -3` if `python` is unavailable. On macOS or Linux, use `python3` if needed.

```console
python -m pip install -r requirements.txt
python demo_client.py
```

The demo searches for programming books and looks up book B102. Expect two programming titles and an **On loan** status for B102.

| Tool | Example input | What it returns |
|---|---|---|
| `search_books` | `{"query": "programming"}` | Books with matching titles or topics |
| `get_book_status` | `{"book_id": "B102"}` | The matching book, including its status and shelf |

The client starts `server.py` as a subprocess, lists its tools, and calls them over MCP using standard input and output. The demo needs no API key or AI account.

To use your own catalog, edit `BOOKS` in `server.py`. To connect a different MCP client, configure a **stdio** server with the path to your Python interpreter as its command and the absolute path to `server.py` as its argument.

[MCP Python SDK documentation (v1)](https://py.sdk.modelcontextprotocol.io/v1/)
