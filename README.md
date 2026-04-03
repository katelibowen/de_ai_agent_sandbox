# 🚀 Kate's Data Playground: Agentic dbt Auditor

An open-source **Agentic AI Framework** designed to automate dbt (data build tool) code audits. This project demonstrates how to bridge local LLMs (Ollama) with workflow automation (n8n) to create a "Data Auditor" that reads, analyzes, and reports on SQL models directly from GitHub.

---

## 🤖 What it Does
* Automated Code Review: Reads .sql files from GitHub and audits them against dbt naming conventions (e.g., ensuring marts models don't use stg_ prefixes).
* Local LLM Execution: Uses Llama 3.2:1b running locally inside Docker—ensuring your code never leaves your infrastructure.
* Agentic Logic: The n8n AI Agent autonomously decides when to fetch a file via the GitHub API based on your natural language prompts.

---

## 🛠️ System Architecture
1. Python Client: Sends a request to the n8n Webhook.
2. n8n AI Agent: Evaluates the request and triggers the GitHub Tool.
3. Ollama: Provides the LLM reasoning to "audit" the SQL text returned from GitHub.
4. Output: A formatted audit report returned to the user via terminal or API.

---

## ⚙️ Step-by-Step Setup Guide

### 1. Launch the Docker Stack
This command starts the n8n "Brain" and the Ollama "Muscle" in a private, shared network.

    docker-compose up -d

Verify: Run 'docker ps'. You should see 'n8n_data_agent' and 'ollama_service' both showing as "Up".

### 2. Initialize the AI Model
By default, the Ollama container is an empty shell. You must "pull" the model into the container's internal storage to enable the reasoning engine:

    docker exec -it ollama_service ollama pull llama3.2:1b

> [!NOTE]
> This is a ~1.3GB download. Once it reaches 100%, the AI is live and ready for inference.

### 3. Configure the n8n Workflow
1. Open n8n: Navigate to http://localhost:5678 in your browser.
2. Import: Go to Settings > Import from File and select the .json workflow from the /n8n directory.
3. GitHub Connection:
    * Open the GitHub Node.
    * Click "Add Credential" and paste your GitHub Personal Access Token (PAT).
    * Ensure the Repository Name is set to kate_data_playground.
4. Ollama Connection:
    * Open the Ollama Chat Model node.
    * Set the Base URL to http://ollama_service:11434. (Docker uses service names for internal DNS).

### 4. Run the test
Trigger the agent using the provided Python wrapper script:

    python scripts/ask_agent.py

---

## 📂 Project Structure
* /dbt: Sample dbt models used for auditing.
* /n8n: Exported workflow JSON files.
* /scripts: Python client wrappers (ask_agent.py).
* docker-compose.yaml: The master orchestration file.
* .gitignore: Configured to protect your local AI weights and n8n database.

---

**Maintainer:** Kate | Senior Data Engineer  
**Status:** Active Development (Targeting Staff/Senior Role May 2026)
