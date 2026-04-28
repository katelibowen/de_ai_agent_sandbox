---
name: n8n-logs
description: Tail the n8n Docker container logs to debug workflow execution issues, see agent responses, or check for errors. Use when the agent is behaving unexpectedly or a workflow is failing.
allowed-tools: Bash(docker *)
---

Show the last 50 lines of n8n logs and watch for new output:

```bash
docker logs n8n_data_agent --tail 50 2>&1
```

If the user wants to follow logs in real time, note that live tailing isn't interactive here — suggest they run this in a terminal:

```
docker logs n8n_data_agent --tail 50 -f
```

After showing logs, summarize:
- Any ERROR or WARN lines
- Recent workflow executions (look for `Workflow executed` or `execution` entries)
- Any tool call activity from the AI agent node
- Connection issues to Ollama (look for `ECONNREFUSED` to port 11434)
