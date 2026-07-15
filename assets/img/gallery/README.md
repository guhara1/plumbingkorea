# 시공 갤러리 이미지 (21개 키워드 슬롯)

이 폴더의 SVG 파일은 각 키워드별 **이미지 자리(플레이스홀더)** 입니다.
메인 페이지와 모든 지역 페이지의 "시공 갤러리" 영역에 자동으로 노출됩니다.

## 실제 사진으로 교체하는 방법
1. 준비한 시공 사진을 **가로:세로 = 4:3 비율**(예: 1200×900)로 맞춥니다.
2. 아래 파일명과 **동일한 이름**으로 저장해 이 폴더의 SVG를 덮어씁니다.
   - 파일 형식을 사진(JPG/PNG)으로 바꾼 경우, 파일명을 알려주시면 코드의 확장자
     참조(`pages.py`의 `gallery_grid`)를 함께 변경해 드립니다. SVG 이름 그대로 두면
     추가 작업 없이 바로 반영됩니다.
3. 지역 페이지는 21장 중 6~8장이 지역별로 회전 노출되고, 메인 페이지에는 21장 전체가 노출됩니다.

## 키워드 ↔ 파일명 매핑
| 키워드 | 파일 |
|---|---|
| 누수탐지 | nusu-tamji.svg |
| 누수공사 | nusu-gongsa.svg |
| 하수구막힘 | hasugu-makim.svg |
| 배관막힘 | baegwan-makim.svg |
| 배관설비 | baegwan-seolbi.svg |
| 수전교체 | sujeon-gyoche.svg |
| 싱크대수전교체 | sink-sujeon.svg |
| 화장실수전교체 | hwajangsil-sujeon.svg |
| 변기막힘 | byeongi-makim.svg |
| 화장실변기교체 | byeongi-gyoche.svg |
| 변기부속품수리 | byeongi-busok.svg |
| 싱크대하수구막힘 | sink-hasugu.svg |
| 세면대막힘 | semyeondae-makim.svg |
| 세면대교체 | semyeondae-gyoche.svg |
| 배수구막힘 | baesugu-makim.svg |
| 배수구뚫음 | baesugu-ttuleum.svg |
| 욕실배관누수 | yoksil-nusu.svg |
| 수도누수 | sudo-nusu.svg |
| 수도수리 | sudo-suri.svg |
| 주방배관누수 | jubang-nusu.svg |
| 주방배수구막힘 | jubang-baesugu.svg |
