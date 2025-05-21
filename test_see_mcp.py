# test_sse_mcp.py
import sys
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("TestServer")

@mcp.tool()
def hello(name: str) -> str:
    return f"Hola {name}"

if __name__ == "__main__":
    print("🧠 Archivo que se ejecuta:", sys.argv[0])
    print("✅ Lanzando con SSE...")
    mcp.run(transport="sse")
