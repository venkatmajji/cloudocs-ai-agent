from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from openai import OpenAI
import pinecone
import os

# Load environment
load_dotenv()

# OpenAI & Pinecone setup
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENVIRONMENT")
)
index = pinecone.Index(os.getenv("PINECONE_INDEX_NAME"))

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

# Request schema
class AskRequest(BaseModel):
    question: str

# Route
@app.post("/ask")
def ask(req: AskRequest):
    query = req.question.strip()
    if not query:
        return {"error": "Empty question."}

    # Embed user question
    try:
        embed = client.embeddings.create(
            input=[query],
            model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
        ).data[0].embedding
    except Exception as e:
        return {"error": f"Embedding failed: {str(e)}"}

    # Query Pinecone
    try:
        results = index.query(vector=embed, top_k=3, include_metadata=True)
        contexts = [match.metadata["title"] + ":\n" + match.metadata["url"] for match in results.matches]
        context_text = "\n\n".join(contexts)
    except Exception as e:
        return {"error": f"Pinecone query failed: {str(e)}"}

    # Compose prompt
    prompt = f"""You are a Microsoft cloud expert assistant. Use the following documentation snippets to answer the question concisely and accurately:

{context_text}

Q: {query}
A:"""

    # Call OpenAI
    try:
        chat = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        answer = chat.choices[0].message.content.strip()
    except Exception as e:
        return {"error": f"OpenAI failed: {str(e)}"}

    return {
        "answer": answer,
        "sources": contexts
    }
