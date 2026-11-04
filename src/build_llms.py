# llms.txt (index) + llms-full.txt (all doc pages as plain markdown) from the built site
import re, pathlib
from bs4 import BeautifulSoup, NavigableString
R = pathlib.Path('site')
src = open('src/build_site.py').read()
PAGES = re.findall(r"\('([a-z0-9-]+)', '([^']+)', '(start|brand|found|comp)', ", src)
GROUP = {'start': '시작하기', 'brand': 'Brand', 'found': 'Foundations', 'comp': 'Components'}
def md(node):
    out = []
    def walk(n):
        if isinstance(n, NavigableString):
            t = re.sub(r'\s+', ' ', str(n)); out.append(t); return
        name = n.name
        if name in ('script', 'style', 'svg', 'button', 'img'): return
        if 'class' in n.attrs and any(c in ('canvas', 'ex-stage', 'phone', 'swatches', 'ic-grid', 'il-grid', 'pager', 'copy') for c in n['class']): return
        if name in ('h1', 'h2', 'h3', 'h4'):
            out.append('\n\n' + '#' * (int(name[1]) + 0) + ' ' + n.get_text(' ', strip=True) + '\n\n'); return
        if name == 'pre':
            out.append('\n\n```\n' + n.get_text() .strip() + '\n```\n\n'); return
        if name == 'table':
            rows = []
            for tr in n.find_all('tr'):
                cells = [re.sub(r'\s+', ' ', c.get_text(' ', strip=True)).replace('|', '/') for c in tr.find_all(['th', 'td'])]
                rows.append('| ' + ' | '.join(cells) + ' |')
                if tr.find('th') and len(rows) == 1: rows.append('|' + '---|' * len(cells))
            out.append('\n\n' + '\n'.join(rows) + '\n\n'); return
        if name == 'li': out.append('\n- ')
        if name == 'code': out.append('`' + n.get_text() + '`'); return
        if name == 'br': out.append('\n'); return
        for c in n.children: walk(c)
        if name in ('p', 'div', 'section', 'ul', 'ol', 'details', 'summary'): out.append('\n')
    walk(node)
    t = ''.join(out)
    t = re.sub(r'[ \t]+\n', '\n', t); t = re.sub(r'\n{3,}', '\n\n', t)
    return t.strip()
full, idx = [], {}
for slug, title, grp in PAGES:
    p = R / f'{slug}.html'
    if not p.exists(): continue
    s = BeautifulSoup(p.read_text(), 'html.parser')
    c = s.select_one('.content') or s.body
    lead = s.select_one('.lead')
    idx.setdefault(grp, []).append((slug, title, lead.get_text(' ', strip=True) if lead else ''))
    full.append(f'\n\n---\n\n<!-- {slug}.html -->\n' + md(c))
head = '''# Layer Design System

> 팀 회고 서비스 "레이어"의 디자인 시스템 문서. 모바일(375) · 웹(1440), 라이트 모드. 토큰 · 컴포넌트 82개 · 화면 틀(Template) · AI용 파일(DESIGN.md · components.json · tokens.json)과 웹 키트(layer.css · layer-icons.js · layer-examples.html)를 제공한다.

AI가 화면을 만들 때: DESIGN.md를 먼저 읽고, components.json에 있는 이름만 쓰고, Figma에서는 라이브러리 인스턴스를, 웹에서는 layer.css 클래스와 layer-examples.html 마크업을 그대로 쓴다. 컴포넌트를 새로 그리지 않는다. 전체 문서 텍스트는 llms-full.txt.

## AI 파일
- [DESIGN.md](downloads/DESIGN-v0.2.1.md): 규칙 요약(가장 먼저 읽기)
- [components.json](downloads/layer-components-v0.2.1.json): 컴포넌트 82개 — 쓰임 · 속성 · Figma 키 · 코드 클래스 · 예시 위치
- [tokens.json](downloads/layer-tokens-v0.2.1.json): 토큰 151개(DTCG)
- [AI 안내문](downloads/ai-instructions.md): 프로젝트 지침에 붙여넣는 글
- [layer-inline.css](kit/layer-inline.css)(채팅 미리보기에 붙여 넣는 스타일) · [layer.css](kit/layer.css) · [layer-icons.js](kit/layer-icons.js) · [layer-examples.html](kit/layer-examples.html): 웹 키트
- [llms-full.txt](llms-full.txt): 문서 전체 텍스트
- 웹 키트 고정 주소: <script src="https://cdn.jsdelivr.net/gh/Nakyeonng/layer-ds@v0.2.1/kit/layer.js"></script> (HTML 파일 · 사이트용, 스타일 + 아이콘 한 줄)
- GitHub: https://github.com/Nakyeonng/layer-ds
- [Figma 커뮤니티 파일](https://www.figma.com/community/file/1699490552460986431/layer-ds): 복제해서 쓰는 Figma 원본(컴포넌트 · 변수 · 스타일)
'''
body = []
for g in ('start', 'brand', 'found', 'comp'):
    if g not in idx: continue
    body.append(f'\n## {GROUP[g]}\n')
    for slug, title, lead in idx[g]:
        body.append(f'- [{title}]({slug}.html)' + (f': {lead}' if lead else ''))
(R / 'llms.txt').write_text(head + '\n'.join(body) + '\n')
(R / 'llms-full.txt').write_text('# Layer Design System — 문서 전체\n\n> llms.txt의 각 페이지를 한 파일로 이은 것. 표와 코드만 남기고 시각 예시는 뺐다.' + ''.join(full) + '\n')
print(len(PAGES), (R / 'llms.txt').stat().st_size, (R / 'llms-full.txt').stat().st_size)
