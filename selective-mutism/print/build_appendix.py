# practice.html의 예시 과제 -> worksheets.html 부록 페이지 (난이도·상황 쉬운 순). 이후 `node render.js`
import re, ast, pathlib
here = pathlib.Path(__file__).parent
src = (here / '../practice.html').read_text(encoding='utf-8')
items = [ast.literal_eval(m) for m in re.findall(r"^(\['.*?\]),?$", src, re.M)]
cats = ast.literal_eval(re.search(r"const CATS = (\[.*?\]);", src).group(1))
L = '⓪①②③④⑤⑥⑦'
head = '<thead><tr><th style="width:5%">✓</th><th style="width:14%">상황</th><th>과제</th><th style="width:7%">단계</th><th style="width:9%">예시<br>불안</th><th style="width:9%">내<br>불안</th></tr></thead>'
body = ''
for g, lo, hi in [('쉬움 (예상 불안 0–3)', 0, 3), ('보통 (예상 불안 4–6)', 4, 6), ('어려움 (예상 불안 7–10)', 7, 10)]:
    its = sorted([x for x in items if lo <= x[2] <= hi], key=lambda x: (x[2], cats.index(x[0])))
    rows = ''.join(f'<tr><td>□</td><td>{c}</td><td>{t}</td><td style="text-align:center">{L[l]}</td><td style="text-align:center">{s}</td><td></td></tr>' for c, l, s, t in its)
    body += f'<h2>{g} · {len(its)}개</h2><table>{head}<tbody>{rows}</tbody></table>'
page = f'''<section class="sheet ex"><h1>부록. 불안 사다리 예시 과제 {len(items)}개</h1>
<p class="hint">나에게 해당하는 과제에 ✓ 하고, 오른쪽 칸에 <b>내가 느끼는 예상 불안</b>을 다시 적으세요. 고른 과제를 B. 불안 사다리에 옮겨 적으면 됩니다. (단계 ⓪비언어 ①소리 ②녹음/비대면 ③한 단어 ④짧은 문장 ⑤질문 ⑥대화 ⑦여러 사람 앞)<br>
상황 쉬운 순: {' → '.join(cats)}</p>
{body}</section>'''
f = here / 'worksheets.html'
s = re.sub(r'<section class="sheet ex">.*?</section>\n?', '', f.read_text(encoding='utf-8'), flags=re.S)
f.write_text(s.replace('</body>', page + '\n</body>'), encoding='utf-8')
