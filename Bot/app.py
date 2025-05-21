# app_chainlit.py

import chainlit as cl
from agents import supervisor
from langchain_core.messages import HumanMessage
from agents.supervisor import supervisor_app as supervisor


@cl.on_chat_start
async def on_chat_start():
    await cl.Message("Hola 👋 Soy tu asistente. Envíame texto o una imagen (como ruta local) para analizar.").send()

@cl.on_message
async def on_message(message: cl.Message):
    try:
        user_input = message.content.strip()
        state_input = {"input": user_input}
        result = await supervisor.ainvoke(state_input)

        await cl.Message(f"🧠 Resultado:\n{result['result']}").send()
    except Exception as e:
        await cl.Message(f"❌ Error: {str(e)}").send()
