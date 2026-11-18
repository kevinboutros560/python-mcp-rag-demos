import asyncio
import json
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main() -> None:
    server_path = Path(__file__).with_name("server.py").resolve()
    server = StdioServerParameters(command=sys.executable, args=[str(server_path)])

    async with stdio_client(server) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("Tools:", ", ".join(tool.name for tool in tools.tools))

            for name, arguments in [
                ("search_books", {"query": "programming"}),
                ("get_book_status", {"book_id": "B102"}),
            ]:
                result = await session.call_tool(name, arguments=arguments)
                if result.isError:
                    raise RuntimeError(f"{name} failed: {result.content}")

                print(f"\n{name}({arguments})")
                print(json.dumps(result.structuredContent, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
