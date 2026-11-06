#!/usr/bin/env python3
"""PS-0208: independently observe the public Pages output; no credentials."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import time
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
BASE = "https://endeavoreverlasting.github.io/TokenCorridor-prompt-kit-site/"
PATHS = {
    "": "index.html",
    "moonwake/": "moonwake/index.html",
    "prompt-library/index.html": "prompt-library/index.html",
    "assets/moonwake-mark.svg": "assets/moonwake-mark.svg",
    "assets/moonwake-mark-512-impeccable.png": "assets/moonwake-mark-512-impeccable.png",
    "moonwake/assets/moonwake-mark.svg": "moonwake/assets/moonwake-mark.svg",
}

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def probe_once(revision: str) -> None:
    for route, local in PATHS.items():
        u = urllib.parse.urljoin(BASE, route)
        # Cache-bust by expected commit without exposing any private source.
        u += ("?" if "?" not in u else "&") + urllib.parse.urlencode({"revision": revision})
        with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent":"Moonwake-PS-0208-Public-Smoke/1.0"}), timeout=14) as reply:
            body = reply.read(16_000_000)
            if reply.status != 200:
                raise ValueError(f"HTTP {reply.status} at {route!r}")
        expected = (ROOT/local).read_bytes()
        if digest(body) != digest(expected):
            raise ValueError(f"PUBLIC_CDN_REVISION_MISMATCH at {route!r}; expected exact source content")
    root = (ROOT/"index.html").read_text(encoding="utf-8")
    if '<h1 id="hero-title">Moonwake</h1>' not in root:
        raise ValueError("ROOT_BRAND_NOT_MOONWAKE")
    if "prompt-library/index.html" not in root:
        raise ValueError("ROOT_PROMPT_LIBRARY_ROUTE_MISSING")

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--revision", required=True)
    p.add_argument("--attempts", type=int, default=24)
    p.add_argument("--delay", type=int, default=10)
    args = p.parse_args()
    for attempt in range(1, args.attempts + 1):
        try:
            probe_once(args.revision)
        except (OSError, ValueError) as exc:
            # Status is bounded, never serialize HTTP response or repository source.
            print(f"PENDING {attempt}/{args.attempts}: {type(exc).__name__}: {str(exc)[:150]}", flush=True)
            if attempt < args.attempts:
                time.sleep(args.delay)
        else:
            print("PASS PUBLIC_HTTP_ROOT_LIBRARY_R3_ASSET_PARITY "+BASE,flush=True)
            return 0
    print("FAIL PUBLIC_HTTP_RELEASE_NOT_OBSERVED",flush=True)
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
