import os
import json
from tqdm import tqdm
from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone

# Load .env
load_dotenv()

# Load config
openai_key = os.getenv("OPENAI_API_KEY")
pinecone_key = os.getenv("PINECONE_API_KEY")
pinecone_index = os.getenv("PINECONE_INDEX_NAME")
pinecone_env = os.getenv("PINECONE_ENVIRONMENT")
embedding_model = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

# Initialize clients
client = OpenAI(api_key=openai_key)
pc = Pinecone(api_key=pinecone_key)
index = pc.Index(pinecone_index)

# Load docs
with open("../docs/azure_core_docs.json", encoding="utf-8") as f:
    docs = json.load(f)

# Process and upsert
for i, doc in enumerate(tqdm(docs)):
    text = doc.get("content", "").strip()
    if not text or len(text) < 50:
        continue

    try:
        res = client.embeddings.create(input=[text], model=embedding_model)
        vector = res.data[0].embedding
    except Exception as e:
        print(f"❌ Embedding failed for doc-{i}: {e}")
        continue

    metadata = {
        "title": doc["title"],
        "url": doc["url"],
        "service": doc["service"]
    }

    index.upsert([
        {
            "id": f"doc-{i}",
            "values": vector,
            "metadata": metadata
        }
    ])
    print(f"✅ Indexed doc-{i}: {metadata['title'][:50]}")

print("🚀 All documents embedded and indexed successfully.")
