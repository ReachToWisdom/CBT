// A4 PDF 생성: node render.js
//  - guide.html, worksheets.html -> ../guide.pdf, ../worksheets.pdf
//  - practice.html의 [사다리 인쇄] 결과(예시 과제 전체, 쉬운 순) -> ../ladder.pdf
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
  await lp.click('#printLadder');
  await lp.evaluate(() => { document.querySelector('.pmeta span:last-child').textContent = '날짜:'; });
  await lp.emulateMedia({ media: 'print' });
  await lp.pdf({ path: path.join(__dirname, '..', 'ladder.pdf'), format: 'A4', printBackground: true, preferCSSPageSize: true });
  await b.close();
})();
