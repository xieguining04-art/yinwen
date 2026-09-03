#!/usr/bin/env python3
"""Build maintainable importer landing pages from Markdown."""

from __future__ import annotations

import argparse
import datetime as dt
import html
from pathlib import Path

from publish import PublishError, markdown_to_html, parse_frontmatter, validate_meta


SITE_URL = "https://tengyodalogistics.com"


def page_template(post: dict[str, object], body: str) -> str:
    slug = str(post["slug"])
    title = html.escape(str(post["title"]))
    description = html.escape(str(post["description"]), quote=True)
    summary = html.escape(str(post["summary"]))
    category = html.escape(str(post["category"]))
    keywords = html.escape(str(post["keywords"]), quote=True)
    cover = html.escape(str(post["cover"]), quote=True)
    canonical = f"{SITE_URL}/{slug}/"
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{title} | TengYoda Logistics</title>
  <meta name="description" content="{description}">
  <meta name="keywords" content="{keywords}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{SITE_URL}{cover}">
  <link rel="icon" href="/favicon.svg">
  <link rel="stylesheet" href="/assets/discovery.css">
  <link rel="stylesheet" href="/assets/logo-unified.css">
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to main content</a>
  <div class="topbar"><div class="shell"><span>China origin logistics for global importers</span><div class="topbar-actions"><a href="tel:+8618620244613">+86 186 2024 4613</a></div></div></div>
  <header class="header"><div class="shell nav-wrap">
    <a class="ty-brand" href="/" aria-label="TengYoda Logistics home"><span><strong>TengYoda<span class="ty-brand-chevron" aria-hidden="true">›</span></strong><small>GLOBAL LOGISTICS</small></span></a>
    <nav aria-label="Main navigation"><a href="/about/">About</a><a href="/services/">Services</a><a href="/blog/">Importer Guides</a><a href="/contact/">Contact</a></nav>
    <a class="nav-cta" href="https://wa.me/8618620244613">Request a shipping plan</a>
  </div></header>
  <main id="main-content">
    <section class="hero"><img class="hero-image" src="{cover}" alt="" fetchpriority="high"><div class="hero-overlay"></div><div class="shell hero-content">
      <span class="eyebrow">{category}</span><h1>{title}</h1><p>{summary}</p>
      <div class="hero-actions"><a class="button primary" href="https://wa.me/8618620244613">Discuss your shipment</a><a class="button ghost" href="/services/">View services</a></div>
    </div></section>
    <div class="shell content-grid">
      <article class="prose">{body}</article>
      <aside class="proof" aria-label="TengYoda company facts">
        <span class="eyebrow">VERIFIABLE COMPANY FACTS</span>
        <h2>One China-side team</h2>
        <dl>
          <div><dt>Experience</dt><dd>More than 10 years</dd></div>
          <div><dt>Team</dt><dd>Over 100 service professionals</dd></div>
          <div><dt>Qualification</dt><dd>NVOCC-qualified operator</dd></div>
          <div><dt>Foshan warehouses</dt><dd>Lishui and Lecong, each over 3,000 m²</dd></div>
          <div><dt>Focus lanes</dt><dd>Oceania, Africa and South America</dd></div>
        </dl>
        <a class="proof-link" href="/about/">Review our company profile →</a>
      </aside>
    </div>
    <section class="closing"><div class="shell closing-inner"><div><span class="eyebrow">FROM CARGO DETAILS TO A SHIPPING PLAN</span><h2>Tell us what you are importing.</h2><p>Send the product, package count, packed dimensions, gross weight, pickup city, destination and cargo-ready date.</p></div><div class="closing-actions"><a class="button primary" href="https://wa.me/8618620244613">WhatsApp Vinson</a><a class="button ghost" href="mailto:vinson_xie@tydscc.cn">Email TengYoda</a></div></div></section>
  </main>
  <footer><div class="shell footer-grid"><div><strong>TengYoda Logistics</strong><p>China freight forwarding, consolidation and international shipping coordination.</p></div><div><a href="/about/">About</a><a href="/services/">Services</a><a href="/blog/">Blog</a></div><div><a href="mailto:vinson_xie@tydscc.cn">vinson_xie@tydscc.cn</a><a href="tel:+8618620244613">+86 186 2024 4613</a></div></div></footer>
</body>
</html>'''


def update_sitemap(site_dir: Path, posts: list[dict[str, object]]) -> None:
    path = site_dir / "sitemap.xml"
    source = path.read_text(encoding="utf-8")
    additions: list[str] = []
    for post in posts:
        route = f"/{post['slug']}/"
        if route in source:
            continue
        date = post["date_obj"]
        assert isinstance(date, dt.date)
        additions.append(f"  <url><loc>{SITE_URL}{route}</loc><lastmod>{date.isoformat()}</lastmod></url>")
    if additions:
        source = source.replace("</urlset>", "\n".join(additions) + "\n</urlset>")
        path.write_text(source, encoding="utf-8")


def publish(site_dir: Path, pages_dir: Path) -> int:
    if not pages_dir.is_dir():
        print("No pages directory found.")
        return 0
    posts: list[dict[str, object]] = []
    for path in sorted(pages_dir.glob("*.md")):
        meta, source = parse_frontmatter(path)
        post = validate_meta(path, meta, site_dir)
        if str(post["language"]) != "en":
            raise PublishError(f"{path}: importer landing pages must use language: en")
        body, _ = markdown_to_html(source)
        if not body:
            raise PublishError(f"{path}: page body is empty")
        destination = site_dir / str(post["slug"])
        destination.mkdir(parents=True, exist_ok=True)
        (destination / "index.html").write_text(page_template(post, body), encoding="utf-8")
        posts.append(post)
        print(f"Published /{post['slug']}/")
    update_sitemap(site_dir, posts)
    return len(posts)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", required=True, type=Path)
    parser.add_argument("--pages", required=True, type=Path)
    args = parser.parse_args()
    try:
        count = publish(args.site.resolve(), args.pages.resolve())
    except (PublishError, OSError) as exc:
        print(f"ERROR: {exc}")
        return 2
    print(f"Landing-page publisher completed: {count} page(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
