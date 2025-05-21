# bert_client.py

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import os

client = None  

async def initialize_client():
    global client
    client = MultiServerMCPClient({
        "tools": {
            "url": "http://127.0.0.1:8050/sse",
            "transport": "sse",
        }
    })


async def close_client():
    global client
    if client:
        await client.__aexit__(None, None, None)


async def create_mcp_agent(model):
    if client is None:
        raise Exception("Client not initialized.")
    tools = await client.get_tools()
    return create_react_agent(model, tools, prompt="Eres un agente de análisis de sentimientos.")
