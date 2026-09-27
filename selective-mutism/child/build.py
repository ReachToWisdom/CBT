# ../practice.html(성인용)을 틀로 삼아 초등학생(3학년 무렵)용 연습 노트 child/practice.html을 만든다.
# 예시 과제: child/examples.txt ([상황, 말하기 단계 0–7, 예상 불안, 과제] 한 줄씩). 이후 `node render.js`로 PDF 생성.
import re, ast, pathlib
from collections import defaultdict
here = pathlib.Path(__file__).parent
s = (here / '../practice.html').read_text(encoding='utf-8')
lines = (here / 'examples.txt').read_text(encoding='utf-8').strip() + '\n'
items = [ast.literal_eval(l.rstrip(',')) for l in lines.splitlines()]

# 상황 순서 = 예시 과제 평균 예상 불안이 낮은 순
avg = defaultdict(list)
for c, _, suds, _ in items: avg[c].append(suds)
cats = sorted(avg, key=lambda c: sum(avg[c]) / len(avg[c]))

def rep(a, b, pattern=False):
    global s
    n = len(re.findall(a, s, re.S)) if pattern else s.count(a)
    assert n == 1, (a[:40], n)
    s = re.sub(a, lambda m: b, s, flags=re.S) if pattern else s.replace(a, b)

rep(r"const EXAMPLES = \[\n.*?\n\];", 'const EXAMPLES = [\n' + lines + '];', pattern=True)
rep(r"const CATS = \[.*?\];", 'const CATS = [' + ', '.join(f"'{c}'" for c in cats) + '];', pattern=True)
rep("const KEY = 'sm-practice-v1';", "const KEY = 'sm-practice-child-v1';")
rep("<title>말하기 연습 노트</title>", "<title>우리 아이 말하기 연습</title>")
rep("<h1>말하기 연습 노트</h1>", "<h1>우리 아이 말하기 연습 노트</h1>")
rep("""선택적 함묵증 자가 실행용 · 불안 사다리를 만들고, 한 단계씩 연습하고, 변화를 기록하세요.<br>""",
    """선택적 함묵증 · 초등학생용 (보호자와 함께) · 용기 사다리를 만들고, 한 단계씩 연습하고, 변화를 기록하세요.<br>
    불안 점수는 아이에게 "얼마나 떨려? 0(하나도 안 떨림)~10(엄청 떨림)"으로 물어 보세요. 말하라고 재촉하지 말고 5초 기다려 주고, 대신 대답해 주지 마세요.<br>""")
rep("""placeholder="예) 편의점에서 '봉투 주세요' 말하기\"""", """placeholder="예) 문구점에서 '이거 주세요' 말하기\"""")
rep("""placeholder="예) 목소리가 떨려서 점원이 이상하게 볼 것이다\"""", """placeholder="예) 친구들이 내 목소리 듣고 놀랄 것 같아\"""")
rep("""placeholder="예) 점원은 아무렇지 않게 봉투를 줬다. 걱정한 일은 일어나지 않았다.\"""", """placeholder="예) 아저씨가 웃으면서 '고마워' 했다. 생각보다 괜찮았다.\"""")
rep("""placeholder="예) 좋아하는 음료 한 잔\"""", """placeholder="예) 스티커 1개, 놀이터 10분 더\"""")
rep("""placeholder="예) 회의에서 의견을 물어봄\"""", """placeholder="예) 선생님이 출석을 부름\"""")
rep("""placeholder="예) 이제 와서 말하면 다들 놀라서 쳐다볼 거야\"""", """placeholder="예) 내가 말하면 다들 '말했다!' 하고 쳐다볼 거야\"""")
rep("""placeholder="예) 잠깐 놀랄 수 있지만 금방 잊는다. 불편해도 견딜 수 있다.\"""", """placeholder="예) 잠깐 볼 수도 있지만 금방 자기 할 일 한다. 떨려도 나는 할 수 있어!\"""")
rep("speaking-practice-${today()}.json", "child-speaking-practice-${today()}.json")
s = s.replace("나의 불안 사다리", "우리 아이 용기 사다리").replace("<h2>나의 사다리", "<h2>용기 사다리")
(here / 'practice.html').write_text(s, encoding='utf-8')
print(len(items), 'examples;', ' → '.join(cats))
