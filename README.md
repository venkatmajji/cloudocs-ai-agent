# CloudDocs AI 🔍☁️

An AI-powered assistant for Microsoft documentation — ask technical questions and get accurate answers sourced directly from official Azure, Key Vault, and AI Services docs.

## ✨ Features

- ✅ FastAPI backend using OpenAI + Pinecone
- ✅ Crawls Microsoft Docs and embeds into vector DB
- ✅ React + Tailwind UI (fully responsive)
- ✅ Hosted on Render with CI/CD
- ✅ No hallucinations — only real docs as sources

## 🚀 Try It Live

👉 https://cloudocs-ui.onrender.com/

## 🛠 Stack

- Frontend: React + TailwindCSS + Vite
- Backend: FastAPI + OpenAI GPT-4 + Pinecone
- Deployment: Render.com (separate frontend & backend services)

## 📚 How It Works

1. Crawler scrapes selected Microsoft Docs sections
2. Embeds content via OpenAI and stores in Pinecone
3. FastAPI receives user questions, embeds them, and performs similarity search
4. Answers generated using top matched docs as context

## 🧪 Dev Setup

```bash
# Backend
cd scraper
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Frontend
cd ui
npm install
npm run dev

