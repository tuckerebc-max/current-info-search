# OpenAI Responses API examples

The default model is `gpt-5.6-terra`, selected for a balance of intelligence and cost. Set `CURRENT_INFO_MODEL` to override it.

## Python

The bundled script uses only the Python standard library:

```powershell
$env:OPENAI_API_KEY = "<your API key>"
python scripts/current_info_search.py "What changed in the OpenAI API this month?"
```

Preview the request without a key or network call:

```powershell
python scripts/current_info_search.py --dry-run "What changed in the OpenAI API this month?"
```

## curl

```bash
curl "https://api.openai.com/v1/responses" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-5.6-terra",
    "tools": [{"type": "web_search"}],
    "input": "Search the live web. Prefer primary sources, include relevant dates and inline citations, and distinguish confirmed facts from inference. Question: What changed in the OpenAI API this month?"
  }'
```

The response proves that web search ran when its `output` contains a completed `web_search_call`. The answer's `url_citation` annotations contain source titles and URLs. Do not claim that a search ran unless that evidence or the harness's corresponding tool trace is present.
