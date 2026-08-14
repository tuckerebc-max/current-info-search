---
name: current-info-search
description: Verify recent, current, or fast-changing information with live web search instead of model memory. Invoke automatically for breaking news, AI model releases, pricing, APIs, documentation, product or company announcements, software versions, regulations, policies, schedules, current officeholders, or any fact that may have changed; also invoke whenever the user asks to search, look up, find the latest, verify, or check current information.
---

# Current Info Search

Use live web search whenever freshness can materially affect the answer. Do not answer a current-fact question solely from training data, cached knowledge, or an earlier search.

## Workflow

1. Identify the claims whose truth may have changed.
2. Search the web with the harness's native web-search tool when available.
3. Prefer primary sources: official documentation, government and regulator sites, standards bodies, vendor documentation, filings, and original announcements.
4. Check publication or update dates and whether each source describes the event directly.
5. Cross-check consequential claims with a second authoritative source when practical.
6. Answer with citations placed next to the claims they support.

If the harness has no native web-search tool, use `scripts/current_info_search.py`. It calls the OpenAI Responses API with `web_search`, defaults to `gpt-5.6-terra`, and reads `OPENAI_API_KEY`. Read `references/api-examples.md` for Python and curl usage.

## Evidence Rules

- Include publication or update dates when available and relevant.
- Link to original primary sources whenever possible.
- Distinguish confirmed facts from analysis, interpretation, and inference.
- Say when a date refers to publication rather than the underlying event.
- Prefer current search evidence over conflicting internal knowledge.
- When authoritative sources disagree, describe the disagreement and attribute each position.
- Never fabricate a citation, date, quotation, search result, or claim that a search occurred.

## Failure Behavior

- If web search is unavailable, state: "I could not verify this with current web sources."
- Do not silently fall back to memory for a freshness-dependent answer.
- If evidence is partial, say what is confirmed, what remains uncertain, and the confidence level.
- If authentication fails, identify the missing or rejected credential without exposing its value.

## Search Discipline

- Search only when freshness is materially important or the user explicitly requests it.
- Use narrow queries and open the supporting pages; do not rely only on search-result snippets.
- For OpenAI product or API questions, prefer official OpenAI documentation.
- For private workspace facts, prefer an authorized connector over the public web.
