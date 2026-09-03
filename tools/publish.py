#!/usr/bin/env python3
"""Generate TengYoda blog pages from repository Markdown files.

The script intentionally uses only Python's standard library so it can run on a
clean GitHub Actions runner without installing packages.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import urlparse


SITE_URL = "https://tengyodalogistics.com"
DEFAULT_COVER = "/images/sea-freight.webp"
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REQUIRED = ("title", "date", "summary", "category", "language")
MARKER_START = "<!-- MARKDOWN_POSTS_START -->"
MARKER_END = "<!-- MARKDOWN_POSTS_END -->"


class PublishError(RuntimeError):
    pass


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise PublishError(f"{path}: the first line must be ---")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration as exc:
        raise PublishError(f"{path}: front matter is missing its closing ---") from exc

    meta: dict[str, str] = {}
    for number, line in enumerate(lines[1:end], start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise PublishError(f"{path}:{number}: expected key: value")
        key, value = line.split(":", 1)
        key = key.strip().lower()
        value = value.strip().strip('"').strip("'")
        if not key or not value:
            raise PublishError(f"{path}:{number}: empty front-matter key or value")
        if key in meta:
            raise PublishError(f"{path}:{number}: duplicate field {key}")
        meta[key] = value

    missing = [key for key in REQUIRED if not meta.get(key)]
    if missing:
        raise PublishError(f"{path}: missing required fields: {', '.join(missing)}")
    return meta, "\n".join(lines[end + 1 :]).strip()


def safe_url(value: str, *, image: bool = False) -> str:
    value = value.strip()
    parsed = urlparse(value)
    if value.startswith("/") and not value.startswith("//"):
        return value
    if parsed.scheme == "https":
        return value
    if not image and parsed.scheme == "mailto":
        return value
    raise PublishError(f"unsafe or unsupported URL: {value}")


def render_inline(value: str) -> str:
    placeholders: list[str] = []

    def hold(fragment: str) -> str:
        placeholders.append(fragment)
        return f"\x00{len(placeholders) - 1}\x00"

    def code_replace(match: re.Match[str]) -> str:
        return hold(f"<code>{html.escape(match.group(1), quote=False)}</code>")

    value = re.sub(r"`([^`]+)`", code_replace, value)
    escaped = html.escape(value, quote=False)

    def image_replace(match: re.Match[str]) -> str:
        alt = html.escape(match.group(1), quote=True)
        url = html.escape(safe_url(html.unescape(match.group(2)), image=True), quote=True)
        return hold(f'<img src="{url}" alt="{alt}" loading="lazy">')

    def link_replace(match: re.Match[str]) -> str:
        label = match.group(1)
        url = html.escape(safe_url(html.unescape(match.group(2))), quote=True)
        external = ' target="_blank" rel="noopener noreferrer"' if url.startswith("https://") else ""
        return hold(f'<a href="{url}"{external}>{label}</a>')

    escaped = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", image_replace, escaped)
    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link_replace, escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", escaped)

    for index, fragment in enumerate(placeholders):
        escaped = escaped.replace(f"\x00{index}\x00", fragment)
    return escaped


def markdown_to_html(source: str) -> tuple[str, int]:
    lines = source.splitlines()
    output: list[str] = []
    paragraph: list[str] = []
    list_type: str | None = None
    quote: list[str] = []
    in_code = False
    code_lines: list[str] = []
    code_language = ""

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            output.append(f"<p>{render_inline(' '.join(x.strip() for x in paragraph))}</p>")
            paragraph = []

    def close_list() -> None:
        nonlocal list_type
        if list_type:
            output.append(f"</{list_type}>")
            list_type = None

    def flush_quote() -> None:
        nonlocal quote
        if quote:
            output.append(f"<blockquote><p>{render_inline(' '.join(quote))}</p></blockquote>")
            quote = []

    for line in lines + [""]:
        if line.startswith("```"):
            flush_paragraph()
            close_list()
            flush_quote()
            if in_code:
                language_class = f' class="language-{html.escape(code_language, quote=True)}"' if code_language else ""
                output.append(f"<pre><code{language_class}>{html.escape(chr(10).join(code_lines))}</code></pre>")
                code_lines = []
                code_language = ""
                in_code = False
            else:
                in_code = True
                code_language = line[3:].strip()
            continue
        if in_code:
            code_lines.append(line)
            continue

        stripped = line.strip()
        if not stripped:
            flush_paragraph()
            close_list()
            flush_quote()
            continue

        heading = re.match(r"^(#{1,3})\s+(.+)$", stripped)
        if heading:
            flush_paragraph()
            close_list()
            flush_quote()
            level = max(2, len(heading.group(1)))
            output.append(f"<h{level}>{render_inline(heading.group(2))}</h{level}>")
            continue
        if re.fullmatch(r"(?:---+|\*\*\*+)", stripped):
            flush_paragraph()
            close_list()
            flush_quote()
            output.append("<hr>")
            continue
        if stripped.startswith(">"):
            flush_paragraph()
            close_list()
            quote.append(stripped[1:].strip())
            continue

        unordered = re.match(r"^[-*+]\s+(.+)$", stripped)
        ordered = re.match(r"^\d+[.)]\s+(.+)$", stripped)
        if unordered or ordered:
            flush_paragraph()
            flush_quote()
            wanted = "ul" if unordered else "ol"
            if list_type != wanted:
                close_list()
                list_type = wanted
                output.append(f"<{wanted}>")
            match = unordered or ordered
            output.append(f"<li>{render_inline(match.group(1))}</li>")
            continue

        close_list()
        flush_quote()
        paragraph.append(stripped)

    if in_code:
        raise PublishError("unclosed fenced code block")
    plain_words = re.findall(r"[A-Za-z0-9]+|[\u3400-\u9fff]", source)
    return "\n".join(output), max(1, round(len(plain_words) / 260))


def validate_meta(path: Path, meta: dict[str, str], site_dir: Path) -> dict[str, object]:
    slug = path.stem
    if not SLUG_RE.fullmatch(slug):
        raise PublishError(f"{path}: filename must use lowercase English letters, numbers and hyphens")
    if len(meta["title"]) > 110:
        raise PublishError(f"{path}: title is longer than 110 characters")
    if len(meta["summary"]) > 240:
        raise PublishError(f"{path}: summary is longer than 240 characters")
    try:
        date = dt.date.fromisoformat(meta["date"])
    except ValueError as exc:
        raise PublishError(f"{path}: date must be YYYY-MM-DD") from exc
    language = meta["language"]
    if language != "en":
        raise PublishError(f"{path}: language must be en in the English-only website")
    cover = safe_url(meta.get("cover", DEFAULT_COVER), image=True)
    if cover.startswith("/") and not (site_dir / cover.lstrip("/")).is_file():
        raise PublishError(f"{path}: local cover image does not exist: {cover}")
    return {
        **meta,
        "slug": slug,
        "date_obj": date,
        "cover": cover,
        "description": meta.get("description", meta["summary"]),
        "author": meta.get("author", "TengYoda Logistics"),
        "keywords": meta.get("keywords", "China freight forwarding, international shipping, TengYoda"),
    }


def article_page(
    post: dict[str, object], body: str, minutes: int,
) -> str:
    title = html.escape(str(post["title"]))
    description = html.escape(str(post["description"]), quote=True)
    summary = html.escape(str(post["summary"]))
    category = html.escape(str(post["category"]))
    author = html.escape(str(post["author"]))
    keywords = html.escape(str(post["keywords"]), quote=True)
    cover = html.escape(str(post["cover"]), quote=True)
    slug = str(post["slug"])
    date = post["date_obj"]
    assert isinstance(date, dt.date)
    canonical = f"{SITE_URL}/blog/{slug}/"
    date_label = date.strftime("%d %b %Y")
    read_label = f"{minutes} min read"
    schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": str(post["title"]),
        "description": str(post["description"]),
        "image": str(post["cover"]) if str(post["cover"]).startswith("https://") else SITE_URL + str(post["cover"]),
        "datePublished": date.isoformat(),
        "dateModified": date.isoformat(),
        "inLanguage": "en",
        "author": {"@type": "Organization", "name": str(post["author"])},
        "publisher": {"@type": "Organization", "name": "TengYoda Logistics"},
        "mainEntityOfPage": canonical,
    }, ensure_ascii=False).replace("</", "<\\/")
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{title} | TengYoda</title>
  <meta name="description" content="{description}">
  <meta name="keywords" content="{keywords}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{cover}">
  <link rel="icon" href="/favicon.svg">
  <link rel="stylesheet" href="/assets/index-Ct9JYy3b.css">
  <style>
    :root{{--md-orange:#ff8700;--md-navy:#101820;--md-ink:#132238;--md-muted:#5f6b7a}}
    *{{box-sizing:border-box}}body{{margin:0;color:var(--md-ink);background:#f5f6f7;font-family:Arial,"Noto Sans SC",sans-serif;line-height:1.75}}
    .md-top{{background:#29282d;color:#fff;font-size:12px}}.md-top-inner,.md-nav-inner,.md-wrap{{width:min(1120px,calc(100% - 40px));margin:auto}}
    .md-top-inner{{padding:8px 0;display:flex;justify-content:flex-end;align-items:center;gap:18px}}.md-nav{{background:#111a25;color:#fff;border-bottom:1px solid rgba(255,255,255,.12)}}
    .md-nav-inner{{min-height:104px;display:flex;align-items:center;justify-content:space-between;gap:30px}}.md-brand{{flex:none;color:#fff;text-decoration:none;display:inline-flex}}.md-brand>span{{display:flex;flex-direction:column}}.md-brand strong{{color:#fff;letter-spacing:-.055em;font-size:37px;font-weight:800;line-height:1}}.md-brand-chevron{{color:var(--md-orange);vertical-align:-2px;margin-left:1px;font-size:48px;line-height:.55;display:inline-block}}.md-brand small{{color:#fff;letter-spacing:.17em;margin-top:9px;font-size:9px;font-weight:600}}
    .md-links{{display:flex;align-items:center;gap:34px}}.md-links a{{color:#fff;text-decoration:none;font-size:15px}}.md-links .md-action{{background:#5d6977;padding:14px 22px}}
    .md-hero{{position:relative;min-height:500px;color:#fff;display:flex;align-items:flex-end;background:#0d1824 center/cover no-repeat}}
    .md-hero:before{{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(8,17,27,.95),rgba(8,17,27,.78) 54%,rgba(8,17,27,.35))}}
    .md-hero-inner{{position:relative;width:min(920px,calc(100% - 40px));margin:0 auto;padding:82px 0 72px}}.md-kicker{{color:#ff9a16;font-size:13px;font-weight:700;letter-spacing:.12em;text-transform:uppercase}}
    .md-hero h1{{font-size:clamp(40px,6vw,72px);line-height:1.08;max-width:920px;margin:18px 0 24px;letter-spacing:-.03em}}
    .md-summary{{font-size:19px;max-width:760px;color:#e6ebf0}}.md-meta{{display:flex;gap:18px;flex-wrap:wrap;margin-top:24px;color:#d4dce5;font-size:14px}}
    .md-wrap{{display:grid;grid-template-columns:minmax(0,760px) 280px;gap:72px;padding:72px 0 88px}}
    .md-content{{background:#fff;padding:48px 54px;box-shadow:0 12px 40px rgba(16,24,32,.07)}}.md-content h2{{font-size:32px;line-height:1.25;margin:48px 0 18px;color:#102038}}
    .md-content h3{{font-size:23px;line-height:1.35;margin:36px 0 14px}}.md-content p,.md-content li{{font-size:17px}}.md-content ul,.md-content ol{{padding-left:24px}}
    .md-content blockquote{{border-left:4px solid var(--md-orange);margin:30px 0;padding:15px 24px;background:#fff7ed;color:#344154}}
    .md-content img{{max-width:100%;height:auto;margin:28px 0}}.md-content a{{color:#bf5b00}}.md-content pre{{overflow:auto;background:#0e1722;color:#f4f7fa;padding:20px}}
    .md-side{{align-self:start;position:sticky;top:24px;background:#111a25;color:#fff;padding:30px}}.md-side h2{{margin:0 0 14px;font-size:25px;line-height:1.25}}.md-side p{{color:#ced5dc;font-size:14px}}
    .md-side a{{display:block;background:var(--md-orange);color:#111;text-align:center;text-decoration:none;font-weight:700;padding:14px;margin-top:22px}}
    .md-back{{display:inline-block;margin-bottom:25px;color:#9c4a00;text-decoration:none;font-weight:700}}.md-footer{{background:#0d1620;color:#cbd3da;padding:38px 0}}
    .md-footer-inner{{width:min(1120px,calc(100% - 40px));margin:auto;display:flex;justify-content:space-between;gap:30px;flex-wrap:wrap}}.md-footer a{{color:#fff}}
    @media(max-width:800px){{.md-nav-inner{{min-height:84px}}.md-brand strong{{font-size:31px}}.md-brand-chevron{{font-size:42px}}.md-brand small{{font-size:8px}}.md-links a:not(.md-action){{display:none}}.md-wrap{{grid-template-columns:1fr;gap:28px;padding-top:38px}}.md-content{{padding:30px 24px}}.md-side{{position:static}}.md-hero{{min-height:430px}}}}
  </style>
  <script type="application/ld+json">{schema}</script>
</head>
<body>
  <div class="md-top"><div class="md-top-inner"><span>Call us +86 186 2024 4613</span></div></div>
  <header class="md-nav"><div class="md-nav-inner">
    <a class="md-brand" href="/" aria-label="TengYoda Logistics home"><span><strong>TengYoda<span class="md-brand-chevron" aria-hidden="true">›</span></strong><small>GLOBAL LOGISTICS</small></span></a>
    <nav class="md-links" aria-label="Main navigation"><a href="/about/">About Us</a><a href="/services/">Our Services</a><a href="/blog/">Blog</a><a href="/contact/">Contact Us</a><a class="md-action" href="https://wa.me/8618620244613">Speak to an expert →</a></nav>
  </div></header>
  <main>
    <section class="md-hero" style="background-image:url('{cover}')"><div class="md-hero-inner">
      <div class="md-kicker">{category}</div><h1>{title}</h1><p class="md-summary">{summary}</p>
      <div class="md-meta"><span>{date_label}</span><span>{read_label}</span><span>{author}</span></div>
    </div></section>
    <div class="md-wrap"><article class="md-content"><a class="md-back" href="/blog/">← Back to Blog</a>{body}</article>
      <aside class="md-side"><h2>Planning a shipment from China?</h2><p>Send us the cargo details and destination. We will help plan the China-side process.</p><a href="https://wa.me/8618620244613">Speak to Vinson →</a></aside>
    </div>
  </main>
  <footer class="md-footer"><div class="md-footer-inner"><strong>TengYoda Global Logistics</strong><span>vinson_xie@tydscc.cn · <a href="tel:+8618620244613">+86 186 2024 4613</a></span></div></footer>
</body></html>'''


def blog_section(posts: list[dict[str, object]]) -> str:
    cards: list[str] = []
    for post in posts:
        date = post["date_obj"]
        assert isinstance(date, dt.date)
        date_label = date.strftime("%d %b %Y")
        read_label = f"{post['minutes']} min read"
        cards.append(f'''<article class="md-index-card">
          <a class="md-index-cover" href="/blog/{post['slug']}/"><img src="{html.escape(str(post['cover']), quote=True)}" alt="" loading="lazy"></a>
          <div class="md-index-body"><div class="md-index-kicker">{html.escape(str(post['category']))}</div>
          <div class="md-index-meta">{date_label} · {read_label}</div>
          <h2><a href="/blog/{post['slug']}/">{html.escape(str(post['title']))}</a></h2>
          <p>{html.escape(str(post['summary']))}</p><a class="md-index-link" href="/blog/{post['slug']}/">Read article →</a></div>
        </article>''')
    return f'''{MARKER_START}<section class="md-posts" data-markdown-posts>
      <style>.md-posts{{padding:72px 0;background:#f5f6f7}}.md-posts-inner{{width:min(1320px,calc(100% - 40px));margin:auto}}.md-posts-title{{font-size:36px;color:#132238;margin:0 0 30px}}.md-posts-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:28px}}.md-index-card{{background:#fff;box-shadow:0 8px 28px rgba(16,24,32,.06)}}.md-index-cover{{display:block;aspect-ratio:16/9;overflow:hidden}}.md-index-cover img{{width:100%;height:100%;object-fit:cover;transition:transform .3s}}.md-index-card:hover img{{transform:scale(1.03)}}.md-index-body{{padding:26px}}.md-index-kicker{{color:#bf5b00;font-weight:700;font-size:12px;letter-spacing:.08em;text-transform:uppercase}}.md-index-meta{{font-size:12px;color:#6a7480;margin:10px 0}}.md-index-body h2{{font-size:24px;line-height:1.25;margin:12px 0}}.md-index-body h2 a{{color:#132238;text-decoration:none}}.md-index-body p{{color:#596575}}.md-index-link{{color:#ad5000;font-weight:700;text-decoration:none}}@media(max-width:900px){{.md-posts-grid{{grid-template-columns:1fr 1fr}}}}@media(max-width:620px){{.md-posts-grid{{grid-template-columns:1fr}}}}</style>
      <div class="md-posts-inner"><h2 class="md-posts-title">Latest Markdown articles</h2><div class="md-posts-grid">{''.join(cards)}</div></div>
    </section>{MARKER_END}'''


def update_blog_index(site_dir: Path, section: str) -> None:
    path = site_dir / "blog" / "index.html"
    source = path.read_text(encoding="utf-8")
    source = re.sub(re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END), "", source, flags=re.S)
    anchor = '<section class="blog-cta">'
    if anchor not in source:
        raise PublishError("could not find the blog CTA insertion point")
    source = source.replace(anchor, section + anchor, 1)
    recovery = json.dumps(section, ensure_ascii=False).replace("</", "<\\/")
    script = f'''<script data-markdown-recovery>(function(){{const h={recovery};function e(){{if(!document.querySelector('[data-markdown-posts]')){{const c=document.querySelector('.blog-cta');if(c)c.insertAdjacentHTML('beforebegin',h)}}}}window.addEventListener('load',e);[0,100,500,1500,3000].forEach(t=>setTimeout(e,t));}})();</script>'''
    source = re.sub(r"<script data-markdown-recovery>.*?</script>", "", source, flags=re.S)
    source += script
    path.write_text(source, encoding="utf-8")


def update_sitemap(site_dir: Path, posts: list[dict[str, object]]) -> None:
    path = site_dir / "sitemap.xml"
    source = path.read_text(encoding="utf-8")
    additions = []
    for post in posts:
        slug = str(post["slug"])
        if f"/blog/{slug}/" in source:
            continue
        date = post["date_obj"]
        assert isinstance(date, dt.date)
        additions.append(f"  <url><loc>{SITE_URL}/blog/{slug}/</loc><lastmod>{date.isoformat()}</lastmod></url>")
    if additions:
        source = source.replace("</urlset>", "\n".join(additions) + "\n</urlset>")
        path.write_text(source, encoding="utf-8")


def publish(site_dir: Path, articles_dir: Path) -> int:
    if not articles_dir.is_dir():
        print("No articles directory found; deploying the stable website unchanged.")
        return 0
    files = sorted(articles_dir.glob("*.md"))
    if not files:
        print("No Markdown articles found; deploying the stable website unchanged.")
        return 0

    posts: list[dict[str, object]] = []
    for path in files:
        meta, source = parse_frontmatter(path)
        post = validate_meta(path, meta, site_dir)
        if str(post["language"]) != "en":
            raise PublishError(f"{path}: English-only articles must use language: en")
        body, minutes = markdown_to_html(source)
        if not body:
            raise PublishError(f"{path}: article body is empty")
        post["minutes"] = minutes
        post["body"] = body
        posts.append(post)

    posts.sort(key=lambda item: (item["date_obj"], item["slug"]), reverse=True)
    for post in posts:
        destination = site_dir / "blog" / str(post["slug"])
        destination.mkdir(parents=True, exist_ok=True)
        (destination / "index.html").write_text(
            article_page(post, str(post["body"]), int(post["minutes"])),
            encoding="utf-8",
        )
        print(f"Published /blog/{post['slug']}/")
    update_blog_index(site_dir, blog_section(posts))
    update_sitemap(site_dir, posts)
    return len(posts)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", required=True, type=Path)
    parser.add_argument("--articles", required=True, type=Path)
    args = parser.parse_args()
    site_dir = args.site.resolve()
    if not (site_dir / "index.html").is_file() or not (site_dir / "blog" / "index.html").is_file():
        print("ERROR: the extracted stable website is incomplete", file=sys.stderr)
        return 2
    try:
        count = publish(site_dir, args.articles.resolve())
    except (PublishError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(f"Markdown publisher completed: {count} article(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
