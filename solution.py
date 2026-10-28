"""사용법: python solution.py "1,820"
보도자료데이터.json과 같은 폴더에 놓으세요. 표준 라이브러리만 사용합니다.
"""
import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIELDS = ["번호", "부처", "제목", "본문"]


def main():
    if len(sys.argv) != 2 or not sys.argv[1].strip():
        print('사용법: python solution.py "키워드"', file=sys.stderr)
        return 1
    keyword = sys.argv[1]
    # 경로 이탈 및 Windows 파일명 오류 방지. 검색어 자체는 바꾸지 않습니다.
    if any(c in keyword for c in '<>:"/\\|?*') or any(ord(c) < 32 for c in keyword):
        print('[ERROR] 파일명에 사용할 수 없는 문자가 포함된 키워드입니다.', file=sys.stderr)
        return 1
    try:
        text = (HERE / '보도자료데이터.json').read_text(encoding='utf-8-sig').strip()
        # 첨부 원본처럼 ```json 코드 블록으로 감싼 경우도 지원합니다.
        if text.startswith('```json\n') and text.endswith('```'):
            text = text[len('```json\n'):-3].strip()
        articles = json.loads(text)
        if not isinstance(articles, list) or not all(
            isinstance(a, dict) and all(isinstance(a.get(k), str) for k in FIELDS)
            for a in articles
        ):
            raise ValueError('데이터는 번호·부처·제목·본문 문자열을 가진 객체 배열이어야 합니다.')
        filtered = [a for a in articles if keyword in a['본문']]
        out = HERE / f'결과_{keyword}.csv'
        # UTF-8 BOM: Excel에서도 한글을 안정적으로 표시합니다.
        with out.open('w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(FIELDS)
            writer.writerows([[a[k] for k in FIELDS] for a in filtered])
    except (OSError, ValueError) as exc:
        print(f'[ERROR] {exc}', file=sys.stderr)
        return 1
    print(f'[OK] {len(filtered)}건 저장 → {out.name}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
