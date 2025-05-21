import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

async def main():
    async with sse_client("http://localhost:8050/sse") as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("🛠️ Herramientas disponibles:")
            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")

            result = await session.call_tool("classify_review", arguments={
                "text": "This product is not as high as my expectations!"
            })

            print("\n✅ Resultado del análisis:")
            print(result.content[0].text)

if __name__ == "__main__":
    asyncio.run(main())
