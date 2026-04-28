---
name: audit-model
description: Send a dbt model file path to the DE schema agent running in n8n for naming convention audit. Use when you want to audit a specific dbt SQL file (e.g. /audit-model models/marts/fct_orders.sql). Requires n8n to be running on localhost:5678.
allowed-tools: Bash(curl *)
---

Audit the dbt model file: `$ARGUMENTS`

Run this curl command to send the audit request to the n8n DE schema agent:

```bash
curl -s -X POST http://localhost:5678/webhook/data-agent \
  -H "Content-Type: application/json" \
  -d "{\"chatInput\": \"Read the file '$ARGUMENTS' from the kate_data_playground repository and audit it for naming convention errors.\", \"sessionId\": \"claude-audit-session\"}" | python -m json.tool
```

Then present the `output` field from the JSON response to the user in plain English, formatted as a readable audit report with:
- The file path that was audited
- Any naming convention errors found (as bullet points)
- Or a ✅ confirmation if no errors found

If curl fails (connection refused), remind the user to start n8n with: `docker compose up -d`
