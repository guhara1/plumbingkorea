#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sitemap.xml 자동 생성 + 전국 색인 보장 도구.

원칙(운영 지시): 전국 모든 지역 페이지는 반드시 색인(index)한다. noindex 금지.

동작:
  1) 사이트 루트의 모든 .html 파일을 스캔한다(404.html 제외).
  2) 각 페이지의 <meta name="robots">에 noindex가 있으면 오류로 중단한다.
     (전국 색인 정책 위반을 빌드 단계에서 차단)
  3) 모든 페이지를 sitemap.xml에 포함한다. 일부만 넣지 않는다.

사용:
  python3 tools/build_sitemap.py            # sitemap.xml 재생성
  python3 tools/build_sitemap.py --check    # 생성 없이 noindex/누락만 점검
"""
import os
import re
import sys
import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_URL = "https://plumbingkorea.pages.dev"
TODAY = datetime.date.today().isoformat()

# 스캔에서 제외할 디렉터리(자산/도구/빌드 산출물)
SKIP_DIRS = {"assets", "tools", ".git", "__pycache__", ".claude"}
# sitemap에 넣지 않는 파일(에러 페이지 등)
SKIP_FILES = {"404.html"}

NOINDEX_RE = re.compile(r'<meta[^>]+name=["\']robots["\'][^>]*content=["\'][^"\']*noindex',
                        re.IGNORECASE)


def url_for(rel_path):
    rel = rel_path.replace(os.sep, "/")
    if rel.endswith("index.html"):
        rel = rel[: -len("index.html")]
    return "/" + rel


def priority_for(url):
    """기존 사이트 우선순위 체계를 그대로 재현한다."""
    if url == "/":
        return "1.0"
    if url == "/contact.html":
        return "0.9"
    depth = url.strip("/").count("/")
    # 시·군·구(depth 2) 및 행정동·읍·면(depth 3+)
    if url.startswith("/area/") and depth >= 2:
        return "0.6"
    # 그 외(루트 문서, 서비스, 시·도 허브 등)
    return "0.8"


def collect_pages():
    pages = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if not fn.endswith(".html") or fn in SKIP_FILES:
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, ROOT)
            pages.append((rel, full))
    pages.sort(key=lambda x: url_for(x[0]))
    return pages


def main():
    check_only = "--check" in sys.argv
    pages = collect_pages()

    violations = []
    for rel, full in pages:
        with open(full, encoding="utf-8") as f:
            head = f.read(4000)  # robots 메타는 <head> 상단에 있음
        if NOINDEX_RE.search(head):
            violations.append(url_for(rel))

    if violations:
        print("✗ 전국 색인 정책 위반: 아래 페이지에 noindex가 있습니다.", file=sys.stderr)
        for v in violations:
            print("   noindex:", v, file=sys.stderr)
        sys.exit(1)

    print(f"✓ noindex 0건 — 전국 {len(pages):,}개 페이지 모두 색인 대상")

    if check_only:
        return

    rows = []
    for rel, _ in pages:
        url = url_for(rel)
        loc = BASE_URL + url
        rows.append(
            f"  <url><loc>{loc}</loc><lastmod>{TODAY}</lastmod>"
            f"<changefreq>monthly</changefreq><priority>{priority_for(url)}</priority></url>"
        )

    out = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(rows)
        + "\n</urlset>\n"
    )
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(out)
    print(f"✓ sitemap.xml 생성 완료 — {len(rows):,}개 URL (lastmod={TODAY})")


if __name__ == "__main__":
    main()
