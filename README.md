# 🚀 Agentic dbt Auditor

An open-source **agentic AI framework** for automated dbt code review using local LLMs. The agent reads SQL models from GitHub, audits them against dbt naming conventions and layering rules, and returns a formatted report — all without your code leaving your infrastructure.

Built as a sandbox to prototype agentic patterns, local LLM inference, and AI-assisted data engineering workflows.

---

## 🤖 What it Does

- **Automated Code Review**: Reads `.sql` files from GitHub and audits them against dbt conventions (e.g., flags marts models using `stg_` prefixes, catches sources referenced outside staging).
- **Local LLM Execution**: Runs Llama 3.2:1b inside Docker via Ollama — code never leaves local infrastructure.
- **Agentic Orchestration**: The n8n AI Agent autonomously decides when to fetch a file via the GitHub API based on natural-language prompts.

---

## 🧪 Example Output

    Input: "Audit the model marts/fct_orders.sql"

    Agent:
      → Calling GitHub tool to fetch marts/fct_orders.sql
      → Analyzing against dbt conventions...

    Audit Report
    ============
    ✅ Naming: 'fct_' prefix correctly indicates a fact table in marts layer.
    ⚠️  Layering: Model references `raw.orders` directly — marts should depend on
        intermediate or staging models, not raw sources.
    ⚠️  Materialization: No materialization config found — fact tables in marts
        are typically materialized as `table` or `incremental`.
    ✅ SQL style: Uses CTEs, no SELECT *.

    Severity: 2 warnings, 0 errors.

---

## 🛠️ System Architecture

    ┌─────────────┐     ┌───────────────┐     ┌─────────────┐
    │   Python    │────▶│   n8n Agent   │────▶│   GitHub    │
    │   Client    │     │ (Orchestrator)│     │   (Source)  │
    └─────────────┘     └───────┬───────┘     └─────────────┘
                                │
                                ▼
                        ┌─────────────┐
                        │   Ollama    │
                        │ (Llama 3.2) │
                        └─────────────┘

1. **Python Client** sends a request to the n8n webhook.
2. **n8n AI Agent** evaluates the request and decides whether to invoke the GitHub tool.
3. **Ollama** provides local LLM reasoning to audit the SQL.
4. **Output**: A formatted audit report returned via terminal or API.

---

## 💡 Design Decisions

- **Local LLM (Llama 3.2:1b) over OpenAI API**: Code privacy is non-negotiable for code-review tooling — nothing leaves the local infrastructure. Also gives reproducible behavior and zero API cost during iteration.
- **n8n over building in Python directly**: Wanted to evaluate a low-code agent orchestrator end-to-end. Trade-off: faster iteration on agent logic, but less programmatic control than LangChain/LangGraph. For production I'd reach for the latter.
- **dbt audits over generic SQL linting**: dbt has opinionated conventions — naming prefixes, layer dependencies, materialization patterns — that aren't well-covered by tools like sqlfluff. The agent applies semantic rules a linter can't.
- **Llama 3.2:1b over larger models**: Small enough to run on a laptop, large enough to follow structured audit instructions. Bigger models would catch more nuance, but the goal here was to prove the architecture, not maximize accuracy.

---

## ⚙️ Setup

### 1. Launch the Docker stack

```
docker-compose up -d
```

Verify with `docker ps` — you should see `n8n_data_agent` and `ollama_service` both `Up`.

### 2. Pull the LLM into Ollama

```
docker exec -it ollama_service ollama pull llama3.2:1b
```

(~1.3GB download.)

### 3. Configure the n8n workflow

1. Open n8n at `http://localhost:5678`
2. Settings → Import from File → select the `.json` workflow from `/n8n/workflows`
3. **GitHub credential**: add your Personal Access Token; set repository name
4. **Ollama connection**: set Base URL to `http://ollama_service:11434`

### 4. Run

```
python scripts/ask_agent.py
```

---

## 📂 Project Structure

    .
    ├── dbt/                  # Sample dbt models for auditing (clean + intentionally broken)
    ├── n8n/workflows/        # Exported n8n workflow JSON
    ├── scripts/              # Python client (ask_agent.py)
    ├── docker-compose.yml    # Orchestration for n8n + Ollama
    └── README.md

---

## 🗺️ Roadmap

- [ ] Replace hardcoded prompt rules with a RAG-based knowledge base (markdown rules → Chroma → retrieval at audit time)
- [ ] Add evaluation suite: clean vs. broken model fixtures with accuracy scoring
- [ ] Add GitHub Action to run the auditor automatically on PRs
- [ ] Support custom rule packs per project

---

**Status:** Active development.
