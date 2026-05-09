# 🔬 Multi-Agent Research Assistant

An AI-powered research pipeline that takes a topic and autonomously searches the web, scrapes sources, writes a structured report, and critiques it — all in one run.

Built with **LangChain**, **GPT-4o mini**, and **Streamlit**.

---

## How it works

```
Your Topic
    │
    ▼
┌─────────────────────────────────┐
│  Stage 1 — Search Agent         │  Queries Tavily for top 5 results
│  tool: web_search               │  → titles, URLs, snippets
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│  Stage 2 — Reader Agent         │  Scrapes top 3 URLs
│  tool: scrape_url               │  → up to 3000 chars of clean text each
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│  Stage 3 — Writer Chain         │  Synthesises a structured report
│  (LLM, no tools)                │  Intro → Key Findings → Conclusion → Sources
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│  Stage 4 — Critic Chain         │  Reviews the report
│  (LLM, no tools)                │  Score /10 · Strengths · Areas to Improve
└─────────────────────────────────┘
```

---

## Project structure

```
├── main.py               # Streamlit UI
├── utils/
│   ├── agent.py          # Search agent, Reader agent, Writer chain, Critic chain
│   ├── pipeline.py       # Orchestrates all 4 stages in sequence
│   └── tools.py          # web_search (Tavily) and scrape_url (BeautifulSoup)
├── .env                  # API keys (not committed)
├── pyproject.toml        # uv-managed dependencies
└── README.md
```

---

## Setup

### Prerequisites
- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- OpenAI API key
- Tavily API key — free tier at [tavily.com](https://tavily.com)

### Install

```bash
git clone https://github.com/your-username/research-agent
cd research-agent
uv sync
```

### Environment variables

Create a `.env` file in the root:

```env
OPENAI_API_KEY=sk-...
TAVILY_API_KEY=tvly-...
```

### Run

```bash
uv run streamlit run main.py
```

App opens at `http://localhost:8501`

---

## Stack

| Layer | Library |
|---|---|
| LLM | `gpt-4o-mini` via `langchain-openai` |
| Agents | `langchain` AgentExecutor |
| Web search | `tavily-python` |
| Scraping | `requests` + `beautifulsoup4` |
| UI | `streamlit` |
| Env | `python-dotenv` |

---

## Output

Each run produces four sections displayed in the UI:

- **Research Report** — structured long-form write-up with sources
- **Critic Feedback** — score out of 10, strengths, and areas to improve
- **Raw Search Results** *(collapsible)* — titles, URLs, snippets from Tavily
- **Scraped Content** *(collapsible)* — full text pulled from source pages

---

## Notes

- Pipeline takes **30–90 seconds** depending on topic and scraping speed
- Some URLs may be blocked by paywalls or bot protection — the scraper skips them gracefully
- All results are session-scoped; nothing is persisted between runs