#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
색인 즉시 통보 통합 실행기 — 글을 올리거나 페이지를 바꿀 때 한 번만 실행.

  python3 tools/notify_all.py                      # sitemap 전체를 IndexNow로 통보(+SA 있으면 구글까지)
  python3 tools/notify_all.py /area/seoul/ /price.html   # 특정 URL만 통보
  python3 tools/notify_all.py --google              # 구글 Indexing API도 함께(서비스계정 필요)

동작:
  1) IndexNow  → Bing · Naver · Yandex · Seznam 즉시 통보 (항상 실행)
  2) Google Indexing API → tools/google_sa.json 이 있고 --google 지정 시 실행
     (구글은 IndexNow 미참여라 별도 통보. 일일 쿼터 200건)

※ 사이트가 배포되어 IndexNow 키 파일( /<KEY>.txt )이 공개 접근 가능해야 합니다.
※ 구글/빙의 옛 'sitemap ping(GET .../ping?sitemap=)'은 2023년 폐지되어 더 이상 동작하지
   않습니다. 대신 ① IndexNow ② Google Indexing API ③ Search Console·네이버 서치어드바이저
   사이트맵 제출이 현재 유효한 가장 빠른 색인 경로입니다.
"""
import sys, os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))

def run(script, args):
    print(f"\n▶ {script} {' '.join(args)}")
    return subprocess.call([sys.executable, os.path.join(HERE, script)] + args)

def main():
    raw = sys.argv[1:]
    do_google = "--google" in raw
    url_args = [a for a in raw if not a.startswith("--")]

    # 1) IndexNow (Bing·Naver·Yandex·Seznam)
    run("indexnow.py", url_args)

    # 2) Google Indexing API (선택)
    sa = os.path.join(HERE, "google_sa.json")
    if do_google or os.path.exists(sa):
        if os.path.exists(sa):
            g_args = url_args if url_args else ["--from-sitemap"]
            run("google_index.py", g_args)
        else:
            print("\n(구글) tools/google_sa.json 이 없어 건너뜀 — README의 Indexing API 설정 참고")

    print("\n완료: IndexNow 통보됨." + ("  구글 Indexing API 통보 시도됨." if (do_google or os.path.exists(sa)) else ""))

if __name__ == "__main__":
    main()
