---
name: check-agent
description: Check if the n8n DE schema agent is running and responsive. Use when you want to verify the agent is up before sending audit requests, or when troubleshooting connection issues.
allowed-tools: Bash(curl *) Bash(docker *)
---

Check the status of the n8n DE schema agent:

1. **Check Docker containers are running:**

```bash
docker compose -f c:/Users/hp/kate-agentic-stack/docker-compose.yml ps
```

2. **Ping the n8n webhook to confirm it responds:**

```bash
curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:5678/webhook/data-agent \
  -H "Content-Type: application/json" \
  -d '{"chatInput": "hello", "sessionId": "health-check"}'
```

Report back:
- If Docker containers show `Up` — services are running
- If HTTP status is `200` — agent is accepting requests
- If connection refused — tell user to run: `docker compose up -d` from `c:/Users/hp/kate-agentic-stack/`
- If HTTP status is `404` — n8n is running but the workflow may be inactive; tell user to activate the workflow in n8n UI at http://localhost:5678
