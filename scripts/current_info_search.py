#!/usr/bin/env python3
"""Search current information with the OpenAI Responses API."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request


API_URL = "https://api.openai.com/v1/responses"
DEFAULT_MODEL = "gpt-5.6-terra"


def build_request(query: str, model: str) -> dict:
    return {
        "model": model,
        "tools": [{"type": "web_search"}],
        "input": (
            "Search the live web before answering. Prefer primary sources. "
            "Include relevant publication or update dates, use inline citations, "
            "and distinguish confirmed facts from analysis or inference.\n\n"
            f"Question: {query}"
        ),
    }


def extract_text_and_sources(response: dict) -> tuple[str, list[tuple[str, str]]]:
    texts: list[str] = []
    sources: list[tuple[str, str]] = []
    seen_urls: set[str] = set()

    for item in response.get("output", []):
        if item.get("type") != "message":
            continue
        for content in item.get("content", []):
            if content.get("type") != "output_text":
                continue
            if content.get("text"):
                texts.append(content["text"])
            for annotation in content.get("annotations", []):
                if annotation.get("type") != "url_citation":
                    continue
                url = annotation.get("url")
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    sources.append((annotation.get("title") or url, url))

    return "\n\n".join(texts).strip(), sources


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify a freshness-sensitive question with OpenAI web search."
    )
    parser.add_argument("query", help="Question to verify with current web sources")
    parser.add_argument(
        "--model",
        default=os.getenv("CURRENT_INFO_MODEL", DEFAULT_MODEL),
        help=f"Responses API model (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the request body without making a network call",
    )
    args = parser.parse_args()
    payload = build_request(args.query, args.model)

    if args.dry_run:
        print(json.dumps(payload, indent=2))
        return 0

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print(
            "Current information could not be verified: OPENAI_API_KEY is not set.",
            file=sys.stderr,
        )
        return 2

    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=120) as result:
            response = json.load(result)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        print(
            f"Current information could not be verified: API error {exc.code}. "
            f"{detail}",
            file=sys.stderr,
        )
        return 3
    except (urllib.error.URLError, TimeoutError) as exc:
        print(
            f"Current information could not be verified: web search unavailable ({exc}).",
            file=sys.stderr,
        )
        return 4

    text, sources = extract_text_and_sources(response)
    if not text:
        print(
            "Current information could not be verified: the API returned no answer.",
            file=sys.stderr,
        )
        return 5

    print(text)
    if sources:
        print("\nSources:")
        for title, url in sources:
            print(f"- {title}: {url}")
    else:
        print(
            "\nConfidence: partial. No URL citations were returned; inspect the raw "
            "API response before relying on this answer.",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
