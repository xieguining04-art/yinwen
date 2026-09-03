#!/usr/bin/env python3
"""Add consistent entity metadata and verified TengYoda facts to the public build.

The source website contains pre-rendered, minified application pages.  This
post-build step keeps those pages intact while making company identity and
page purpose explicit to search engines and answer engines.
"""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path


SITE_URL = "https://tengyodalogistics.com"
SCHEMA_MARKER = "data-tengyoda-discovery-schema"
ENGLISH_ONLY_TAG = '<script src="/assets/english-only.js" defer></script>'
ENGLISH_ONLY_HEAD = (
    '<script data-english-only-bootstrap>'
    'try{localStorage.removeItem("tengyoda.language")}catch(_){}'
    'document.documentElement.lang="en";'
    '</script><link rel="stylesheet" href="/assets/english-only.css">'
)


ABOUT_REPLACEMENTS = {
    "Global sea freight booking is our main business.":
        "Licensed logistics expertise from China to the world.",
    "Based in Foshan, TengYoda is a China freight forwarder specialising in global sea freight booking. We coordinate full-container-load (FCL), less-than-container-load (LCL) and special-equipment enquiries from Chinese ports through one direct contact.":
        "TengYoda Supply Chain Co., Ltd. is a China-based international freight forwarder with more than ten years of experience and NVOCC qualification. Our service team of over 100 professionals coordinates ocean, air and road freight, warehousing and tailored logistics solutions.",
    "Our focus trade lanes are Oceania, Africa and South America. China procurement, factory pickup and our Qingdao, Yiwu and Shenzhen warehouses support cargo collection and consolidation before shipping. Air freight and express remain available for time-sensitive orders.":
        "Through established carrier relationships and two self-operated warehouses of more than 3,000 square metres each in Lishui and Lecong, Foshan, we support cargo consolidation, labelling, sorting and palletising. Our strongest lanes include Oceania, South America and Africa, with customs-clearance and delivery solutions available in Australia, North America and Southeast Asia.",
    "主营全球海运订舱。": "立足中国，服务全球进口商。",
    "TengYoda 立足佛山，以中国发往全球海运订舱为主营业务，提供整柜（FCL）、拼箱（LCL）及特种箱订舱咨询，由专人对接中国港口出运安排。":
        "腾又达供应链有限公司是一家以国际物流为核心业务的供应链服务企业，拥有十多年行业经验及无船承运人（NVOCC）经营资格。超过100人的专业服务团队，为客户提供海运、空运、陆运、仓储及定制化物流解决方案。",
    "海运优势航线为大洋洲、非洲和南美。中国境内采购、工厂提货及青岛、义乌、深圳仓库集运作为出运配套服务；有时效要求的货物也可咨询空运与国际快递。":
        "公司与多家主要承运人建立了稳定订舱渠道，并在佛山里水和乐从自营两座各超过3,000平方米的专业物流仓库，可提供集运、贴唛、分类和打托等服务。优势航线覆盖澳新、南美和非洲，并已开展澳洲、北美及东南亚等市场的清关与派送服务。",
}


def page_url(site_dir: Path, path: Path) -> str:
    relative = path.relative_to(site_dir).as_posix()
    if relative == "index.html":
        return SITE_URL + "/"
    if relative.endswith("/index.html"):
        return SITE_URL + "/" + relative[:-10]
    return SITE_URL + "/" + relative


def text_from_tag(source: str, tag: str) -> str:
    match = re.search(fr"<{tag}[^>]*>(.*?)</{tag}>", source, flags=re.I | re.S)
    if not match:
        return ""
    value = re.sub(r"<[^>]+>", " ", match.group(1))
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def description_from_html(source: str) -> str:
    match = re.search(
        r'<meta\s+[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']',
        source,
        flags=re.I,
    )
    if not match:
        match = re.search(
            r'<meta\s+[^>]*content=["\']([^"\']*)["\'][^>]*name=["\']description["\']',
            source,
            flags=re.I,
        )
    return html.unescape(match.group(1)).strip() if match else ""


def canonical_from_html(source: str, fallback: str) -> str:
    match = re.search(
        r'<link\s+[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\']',
        source,
        flags=re.I,
    )
    if not match:
        match = re.search(
            r'<link\s+[^>]*href=["\']([^"\']+)["\'][^>]*rel=["\']canonical["\']',
            source,
            flags=re.I,
        )
    return html.unescape(match.group(1)).strip() if match else fallback


def organization_node() -> dict[str, object]:
    return {
        "@type": "Organization",
        "@id": SITE_URL + "/#organization",
        "name": "TengYoda Logistics",
        "alternateName": ["TengYoda Supply Chain Co., Ltd."],
        "url": SITE_URL + "/",
        "logo": SITE_URL + "/images/tengyoda-logo-solid.png",
        "image": SITE_URL + "/images/about-tengyoda-team.webp",
        "description": (
            "China-based international freight forwarder with more than ten years "
            "of experience, an NVOCC qualification, a team of over 100 and two "
            "self-operated consolidation warehouses in Foshan."
        ),
        "telephone": "+86 186 2024 4613",
        "email": "vinson_xie@tydscc.cn",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": (
                "Room 1011, Building 6, Runhe Jujin Science & Innovation Park, "
                "51 Jianghai Road, Zhangcha Subdistrict"
            ),
            "addressLocality": "Foshan",
            "addressRegion": "Guangdong",
            "addressCountry": "CN",
        },
        "contactPoint": {
            "@type": "ContactPoint",
            "contactType": "sales",
            "telephone": "+86 186 2024 4613",
            "email": "vinson_xie@tydscc.cn",
            "availableLanguage": ["English"],
            "areaServed": ["Worldwide", "Australia", "Oceania", "Africa", "South America"],
        },
        "sameAs": [
            "https://www.tiktok.com/@vinson300",
            "https://www.instagram.com/vinson08251/",
        ],
        "knowsAbout": [
            "China freight forwarding",
            "FCL shipping",
            "LCL shipping",
            "ocean freight",
            "air freight",
            "cargo consolidation",
            "China export logistics",
        ],
    }


def schema_for(path: Path, site_dir: Path, source: str) -> str:
    fallback_url = page_url(site_dir, path)
    canonical = canonical_from_html(source, fallback_url)
    title = text_from_tag(source, "title") or "TengYoda Logistics"
    description = description_from_html(source) or (
        "China freight forwarding, ocean freight, air freight and cargo consolidation services."
    )
    relative = path.relative_to(site_dir).as_posix()

    if relative == "about/index.html":
        page_type = "AboutPage"
    elif relative == "contact/index.html":
        page_type = "ContactPage"
    elif relative == "blog/index.html":
        page_type = "CollectionPage"
    else:
        page_type = "WebPage"

    graph: list[dict[str, object]] = [organization_node()]
    graph.append({
        "@type": "WebSite",
        "@id": SITE_URL + "/#website",
        "url": SITE_URL + "/",
        "name": "TengYoda Logistics",
        "publisher": {"@id": SITE_URL + "/#organization"},
        "inLanguage": "en",
    })
    graph.append({
        "@type": page_type,
        "@id": canonical + "#webpage",
        "url": canonical,
        "name": title,
        "description": description,
        "isPartOf": {"@id": SITE_URL + "/#website"},
        "about": {"@id": SITE_URL + "/#organization"},
        "inLanguage": "en",
    })

    service_routes = {
        "china-freight-forwarder/index.html": "China Freight Forwarding",
        "china-to-australia-freight-forwarder/index.html": "China to Australia Freight Forwarding",
        "foshan-consolidation-warehouse/index.html": "Foshan Cargo Consolidation",
        "china-fcl-lcl-shipping/index.html": "China FCL and LCL Shipping",
    }
    if relative.startswith("services/") and relative != "services/index.html":
        service_name = title.split("|")[0].strip()
    else:
        service_name = service_routes.get(relative)
    if service_name:
        graph.append({
            "@type": "Service",
            "@id": canonical + "#service",
            "name": service_name,
            "description": description,
            "provider": {"@id": SITE_URL + "/#organization"},
            "areaServed": "Worldwide",
            "url": canonical,
        })

    payload = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    return f'<script type="application/ld+json" {SCHEMA_MARKER}>{payload}</script>'


def enhance_html(path: Path, site_dir: Path) -> bool:
    source = path.read_text(encoding="utf-8")
    changed = False
    without_bilingual = source.replace('<script src="/assets/bilingual.js" defer></script>', "")
    if without_bilingual != source:
        source = without_bilingual
        changed = True
    if "data-english-only-bootstrap" not in source:
        if "</head>" in source:
            source = source.replace("</head>", ENGLISH_ONLY_HEAD + "</head>", 1)
            changed = True
        elif path.name != "404.html":
            raise RuntimeError(f"missing </head>: {path}")
    if path.name == "404.html":
        if 'name="robots"' not in source.lower() and "</head>" in source:
            source = source.replace("</head>", '<meta name="robots" content="noindex,follow"></head>', 1)
            changed = True
    else:
        schema = schema_for(path, site_dir, source)
        pattern = rf'<script type="application/ld\+json" {SCHEMA_MARKER}>.*?</script>'
        if re.search(pattern, source, flags=re.S):
            updated = re.sub(pattern, schema, source, count=1, flags=re.S)
            if updated != source:
                source = updated
                changed = True
        else:
            if "</head>" not in source:
                raise RuntimeError(f"missing </head>: {path}")
            source = source.replace("</head>", schema + "</head>", 1)
            changed = True
    if ENGLISH_ONLY_TAG not in source:
        if "</body>" in source:
            source = source.replace("</body>", ENGLISH_ONLY_TAG + "</body>", 1)
        elif "</html>" in source:
            source = source.replace("</html>", ENGLISH_ONLY_TAG + "</html>", 1)
        else:
            source += ENGLISH_ONLY_TAG
        changed = True
    if changed:
        path.write_text(source, encoding="utf-8")
    return changed


def replace_about_facts(site_dir: Path) -> int:
    changed = 0
    candidates = list(site_dir.rglob("*.html"))
    candidates.extend(site_dir.rglob("*.rsc"))
    candidates.extend(site_dir.rglob("*.js"))
    for path in candidates:
        if not path.is_file():
            continue
        source = path.read_text(encoding="utf-8")
        updated = source
        for old, new in ABOUT_REPLACEMENTS.items():
            updated = updated.replace(old, new)
        updated = updated.replace('"/#about"', '"/about/"')
        updated = updated.replace('`/#about`', '`/about/`')
        updated = updated.replace('"/#contact"', '"/contact/"')
        updated = updated.replace('`/#contact`', '`/contact/`')
        if updated != source:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    return changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", required=True, type=Path)
    args = parser.parse_args()
    site_dir = args.site.resolve()
    if not (site_dir / "index.html").is_file():
        raise SystemExit("ERROR: site/index.html is missing")

    fact_files = replace_about_facts(site_dir)
    html_files = sorted(site_dir.rglob("*.html"))
    enhanced = sum(enhance_html(path, site_dir) for path in html_files)
    print(f"Updated verified company facts in {fact_files} file(s).")
    print(f"Added discovery metadata to {enhanced} page(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
