<div align="center">

# ✦ NewsPilot

### A transparent AI newsroom for asking better questions about the latest news.

NewsPilot combines live news ingestion, local semantic retrieval, and Google Gemini into a hybrid RAG workspace. When the local index contains strong evidence, the assistant answers from retrieved articles with citations. When the evidence is insufficient, it can transparently fall back to general knowledge instead of fabricating sources.

[![Open Repository](https://img.shields.io/badge/GitHub-Samarssj%2FNewsPilot-181717?style=for-the-badge&logo=github)](https://github.com/Samarssj/NewsPilot)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Gemini](https://img.shields.io/badge/Google%20Gemini-Generative%20AI-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)

</div>

---

## Why NewsPilot?

Traditional chat interfaces often hide where an answer came from. NewsPilot is designed around a different principle: **the answer and the evidence should be visible together**. The application retrieves relevant article chunks, scores their semantic distance, routes the question through a grounded or fallback path, and exposes the retrieval trace through interactive visualizations.

The current interface is a red-themed, responsive Streamlit workspace with a richer chat environment, source cards, retrieval-distance graphs, supporting-chunk graphs, light/dark mode, and mobile-safe sidebar behavior.

## Product Highlights

| Capability | What it provides |
| --- | --- |
| **Live news index** | Ingests current stories from RSS feeds and optional NewsAPI queries. |
| **Local semantic memory** | Chunks article text, embeds it locally, and persists it in ChromaDB. |
| **Hybrid answer routing** | Uses grounded news context when relevance is strong and optionally falls back to Gemini knowledge. |
| **Transparent citations** | Displays clickable article references beside news-grounded answers. |
| **Retrieval graph** | Visualizes article relevance distance, where lower distance means a closer semantic match. |
| **Chunk graph** | Shows how many supporting chunks were merged for each retrieved article. |
| **Responsive workspace** | Includes a collapsible mobile sidebar, explicit light-mode controls, and accessible red-theme contrast. |

## Technology Stack

<div align="center">

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-4285F4?style=flat-square&logo=google&logoColor=white)](https://ai.google.dev/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-F97316?style=flat-square&logo=database&logoColor=white)](https://www.trychroma.com/)
[![Sentence Transformers](https://img.shields.io/badge/Sentence%20Transformers-111827?style=flat-square&logo=huggingface&logoColor=yellow)](https://www.sbert.net/)
[![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat-square&logo=plotly&logoColor=white)](https://plotly.com/python/)
[![RSS](https://img.shields.io/badge/RSS-FFA500?style=flat-square&logo=rss&logoColor=white)](https://www.rssboard.org/rss-specification)
[![NewsAPI](https://img.shields.io/badge/NewsAPI-111827?style=flat-square&logo=newsapi&logoColor=white)](https://newsapi.org/)

</div>

### Stack Icon Wall

<div align="center">
  <a href="https://www.python.org/"><img src="https://cdn.simpleicons.org/python/3776AB" alt="Python" height="46"></a>&nbsp;&nbsp;
  <a href="https://streamlit.io/"><img src="https://cdn.simpleicons.org/streamlit/FF4B4B" alt="Streamlit" height="46"></a>&nbsp;&nbsp;
  <a href="https://ai.google.dev/"><img src="https://cdn.simpleicons.org/google/4285F4" alt="Google Gemini" height="46"></a>&nbsp;&nbsp;
  <a href="https://www.trychroma.com/"><img src="https://img.shields.io/badge/ChromaDB-F97316?style=for-the-badge&logo=database&logoColor=white" alt="ChromaDB" height="46"></a>&nbsp;&nbsp;
  <a href="https://huggingface.co/thenlper/gte-small"><img src="https://cdn.simpleicons.org/huggingface/FFD21E" alt="Sentence Transformers" height="46"></a>&nbsp;&nbsp;
  <a href="https://plotly.com/python/"><img src="https://cdn.simpleicons.org/plotly/3F4F75" alt="Plotly" height="46"></a>&nbsp;&nbsp;
  <a href="https://www.rssboard.org/rss-specification"><img src="https://cdn.simpleicons.org/rss/FFA500" alt="RSS" height="46"></a>&nbsp;&nbsp;
  <a href="https://github.com/Samarssj/NewsPilot"><img src="https://cdn.simpleicons.org/github/181717" alt="GitHub" height="46"></a>
  <br>
  <sub><b>Python</b> · <b>Streamlit</b> · <b>Gemini</b> · <b>ChromaDB</b> · <b>Sentence Transformers</b> · <b>Plotly</b> · <b>RSS</b> · <b>GitHub</b></sub>
</div>

| Layer | Implementation |
| --- | --- |
| **Interface** | Streamlit, custom CSS, responsive layout, Plotly charts |
| **Language** | Python |
| **Generation** | Google Gemini Generative AI |
| **Embeddings** | Sentence Transformers with `all-MiniLM-L6-v2` by default |
| **Vector store** | Persistent ChromaDB collection |
| **Ingestion** | RSS feeds, optional NewsAPI, BeautifulSoup, newspaper3k |
| **Configuration** | `.env` variables with optional Streamlit secrets support |

The interface uses Streamlit [1], generation uses Google Gemini [2], vector persistence uses ChromaDB [3], embeddings use Sentence Transformers [4], and retrieval charts use Plotly [5]. RSS ingestion follows the RSS 2.0 format [7], while NewsAPI remains an optional news provider [6].

## Architecture

```mermaid
flowchart LR
    A[RSS Feeds] --> C[News Fetcher]
    B[NewsAPI optional] --> C
    C --> D[Clean and normalize articles]
    D --> E[Chunk text]
    E --> F[Sentence Transformer embeddings]
    F --> G[(Persistent ChromaDB index)]

    Q[User question] --> H[Query embedding and retrieval]
    G --> H
    H --> I{Enough relevant evidence?}
    I -->|Yes| J[Grounded Gemini answer]
    I -->|No and fallback enabled| K[Gemini general knowledge]
    I -->|No and fallback disabled| L[Transparent insufficient-context response]

    J --> M[Answer + citations + retrieval trace]
    K --> N[Answer + fallback badge]
    L --> N
```

The retrieval engine does not force unrelated articles into an answer. It filters results using a configurable distance threshold and minimum-relevance rule. The interface receives the same retrieval metadata used for routing, which keeps the charts and answer badges tied to real query results rather than simulated analytics.

## End-to-End Workflow

```mermaid
sequenceDiagram
    participant U as User
    participant UI as Streamlit workspace
    participant R as RAG engine
    participant V as ChromaDB
    participant G as Gemini

    U->>UI: Ask a news question
    UI->>R: Submit question and top-k setting
    R->>V: Search indexed article chunks
    V-->>R: Ranked hits and distances
    R->>R: Apply relevance threshold

    alt Relevant news found
        R->>G: Generate answer from numbered excerpts
        G-->>R: Cited grounded response
        R-->>UI: Answer, sources, distances, chunk counts
    else Evidence is insufficient
        R->>G: Generate fallback response without fabricated citations
        G-->>R: General-knowledge response
        R-->>UI: Answer and fallback metadata
    end

    UI-->>U: Chat response, source cards, retrieval graph, chunk graph
```

## Interface Tour

The workspace is organized around five visible surfaces:

1. **Hero workspace.** A concise explanation of the assistant’s routing behavior, live index size, retrieval mode, and top-k configuration.
2. **Session metrics.** Indexed chunks, conversation turns, latest relevant hits, and current answer mode.
3. **Chat environment.** Suggested investigations, answer-source badges, clickable source cards, and a persistent chat input.
4. **Retrieval inspection.** Interactive Plotly charts for relevance distance and supporting chunks per article.
5. **Control sidebar.** News refresh, topic filtering, full-text extraction, top-k, relevance threshold, fallback behavior, theme switching, and conversation reset.

## Project Structure

```text
NewsPilot/
├── app.py                 # Streamlit workspace and visualization layer
├── config.py              # Environment, model, chunking, and retrieval settings
├── news_fetcher.py        # RSS and NewsAPI ingestion
├── vector_store.py        # Chunking, embeddings, ChromaDB persistence, retrieval
├── rag_engine.py          # Relevance routing and Gemini answer generation
├── ingest.py              # Command-line news ingestion
├── ask.py                 # Command-line question answering
├── feeds.txt              # Custom RSS feed URLs
├── requirements.txt       # Python dependencies
├── runtime.txt            # Runtime declaration
└── data/
    └── chroma/            # Local persistent vector index, created at runtime
```

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/Samarssj/NewsPilot.git
cd NewsPilot
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
NEWSAPI_KEY=your_optional_newsapi_key
```

`NEWSAPI_KEY` is optional because the application can ingest from the configured RSS feeds. Keep `.env` private and do not commit credentials.

### 5. Launch the workspace

```bash
streamlit run app.py
```

Then open the local Streamlit URL shown in your terminal. Use **Refresh news index** in the sidebar before asking questions if the local collection is empty.

## Command-Line Usage

Fetch and index the latest news:

```bash
python ingest.py
```

Fetch without full-text extraction:

```bash
python ingest.py --no-fulltext
```

Fetch for a topic or custom feed file:

```bash
python ingest.py --query "artificial intelligence"
python ingest.py --feeds feeds.txt
```

Ask a question from the command line:

```bash
python ask.py "What are the latest developments in AI regulation?"
```

## Retrieval Controls

| Setting | Meaning |
| --- | --- |
| **Top-k** | Maximum number of distinct articles considered for a question. |
| **Relevance threshold** | Maximum semantic distance accepted as grounded evidence; lower values are stricter. |
| **Minimum relevant chunks** | Minimum number of threshold-passing results required for the news route. |
| **General-knowledge fallback** | Allows Gemini to answer when the local news index is not sufficiently relevant. |
| **Chunk size and overlap** | Controls how article text is segmented before embedding. |

## Answer Routing

| Retrieval condition | UI behavior | Source label |
| --- | --- | --- |
| Strong article matches | Generates an answer from numbered excerpts and displays citations. | **Grounded in live news** |
| No strong matches, fallback enabled | Generates a general response without pretending that uncited claims came from the news index. | **General knowledge fallback** |
| No strong matches, fallback disabled | Explains that the local context is insufficient. | **Strict live news** |

## Development Notes

ChromaDB persists the local collection under the configured `CHROMA_PATH`. Article content may come from full-text extraction or RSS summaries when extraction is unavailable. Paywalled or highly dynamic pages may only contribute their feed summary. Retrieval quality depends on index freshness, source quality, chunking parameters, and the configured embedding model.

The current interface stores the conversation and retrieval trace in Streamlit session state. Long-term user accounts, shared histories, scheduled ingestion, and cloud-hosted vector storage remain natural next steps for a production deployment.

## References

[1]: https://streamlit.io/ "Streamlit — build data apps in Python"
[2]: https://ai.google.dev/ "Google AI for Developers"
[3]: https://www.trychroma.com/ "Chroma — AI-native open-source embedding database"
[4]: https://www.sbert.net/ "Sentence Transformers documentation"
[5]: https://plotly.com/python/ "Plotly Python graphing library"
[6]: https://newsapi.org/ "NewsAPI documentation"
[7]: https://www.rssboard.org/rss-specification "RSS 2.0 Specification"

## License

This project is intended for educational, research, and portfolio use. Extend it responsibly, keep credentials private, and verify cited sources before making consequential decisions.
