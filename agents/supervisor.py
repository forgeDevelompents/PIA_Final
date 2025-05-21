import asyncio
from langgraph.prebuilt import create_react_agent
from langgraph.graph import END, StateGraph
from langgraph.prebuilt.tool_node import ToolNode
from langchain_google_genai import ChatGoogleGenerativeAI

from Amcp.bert_client import initialize_client, create_mcp_agent, close_client
from agents.vision_agent import vision_tool  # Herramienta de visión (YOLOv8)


def create_supervisor():
    
    model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    model_kwargs={"streaming": True}  # ✅ forma correcta
    )

    async def create_agent():
        await initialize_client()
        agent = await create_mcp_agent(model)
        return agent

    # ToolNode del agente
    async def agent_node(state):
        agent = await create_agent()
        return await agent.ainvoke(state)

    # ToolNode del agente de visión
    vision_node = ToolNode(vision_tool)

    # Crear el grafo
    workflow = StateGraph()
    workflow.add_node("agente_nlp", agent_node)
    workflow.add_node("agente_vision", vision_node)

    # Conectar nodos
    workflow.set_entry_point("agente_nlp")
    workflow.add_edge("agente_nlp", "agente_vision")
    workflow.add_edge("agente_vision", END)

    app = workflow.compile()
    return app


async def main():
    app = create_supervisor()
    result = await app.ainvoke("¿Qué objetos aparecen en esta imagen?")
    print("\n🧠 Resultado del supervisor:")
    print(result)
    await close_client()


if __name__ == "__main__":
    asyncio.run(main())


#supervisor_app = create_supervisor()
