# bert_mcp.py

from mcp.server.fastmcp import FastMCP
from transformers import pipeline

mcp = FastMCP("BERT Sentiment Service", host="127.0.0.1", port=8050)

bert_pipeline = pipeline("text-classification", model="eidrieenbe/bert-novex-reviews", tokenizer="bert-base-uncased")

@mcp.tool()
def classify_review(text: str) -> dict:
    """
    Clasifica una reseña de producto como positiva o negativa.

    Args:
        text: Texto de la reseña.

    Returns:
        Un diccionario con el sentimiento ('positive'/'negative') y la confianza.
    """
    result = bert_pipeline(text)[0]
    label = result["label"]
    score = result["score"]
    sentiment = "positive" if label == "LABEL_1" else "negative"
    return {"sentiment": sentiment, "confidence": score}

# Ejecutar el servidor
if __name__ == "__main__":
    print("✅ Lanzando con SSE...")
    mcp.run(transport="sse")

