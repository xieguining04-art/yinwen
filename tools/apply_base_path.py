#!/usr/bin/env python3
"""Make the static site work at either a GitHub project path or a custom domain.

GitHub Pages serves a project repository below ``/<repository>/`` until a
custom domain is configured.  The source site intentionally keeps root-based
URLs for its final production domain.  This build step prefixes only known
internal routes and assets with the base path reported by configure-pages.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


TEXT_SUFFIXES = {".html", ".rsc", ".js", ".css"}

# These are public site routes or asset locations. Keeping the allow-list
# explicit prevents accidental edits to external URLs and framework internals.
PUBLIC_ROOTS = (
    "assets",
    "images",
    "article-images",
    "about",
    "contact",
    "services",
    "blog",
    "china-australia.html",
    "china-australia-shipping-cost.html",
    "china-australia-shipping-time.html",
    "ddp-shipping-china-australia.html",
    "fcl-vs-lcl-china-australia.html",
    "china-fcl-lcl-shipping",
    "china-freight-forwarder",
    "china-to-australia-freight-forwarder",
    "foshan-consolidation-warehouse",
    "favicon.svg",
    "robots.txt",
    "sitemap.xml",
)


def normalize_base_path(value: str) -> str:
    value = value.strip()
    if not value or value == "/":
        return ""
    if not value.startswith("/"):
        value = "/" + value
    return value.rstrip("/")


def prefix_known_urls(source: str, base_path: str) -> str:
    roots = "|".join(re.escape(root) for root in PUBLIC_ROOTS)
    # Do not match a slash inside https://example.com/... or an already
    # prefixed URL. Known internal paths may be followed by /, ?, # or a quote.
    pattern = re.compile(
        rf"(?<![A-Za-z0-9_:/.-])/(?=(?:{roots})(?:[/#?]|[\\\"'`<>)\\s]|$))"
    )
    updated = pattern.sub(base_path + "/", source)

    # Home links are the only intentionally exact-root URLs we rewrite. These
    # variants cover normal HTML plus the escaped RSC payload embedded in it.
    replacements = {
        'href="/"': f'href="{base_path}/"',
        "href='/'": f"href='{base_path}/'",
        '"href":"/"': f'"href":"{base_path}/"',
        r'\"href\":\"/\"': rf'\"href\":\"{base_path}/\"',
        'href:`/`': f'href:`{base_path}/`',
    }
    for old, new in replacements.items():
        updated = updated.replace(old, new)
    return updated


def apply_base_path(site_dir: Path, base_path: str) -> tuple[int, int]:
    if not base_path:
        return 0, 0
    scanned = 0
    changed = 0
    for path in sorted(site_dir.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        scanned += 1
        source = path.read_text(encoding="utf-8")
        updated = prefix_known_urls(source, base_path)
        if updated != source:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    return scanned, changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", required=True, type=Path)
    parser.add_argument("--base-path", default="")
    args = parser.parse_args()

    site_dir = args.site.resolve()
    if not (site_dir / "index.html").is_file():
        raise SystemExit("ERROR: site/index.html is missing")

    base_path = normalize_base_path(args.base_path)
    scanned, changed = apply_base_path(site_dir, base_path)
    if base_path:
        print(
            f"Applied GitHub Pages base path {base_path!r} to "
            f"{changed} of {scanned} text files."
        )
    else:
        print("Custom-domain root detected; no base-path rewrite was needed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
