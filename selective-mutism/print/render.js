// A4 PDF 생성: node render.js
//  - guide.html, worksheets.html -> ../guide.pdf, ../worksheets.pdf
//  - practice.html의 [사다리 인쇄] 결과(예시 과제 전체): 난이도순 -> ../ladder.pdf, 상황별 -> ../ladder-situation-{asc,desc}.pdf
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  for (const n of ['guide', 'worksheets']) {
    await p.goto('file://' + path.join(__dirname, n + '.html'), { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.pdf({ path: path.join(__dirname, '..', n + '.pdf'), format: 'A4', printBackground: true, preferCSSPageSize: true });
  }
  const ctx = await b.newContext();  // 빈 저장소 = 예시 과제 전체
  const lp = await ctx.newPage();
  await lp.addInitScript(() => { window.print = () => {}; });
  await lp.goto('file://' + path.join(__dirname, '..', 'practice.html'));
  await lp.emulateMedia({ media: 'print' });
  for (const [mode, dir, file] of [['level', 'asc', 'ladder'], ['cat', 'asc', 'ladder-situation-asc'], ['cat', 'desc', 'ladder-situation-desc']]) {
    await lp.evaluate(([m, d]) => {
      document.getElementById('sortMode').value = m; document.getElementById('sortDir').value = d;
      document.getElementById('printLadder').click();
      document.querySelector('.pmeta span:nth-child(2)').textContent = '날짜:';
    }, [mode, dir]);
    await lp.pdf({ path: path.join(__dirname, '..', file + '.pdf'), format: 'A4', printBackground: true, preferCSSPageSize: true });
  }
  await b.close();
})();
