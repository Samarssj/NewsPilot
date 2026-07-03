# 📰 NewsPilot — Hybrid News Intelligence Platform

> **An AI-powered Hybrid RAG platform that delivers accurate, source-backed answers using live news and general AI knowledge.**

PulseAI combines **Retrieval-Augmented Generation (RAG)** with **Google Gemini** to provide trustworthy responses. When relevant news exists in the local knowledge base, answers are generated from retrieved articles with citations. If no relevant news is found, PulseAI intelligently falls back to Gemini's general knowledge, ensuring users always receive meaningful responses.

---

## ✨ Features

* 📰 Fetches the latest news from **RSS Feeds** and **NewsAPI**
* 🤖 Hybrid AI answering with **RAG + Gemini**
* 📚 Local vector database using **ChromaDB**
* 🔍 Semantic search powered by **Sentence Transformers**
* 💬 Interactive Streamlit chat interface
* 📎 Source-backed answers with clickable references
* ⚡ Automatic fallback to Gemini when news is unavailable
* 💾 Local embeddings and vector storage
* 🎯 Configurable retrieval settings

---

# 🏗️ System Architecture

```text
                ┌───────────────────────────┐
                │   RSS Feeds / NewsAPI     │
                └─────────────┬─────────────┘
                              │
                              ▼
                    Fetch Latest Articles
                              │
                              ▼
                     Text Chunking Engine
                              │
                              ▼
             SentenceTransformer Embeddings
                              │
                              ▼
                  ChromaDB Vector Database
                              │
               ┌──────────────┴──────────────┐
               │                             │
               ▼                             ▼
      Retrieve Relevant Chunks      No Relevant Chunks
               │                             │
               ▼                             ▼
         News-Based Response        Gemini Knowledge
               │                             │
               └──────────────┬──────────────┘
                              ▼
                 Final Answer with Sources
```

---

# 🚀 Tech Stack

| Category        | Technology                           |
| --------------- | ------------------------------------ |
| Frontend        | Streamlit                            |
| LLM             | Google Gemini                        |
| Vector Database | ChromaDB                             |
| Embeddings      | Sentence Transformers                |
| Data Sources    | RSS Feeds, NewsAPI                   |
| Language        | Python                               |
| Retrieval       | RAG (Retrieval-Augmented Generation) |

---

# ⚙️ How It Works

### 1️⃣ News Collection

PulseAI continuously fetches news from:

* RSS Feeds
* NewsAPI *(optional)*

Articles are cleaned and normalized before processing.

---

### 2️⃣ Local Embedding

Each article is

* Split into semantic chunks
* Converted into embeddings using Sentence Transformers
* Stored locally inside ChromaDB

No embeddings are generated using external APIs.

---

### 3️⃣ Intelligent Retrieval

When a question is asked:

* The query is embedded
* Top-K most relevant chunks are retrieved
* Similarity threshold determines whether the retrieved news is sufficiently relevant

---

### 4️⃣ Hybrid Response Generation

If relevant articles exist:

> ✅ Answer is generated using retrieved news with citations.

Otherwise:

> 🤖 Gemini answers using its general knowledge.

This hybrid workflow provides both **freshness** and **broad knowledge coverage**.

---

# 📂 Project Structure

```text
PulseAI/
│
├── app.py                 # Streamlit Web Interface
├── config.py              # Project Configuration
├── news_fetcher.py        # RSS & NewsAPI Fetching
├── vector_store.py        # ChromaDB + Embeddings
├── rag_engine.py          # Hybrid RAG Pipeline
├── ingest.py              # Fetch & Index News
├── ask.py                 # Command-Line Assistant
├── feeds.txt              # Custom RSS Feeds
├── requirements.txt
├── .env.example
└── data/
    └── chroma/            # Local Vector Database
```

---

# ⚡ Installation

### Clone Repository

```bash
git clone <repository-url>
cd PulseAI
```

### Create Virtual Environment

```bash
python -m venv venv
```

Linux / macOS

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file.

```env
GEMINI_API_KEY=YOUR_API_KEY
NEWSAPI_KEY=YOUR_OPTIONAL_KEY
```

> **NewsAPI is optional.** PulseAI works using RSS feeds even without it.

---

# ▶️ Usage

## Fetch Latest News

```bash
python ingest.py
```

Optional commands

```bash
python ingest.py --no-fulltext

python ingest.py --query "Artificial Intelligence"

python ingest.py --feeds feeds.txt
```

---

## Ask Questions (CLI)

```bash
python ask.py
```

or

```bash
python ask.py "Latest AI regulations"
```

---

## Launch Web Application

```bash
streamlit run app.py
```

---

# 💬 Example Questions

* What's happening in the AI industry today?
* Latest developments in the stock market?
* Explain the recent Israel–Iran conflict.
* What are today's technology headlines?
* Tell me the latest sports news.
* What's the current state of cryptocurrency?

---

# 📊 Hybrid Answer Flow

| Situation               | Response Source        |
| ----------------------- | ---------------------- |
| Relevant news available | 📰 Local News Database |
| No relevant news found  | 🤖 Gemini Knowledge    |

---

# 🎯 Why PulseAI?

Unlike traditional chatbots that rely solely on an LLM or static retrieval, PulseAI intelligently combines both approaches.

✅ Live News Retrieval

✅ Semantic Search

✅ Source-backed Answers

✅ Local Vector Storage

✅ Hybrid AI Responses

✅ Fast and Lightweight

---

# 🔮 Future Improvements

* User authentication
* Chat history persistence
* News summarization
* Trending topic analytics
* Multi-language support
* Voice interaction
* Real-time streaming responses
* Docker deployment
* Cloud-hosted vector database
* Admin dashboard

---

# 📌 Notes

* ChromaDB persists data locally.
* Full-text extraction may not work for paywalled websites.
* RSS summaries are used automatically when extraction fails.
* The quality of responses depends on indexed news freshness.
* Gemini fallback ensures the assistant remains useful even when relevant news is unavailable.

---

# 📄 License

This project is intended for educational, research, and portfolio purposes. Feel free to modify and extend it for your own use.

---

## ⭐ If you found this project useful, consider giving it a star!
<img width="1440" height="900" alt="Screenshot 2026-07-04 at 01 22 13" src="https://github.com/user-attachments/assets/2cee2a7b-db42-4a11-872c-fb17d1155f75" />

