#!/usr/bin/env python3
"""Minimal Openverse API v1 client and connectivity check script.

Uses only the Python standard library to query Creative Commons images and audio
from https://api.openverse.org/v1/.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

BASE_URL = "https://api.openverse.org/v1"
USER_AGENT = "motion-designer-openverse-client/1.0"
VALID_MEDIA_TYPES = ("images", "audio")


def search_media(
    media_type: str,
    query: str,
    page_size: int = 3,
    license_type: str | None = None,
    timeout: float = 15.0,
) -> dict[str, Any]:
    """Search Openverse API v1 for `images` or `audio`."""
    if media_type not in VALID_MEDIA_TYPES:
        raise ValueError(f"media_type must be one of {VALID_MEDIA_TYPES}, got {media_type!r}")

    params: dict[str, str | int] = {"q": query, "page_size": page_size}
    if license_type:
        params["license"] = license_type

    url = f"{BASE_URL}/{media_type}/?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
        },
        method="GET",
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status = resp.status
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} for {url}: {body[:300]}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network error for {url}: {exc.reason}") from exc

    payload["_http_status"] = status
    payload["_request_url"] = url
    return payload


def run_check(query: str = "motion", page_size: int = 1) -> int:
    """Verify live connectivity to both images and audio Openverse endpoints."""
    for media_type in VALID_MEDIA_TYPES:
        data = search_media(media_type=media_type, query=query, page_size=page_size)
        results = data.get("results", [])
        first = results[0] if results else {}
        print(
            f"[OK] {media_type}: HTTP {data['_http_status']} | "
            f"result_count={data.get('result_count')} | "
            f"sample_title={first.get('title')!r} | "
            f"license={first.get('license')} | "
            f"url={first.get('url')}"
        )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Minimal Openverse API v1 client and live connectivity checker."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Run connectivity check against both images and audio endpoints.",
    )
    parser.add_argument(
        "--type",
        dest="media_type",
        choices=VALID_MEDIA_TYPES,
        default="images",
        help="Media type to search when not using --check (default: images).",
    )
    parser.add_argument(
        "--query",
        "-q",
        default="motion",
        help="Search query string (default: motion).",
    )
    parser.add_argument(
        "--limit",
        "-n",
        type=int,
        default=3,
        help="Number of results to fetch (default: 3).",
    )
    parser.add_argument(
        "--license",
        default=None,
        help="Optional Openverse license filter (e.g. cc0, by, by-sa).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print raw JSON response instead of summary lines.",
    )
    args = parser.parse_args(argv)

    try:
        if args.check:
            return run_check(query=args.query, page_size=max(1, args.limit))

        data = search_media(
            media_type=args.media_type,
            query=args.query,
            page_size=args.limit,
            license_type=args.license,
        )
        if args.json:
            print(json.dumps(data, indent=2))
            return 0

        print(
            f"Endpoint: {data['_request_url']} (HTTP {data['_http_status']}, "
            f"total={data.get('result_count')})"
        )
        for idx, item in enumerate(data.get("results", []), start=1):
            print(
                f"{idx}. [{item.get('license')}] {item.get('title')} "
                f"(by {item.get('creator')}) -> {item.get('url')}"
            )
        return 0
    except Exception as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
