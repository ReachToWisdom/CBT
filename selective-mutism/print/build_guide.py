# README.md -> guide.html (인쇄용). 이후 `node render.js`로 PDF 생성. 필요: pip install markdown
import markdown, re, pathlib
here = pathlib.Path(__file__).parent
src = (here / '../README.md').read_text(encoding='utf-8')
src = re.sub(r'함께 제공되는 \[`practice.html`\].*?PDF 다시 만들기:[^\n]*\n',
             '함께 제공되는 **연습 기록지(worksheets.pdf)** 에 직접 적으며 진행하세요. 예시 과제 300개는 기록지 부록에 있습니다.\n', src, flags=re.S)
src = re.sub(r'([^\n])\n(- |1\. )', r'\1\n\n\2', src)  # python-markdown은 목록 앞에 빈 줄이 필요
html = markdown.markdown(src, extensions=['tables', 'fenced_code'])
(here / 'guide.html').write_text(f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>선택적 함묵증 자가 실행 안내서</title><link rel="stylesheet" href="print.css"></head><body>{html}</body></html>', encoding='utf-8')
