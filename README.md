# CloudDocs AI 🔍☁️

An AI-powered assistant for Microsoft documentation — ask technical questions and get accurate answers sourced directly from official Azure, Key Vault, and AI Services docs.

## ✨ Features

- ✅ FastAPI backend using OpenAI + Pinecone
- ✅ Crawls Microsoft Docs and embeds into vector DB
- ✅ React + Tailwind UI (fully responsive)
- ✅ Hosted on Render with CI/CD
- ✅ No hallucinations — only real docs as sources

## 🚀 Try It Live

👉 [https://cloud-docs-ui.onrender.com](https://cloud-docs-ui.onrender.com)

## 🛠 Stack

- **Frontend**: React + TailwindCSS + Vite  
- **Backend**: FastAPI + OpenAI GPT-4 + Pinecone  
- **Deployment**: Render.com (separate frontend & backend services)

## 📚 How It Works

1. Crawler scrapes selected Microsoft Docs sections
2. Embeds content via OpenAI and stores in Pinecone
3. FastAPI receives user questions, embeds them, and performs similarity search
4. Answers generated using top matched docs as context

## 🧪 Local Dev Setup

```bash
# Backend (from root/scraper)
cd scraper
python -m venv venv && source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt

# Frontend (from root/ui)
cd ui
npm install
npm run dev
```

## 📁 Project Structure

```
cloudocs-ai-agent/
├── scraper/            # Crawler, embedder, FastAPI backend
├── ui/                 # React + Tailwind frontend
├── docs/               # Raw + embedded document JSON
├── render.yaml         # Render deployment config for both services
└── .env.example        # Example env file for secrets
```

## 🌐 Deployment

This app is deployed fully on [Render](https://render.com):

- **Backend (FastAPI)**  
  [https://cloudocs-ai-agent-6xv2.onrender.com](https://cloudocs-ai-agent-6xv2.onrender.com)  
  Handles `/ask` POST request and returns answers from Pinecone + OpenAI

- **Frontend (React + Tailwind)**  
  [https://cloud-docs-ui.onrender.com](https://cloud-docs-ui.onrender.com)  
  Clean landing page and live Q&A interface

To deploy your own version:
- Fork this repo
- Add your `.env` secrets (see below)
- Push to GitHub → Render auto-deploys both services from `render.yaml`

## 🔐 Environment Variables

Copy `.env.example` → `.env` and fill in your API credentials:

```bash
cp .env.example .env
```

Then restart your backend service or FastAPI server.

## 👤 Author

Built by **[Bhaskar Majji](https://www.linkedin.com/in/bhaskarmajji)** —  
Microsoftie, Startup builder, AI agent tinkerer, and cloud tech strategist.

> *“Turning complex documentation into instant clarity.”*

---

MIT License • Powered by OpenAI, Pinecone, and Render
