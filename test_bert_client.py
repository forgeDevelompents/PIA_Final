# test_bert_client.py

import asyncio
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline
from langchain_openai import ChatOpenAI
from Amcp.bert_client import initialize_client, create_mcp_agent, close_client
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
import os
from langchain_google_genai import ChatGoogleGenerativeAI


async def main():
    await initialize_client()

    load_dotenv() 

    llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7)

    agent = await create_mcp_agent(llm)

    result = await agent.ainvoke(HumanMessage(content="Este producto es una maravilla, me ha encantado"))

    print("\n Respuesta del agente:")
    print(result)

    await close_client()

if __name__ == "__main__":
    asyncio.run(main())
