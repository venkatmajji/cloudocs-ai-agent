from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from openai import OpenAI
import pinecone
import os

# Load env vars
load_dotenv()

# Clients
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENVIRONMENT")
)
index = pinecone.Index(os.getenv("PINECONE_INDEX_NAME"))

# FastAPI app
app = FastAPI()

# Allow CORS (optional if building frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Request model
class AskRequest(BaseModel):
    question: str

@app.post("/ask")
def ask(req: AskRequest):
    query = req.question.strip()
    if not query:
        return {"error": "Question is empty."}

    try:
        embedding = client.embeddings.create(
            input=[query],
            model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
        ).data[0].embedding
    except Exception as e:
        return {"error": f"Embedding failed: {str(e)}"}

    try:
        results = index.query(vector=embedding, top_k=3, include_metadata=True)
        contexts = [f"{m.metadata['title']}\n{m.metadata['url']}" for m in results.matches]
        context_block = "\n\n".join(contexts)
    except Exception as e:
        return {"error": f"Pinecone query failed: {str(e)}"}

    prompt = f"""You are a helpful Microsoft cloud expert. Use the following documentation snippets to answer the user's question with accurate, concise information.

{context_block}

Q: {query}
A:"""

    try:
        chat = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        answer = chat.choices[0].message.content.strip()
    except Exception as e:
        return {"error": f"OpenAI failed: {str(e)}"}

    return {
        "answer": answer,
        "sources": contexts
    }
