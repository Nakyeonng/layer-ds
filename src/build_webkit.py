# Layer web kit: layer.css · layer-icons.js · layer-examples.html (+ logo/illustrations/font copied)
import json, re, pathlib, shutil, html as H
from bs4 import BeautifulSoup
R = pathlib.Path('site'); K = R / 'kit'
F = pathlib.Path('foundations')
I = json.load(open(F / 'icons/_src/assets_nav.json')); G = json.load(open(F / 'icons/_src/graphic.json'))
VER = '0.2.1'
def mono(s): return s.replace('fill="#212329"', 'fill="currentColor"').replace('fill="black"', 'fill="currentColor"')
def bare(s): return re.sub(r'^<svg width="[\d.]+" height="[\d.]+"', '<svg aria-hidden="true" focusable="false"', s)

# ── icon names ──
def iname(k):
    grp, n = k.split('/')[1], k.split('/')[2]
    n = re.sub(r'(?<=[a-z])(?=[A-Z])', '-', n).replace('_', '-').lower()
    return ('nav-' + n) if grp == 'Nav' else n
def gname(k):
    base, var = k.split('|'); n = base.split('/')[-1].lower(); v = var.split('=')[1].lower().replace('_', '-')
    if n == 'emotion': return 'emotion-' + v
    return 'graphic-' + n + ('' if v == 'color' else '-white')
ICONS = {iname(k): bare(mono(v)) for k, v in I.items()}
GRAPH = {gname(k): bare(v) for k, v in G.items()}
ALL = {**ICONS, **GRAPH}

# ── layer.css ──
ORDER = ['color','typography','spacing','radius','elevation','layout','icons','components','buttons','chips','fields','tabs','controls','lists','feedback','date-picker','popup','bottom-sheet','illustration','badge','cards','analysis','writing']
EXTRA = r'''
/* ── Kit additions (not on the doc site) ─────────────────────── */
/* Template/Mobile Background=Secondary — 흰 카드를 쌓는 목록 화면 */
.layout-mobile--secondary { background: var(--color-bg-secondary, #f2f4f8); }
/* App Bar/OS Bar — 시안용 상태 바 44 · 홈 표시줄 34 */
.os-status { height: 44px; flex: none; display: flex; align-items: center; justify-content: space-between; padding: 0 20px 0 28px; font: 600 15px/1 var(--font-family, "Pretendard", sans-serif); color: var(--color-text-primary, #212329); }
.os-home { height: 34px; flex: none; display: flex; align-items: flex-end; justify-content: center; padding-bottom: 8px; }
.os-home::after { content: ""; width: 134px; height: 5px; border-radius: 99px; background: var(--color-gray-900, #212329); }
/* Logo */
.logo { display: inline-block; flex: none; width: 64px; height: 21px; background: url("logo/logo-horizontal-basic.svg") center / contain no-repeat; }
.logo--symbol { width: 20px; height: 20px; background-image: url("logo/symbol-three-colors.svg"); }

/* Menu · Popover anchor — 연 버튼 바로 아래 오른쪽 끝(사이 4), 딤드 없음 */
.menu-anchor { position: relative; display: inline-flex; }
.menu-anchor > .menu, .menu-anchor > .popover { position: absolute; top: calc(100% + var(--spacing-4, 4px)); right: 0; z-index: 10; }

/* Section Header — 목록 · 열 위 제목 + 개수 (개수를 Badge로 만들지 않는다) */
.section-header { display: flex; align-items: baseline; gap: 6px; margin: 0 0 var(--spacing-16, 16px); font-size: 16px; font-weight: 700; line-height: 1.4; color: var(--color-text-primary, #212329); }
.section-header__count { color: var(--color-gray-600, #8b909c); }
.section-header--18 { font-size: 18px; }
.section-header--18 .section-header__count { font-weight: 600; }

/* LNB — Fold=Off 284(Template/Web List) · .lnb--folded 84(Work) */
.lnb { box-sizing: border-box; display: flex; width: var(--layout-lnb, 284px); height: 100vh; position: sticky; top: 0; padding: var(--spacing-12, 12px); background: var(--color-bg-secondary, #f2f4f8); }
.lnb__panel { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 16px; padding-top: 22px; border-radius: var(--radius-12, 12px); background: var(--color-bg-surface, #fff); overflow: hidden; }
.lnb__head { display: flex; align-items: center; justify-content: space-between; height: 24px; padding: 0 16px 17px 20px; border-bottom: 1px solid var(--color-gray-200, #edf0f4); }
.lnb__icon-btn { display: inline-grid; place-items: center; width: 24px; height: 24px; padding: 0; border: 0; border-radius: var(--radius-6, 6px); background: none; color: var(--color-text-primary, #212329); cursor: pointer; }
.lnb__icon-btn .icon { width: 18px; height: 18px; }
.lnb__icon-btn:hover { background: var(--color-gray-100, #f2f4f8); }
.lnb__body { flex: 1; min-height: 0; overflow: auto; display: flex; flex-direction: column; gap: 8px; padding: 0 12px; }
.lnb__home { display: flex; align-items: center; gap: 16px; height: 39px; padding: 4px 8px; border-radius: var(--radius-8, 8px); font-size: 16px; font-weight: 600; line-height: 1.4; color: var(--color-text-primary, #212329); text-decoration: none; }
.lnb__home .icon { width: 16px; height: 16px; }
.lnb__home:hover, .lnb__home[aria-current="page"] { background: var(--color-gray-100, #f2f4f8); }
.lnb__divider { height: 1px; flex: none; background: var(--color-gray-200, #edf0f4); }
.lnb__section-head { display: flex; align-items: center; justify-content: space-between; height: 32px; margin-top: 8px; padding: 4px 4px 4px 8px; box-sizing: border-box; font-size: 16px; font-weight: 600; line-height: 1.4; color: var(--color-text-primary, #212329); }
.lnb__tabs { padding: 4px 4px 0; }
.lnb__spaces { list-style: none; margin: 0; padding: 8px 0; display: flex; flex-direction: column; gap: 4px; }
.lnb__space { display: flex; align-items: center; gap: 10px; padding: 7px 8px 7px 4px; border-radius: var(--radius-8, 8px); color: inherit; text-decoration: none; }
.lnb__space:hover, .lnb__space[aria-current="page"] { background: var(--color-gray-100, #f2f4f8); }
.lnb__thumb { flex: none; display: grid; place-items: center; width: 36px; height: 36px; border-radius: 50%; background: var(--color-gray-200, #edf0f4); }
.lnb__thumb .icon { width: 24px; height: 24px; }
.lnb__text { min-width: 0; display: flex; flex-direction: column; gap: 2px; }
.lnb__title { font-size: 14px; font-weight: 600; line-height: 1.4; color: var(--color-text-primary, #212329); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.lnb__desc { font-size: 12px; font-weight: 500; line-height: 1.4; color: var(--color-gray-600, #8b909c); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.lnb__add { display: flex; align-items: center; gap: 16px; margin-top: 4px; padding: 5px 10px; border: 0; border-radius: var(--radius-8, 8px); background: none; font: inherit; font-size: 14px; font-weight: 500; line-height: 1.4; color: var(--color-gray-600, #8b909c); cursor: pointer; text-align: left; }
.lnb__add-icon { display: grid; place-items: center; width: 24px; height: 24px; border-radius: var(--radius-8, 8px); background: var(--color-gray-100, #f2f4f8); color: var(--color-gray-700, #666b75); }
.lnb__add-icon .icon { width: 14px; height: 14px; }
.lnb__add:hover { background: var(--color-gray-100, #f2f4f8); }
.lnb__foot { display: flex; align-items: center; gap: 8px; padding: 6px 20px 8px; }
.lnb__foot-sep { width: 1px; height: 16px; background: var(--color-gray-200, #edf0f4); }
.lnb__me, .lnb__help { display: flex; align-items: center; height: 36px; box-sizing: border-box; border: 0; border-radius: var(--radius-8, 8px); background: none; font: inherit; font-size: 13px; font-weight: 500; line-height: 1.4; color: var(--color-gray-700, #666b75); cursor: pointer; }
.lnb__me { gap: 12px; padding: 4px; }
.lnb__help { gap: 6px; padding: 8px; }
.lnb__help .icon { width: 18px; height: 18px; }
.lnb__me:hover, .lnb__help:hover { background: var(--color-gray-100, #f2f4f8); }
/* 접은 LNB — 아이콘만 */
.lnb--folded { width: var(--layout-lnb-folded, 84px); }
.lnb--folded .lnb__panel { gap: 12px; padding: 22px 0; align-items: stretch; }
.lnb--folded .lnb__head { justify-content: center; height: auto; padding: 2px 0 8px; border: 0; }
.lnb--folded .lnb__head .logo, .lnb--folded .lnb__text, .lnb--folded .lnb__home span:not(.icon), .lnb--folded .lnb__section-title, .lnb--folded .lnb__tabs, .lnb--folded .lnb__add, .lnb--folded .lnb__foot-sep, .lnb--folded .lnb__me-name, .lnb--folded .lnb__help-label { display: none; }
.lnb--folded .lnb__body { padding: 0; align-items: center; gap: 12px; }
.lnb--folded .lnb__home { width: 38px; height: 38px; padding: 0; justify-content: center; border-radius: 99px; }
.lnb--folded .lnb__divider { width: 36px; }
.lnb--folded .lnb__section-head { justify-content: center; margin: 0; padding: 4px 0; }
.lnb--folded .lnb__spaces { padding: 0; }
.lnb--folded .lnb__space { width: 48px; height: 48px; padding: 0; justify-content: center; box-sizing: border-box; }
.lnb--folded .lnb__foot { flex-direction: column; gap: 8px; padding: 4px 0 12px; }
.lnb--folded .lnb__help { width: 36px; padding: 0; justify-content: center; }
.lnb--folded .lnb__help .icon { width: 20px; height: 20px; }
'''
FONT = '''@font-face {
  font-family: "Pretendard";
  src: url("fonts/PretendardVariable.woff2") format("woff2-variations"), url("fonts/PretendardVariable.woff2") format("woff2");
  font-weight: 45 920; font-display: swap;
}
html { -webkit-text-size-adjust: 100%; }
body { margin: 0; font-family: "Pretendard", -apple-system, BlinkMacSystemFont, system-ui, sans-serif; color: var(--color-text-primary, #212329); background: var(--color-bg-surface, #fff); -webkit-font-smoothing: antialiased; }
*, *::before, *::after { box-sizing: border-box; }
'''
css = [f'/* Layer Design System — layer.css v{VER}\n   한 파일로 모든 토큰 · 컴포넌트 스타일. <link rel="stylesheet" href="layer.css"> 하나만 불러온다.\n   클래스 이름과 예시 마크업은 layer-examples.html, 아이콘은 layer-icons.js(data-icon). */\n', FONT]
for n in ORDER:
    css.append(f'\n/* ═══ {n}.css ═══ */\n' + (R / 'css' / f'{n}.css').read_text())
css.append(EXTRA)
CSS = ''.join(css)
K.mkdir(exist_ok=True)
(K / 'layer.css').write_text(CSS)

# ── layer-icons.js ──
js = ('/* Layer Design System — layer-icons.js v%s\n   <span class="icon icon-24" data-icon="arrow-left"></span> 처럼 쓰고, 페이지 끝에서 이 파일을 불러온다.\n'
      '   단색 아이콘은 글자색(currentColor)을 따른다. Graphic(graphic-* · emotion-*)은 색이 정해져 있다. */\n'
      '(function () {\n  var I = %s;\n'
      '  function fill(root) { (root || document).querySelectorAll("[data-icon]").forEach(function (el) { var s = I[el.getAttribute("data-icon")]; if (s && !el.firstElementChild) el.innerHTML = s; }); }\n'
      '  window.LayerIcons = { names: Object.keys(I), fill: fill };\n'
      '  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", function () { fill(); }); else fill();\n})();\n') % (VER, json.dumps(ALL, ensure_ascii=False, indent=0))
(K / 'layer-icons.js').write_text(js)

# ── copy assets ──
for sub, src in [('logo', R / 'img/logo'), ('illustrations', R / 'img/illustrations')]:
    d = K / sub; d.mkdir(exist_ok=True)
    for f in src.glob('*.svg'): shutil.copy(f, d / f.name)
(K / 'fonts').mkdir(exist_ok=True); shutil.copy(R / 'fonts/PretendardVariable.woff2', K / 'fonts/PretendardVariable.woff2'); shutil.copy(R / 'fonts/OFL.txt', K / 'fonts/OFL.txt')

# ── examples (real markup lifted from the doc site) ──
C = json.load(open(F / 'components.json'))['components']
SIG = {}
for k, v in ALL.items():
    sg = frozenset(p.get('d') for p in BeautifulSoup(v, 'html.parser').find_all('path'))
    SIG.setdefault(sg, k)
SEL = {  # component → CSS selector used to lift one real specimen from the site
 'Button/Filled Button': '.btn.btn--primary', 'Button/Ghost Button': '.btn.btn--ghost', 'Button/Outlined Button': '.btn.btn--outlined',
 'Button/Floating Button': '.btn.btn--floating', 'Button/Button Group': '.btn-group', 'Chip/Two Choice': '.chip-pair',
 'Chip/Multi Choice with Icon': '.chip-button.chip-button--icon', 'Chip/Multi Choice': '.chip-button:not(.chip-button--icon):not(.chip-button--card)',
 'Progress/Progress Bar': '.progress-bar', 'Tabs/Text Tabs': '.tabs:not(.tabs--fixed)', 'Segmented Control': '.segmented', 'Tabs/Text Fixed Tabs': '.tabs.tabs--fixed',
 'Tabs/Box Tabs': '.box-tabs', 'Bottom Sheet/Short': '.bsheet:not(.bsheet--long)', 'Bottom Sheet/Long': '.bsheet.bsheet--long', 'Date Time Picker': '.dtp',
 'Fields/Select Field': '.select-field', 'Fields/Text Input': '.field:not(.field--area)', 'Fields/Text Area': '.field.field--area',
 'Controls/Checkbox': '.control:has(input[type=checkbox])', 'Controls/Radio': '.control:has(input[type=radio])', 'List/Checkbox List': '.list:has(.list-check)',
 'List/Icon List': '.list--cards', 'Accordion/Index Title': '.acc-title', 'Accordion/Index': '.acc-index', 'Accordion/Contents': '.acc',
 'App Bar/Top App Bar': '.app-bar', 'App Bar/Navigation Bar': '.nav-bar', 'Profile': '.avatar', 'Modal (Web)': '.modal', 'Popup': '.popup',
 'Toasts/Toast': '.toast', 'Tooltips/Function Tooltip': '.tooltip:not(.tooltip--hover)', 'Tooltips/Hover Tooltip': '.tooltip.tooltip--hover',
 'Section Header': '.section-header', 'Popover': '.popover', 'Menu': '.menu', 'List/Member Item': '.member-list', 'Info Banner': '.info-banner',
 'Tooltips/Guide Tooltip': '.guide-tip', 'Scroll Bar/Scroll Bar': '.scroll-area', 'Badge': '.badge', 'Button/Text Button': '.text-button',
 'List/Menu Item': '.menu-card', 'Empty State': '.empty-state', 'Card/Retro (Web)': '.retro-card-web', 'Card/Retro (Mobile)': '.retro-card',
 'Card/Space': '.space-card', 'Card/Goal (Web)': '.goal-card:not(.goal-card--mobile)', 'Question Tag': '.question-tag', 'Button/Pager': '.question-pager',
 'Question Index (Web)': '.question-index', 'Card/Goal (Mobile)': '.goal-card.goal-card--mobile', 'Accordion/Section (Web)': '.section-accordion',
 'Card/Answer': '.answer-card', 'Answer/Emotion Scale': '.emotion-scale', 'Answer/Score Bar': '.score-bar', 'Card/Template': '.template-card',
 'Card/Template Detail': '.template-detail', 'Analysis/Section Title': '.analysis-title', 'Analysis/Progress Panel': '.analysis-panel',
 'Analysis/Satisfaction': '.satisfaction', 'Analysis/Goal Rate': '.goal-rate', 'Analysis/Keyword Group': '.keyword-group', 'Analysis/Keyword Item': '.keyword-item',
 'Analysis/Highlight Title': '.highlight-title', 'Card/Template Summary': '.template-summary', 'Card/Question Group (Web)': '.question-group', 'Dropdown': '.dropdown',
}
PAGES = [p for p in sorted(R.glob('*.html')) if p.stem not in ('index', 'updates', 'tokens', 'ai-guide', 'color', 'typography', 'spacing', 'radius', 'elevation', 'iconography', 'state')]
soups = [(p.stem, BeautifulSoup(p.read_text(), 'html.parser')) for p in PAGES]
for _, s in soups:
    for bad in s.select('.site-header, .sidebar, .pager, .site-toast, pre, .code, .copy, script, style, .page-head'): bad.decompose()
def clean(el):
    el = BeautifulSoup(str(el), 'html.parser')
    for t in el.find_all(True):
        for a in list(t.attrs):
            if a.startswith('data-copy') or a in ('data-bsheet', 'data-dl', 'data-dl-name', 'id', 'tabindex') and a != 'id': del t[a]
        if t.get('class'): t['class'] = [c for c in t['class'] if c not in ('is-static', 'ic--static')] or None
        if t.get('class') is None and 'class' in t.attrs: del t['class']
    for svg in el.find_all('svg'):
        key = frozenset(p.get('d') for p in svg.find_all('path'))
        name = SIG.get(key)
        par = svg.parent
        if name and par is not None and par.name == 'span' and 'icon' in (par.get('class') or []) and len(par.find_all('svg')) == 1:
            par['data-icon'] = name; svg.decompose()
    out = str(el).replace('src="img/illustrations/', 'src="illustrations/').replace('src="img/logo/', 'src="logo/')
    el = out
    return el
EX, miss = {}, []
for comp, sel in SEL.items():
    found = None
    for stem, s in soups:
        try: m = s.select_one(sel)
        except Exception as e: m = None
        if m is not None: found = (stem, m); break
    if not found: miss.append(comp); continue
    EX[comp] = (found[0], clean(found[1]))
# LNB / OS Bar / Logo / templates — written by hand (no specimen on the site)
LNB_HTML = '''<aside class="lnb">
  <div class="lnb__panel">
    <div class="lnb__head"><span class="logo" role="img" aria-label="Layer"></span><button class="lnb__icon-btn" aria-label="메뉴 접기"><span class="icon" data-icon="arrow-left"></span></button></div>
    <nav class="lnb__body">
      <a class="lnb__home" href="#"><span class="icon" data-icon="nav-home"></span><span>홈</span></a>
      <div class="lnb__divider"></div>
      <div class="lnb__section-head"><span class="lnb__section-title">내 스페이스</span><button class="lnb__icon-btn" aria-label="스페이스 만들기"><span class="icon" data-icon="add"></span></button></div>
      <div class="lnb__tabs"><div class="tabs tabs--web" role="tablist"><button class="tab" role="tab" aria-selected="true">전체</button><button class="tab" role="tab" aria-selected="false">개인</button><button class="tab" role="tab" aria-selected="false">팀</button></div></div>
      <ul class="lnb__spaces">
        <li><a class="lnb__space" href="#"><span class="lnb__thumb"><span class="icon" data-icon="graphic-management"></span></span><span class="lnb__text"><span class="lnb__title">기획 프로젝트</span><span class="lnb__desc">기획 수업 회고</span></span></a></li>
        <li><a class="lnb__space" href="#" aria-current="page"><span class="lnb__thumb"><span class="icon" data-icon="graphic-development"></span></span><span class="lnb__text"><span class="lnb__title">떡잎마을방범대</span><span class="lnb__desc">IT 연합동아리 디프만 15기의 프로젝트</span></span></a></li>
      </ul>
      <button class="lnb__add"><span class="lnb__add-icon"><span class="icon" data-icon="add"></span></span>스페이스 추가</button>
    </nav>
    <div class="lnb__foot"><button class="lnb__me"><span class="avatar avatar--28"></span><span class="lnb__me-name">홍길동</span></button><span class="lnb__foot-sep"></span><button class="lnb__help"><span class="icon" data-icon="question"></span><span class="lnb__help-label">헬프 센터</span></button></div>
  </div>
</aside>'''
HAND = {
 'LNB': ('kit', LNB_HTML),
 'Section Header': ('kit', '<h2 class="section-header">진행 중인 회고 <span class="section-header__count">4</span></h2>'),
 'Logo': ('kit', '<span class="logo" role="img" aria-label="Layer"></span> <span class="logo logo--symbol" role="img" aria-label="Layer"></span>'),
 'App Bar/OS Bar': ('kit', '<div class="os-status"><span>9:41</span><span></span></div>\n<!-- 화면 맨 아래(하단 내비게이션이 없을 때) -->\n<div class="os-home"></div>'),
}
for k, v in HAND.items(): EX[k] = v
_ab = []
for sel in ('.app-bar.app-bar--home', '.app-bar.app-bar--sub'):
    for stem, sp in soups:
        m = sp.select_one(sel)
        if m is not None: _ab.append(clean(m)); break
if _ab: EX['App Bar/Top App Bar'] = ('app-bar', '\n'.join(_ab))
EX['Date Time Picker'] = ('date-picker', clean(BeautifulSoup(open('src/data/dtp.html').read(), 'html.parser')))
prof = BeautifulSoup(EX['Profile'][1], 'html.parser').select_one('.avatar')
if prof is not None:
    prof['class'] = [c for c in prof['class'] if not c.startswith('avatar--')] + ['avatar--28']
    for k in ('LNB',):
        EX[k] = (EX[k][0], EX[k][1].replace('<span class="avatar avatar--28"></span>', str(prof)))
avatar_ok = 'avatar' in CSS
def anchor(n): return re.sub(r'[^a-z0-9]+', '-', n.lower()).strip('-')
def _ex(comp): return EX.get(comp, ('', ''))[1]
_appbar_sub = BeautifulSoup(_ex('App Bar/Top App Bar'), 'html.parser').select('.app-bar')
_sub = str(_appbar_sub[-1]) if _appbar_sub else ''
_home = str(_appbar_sub[0]) if _appbar_sub else ''
_retro = _ex('Card/Retro (Mobile)')
_rweb = _ex('Card/Retro (Web)')
MOB = f"""<div class="layout-mobile layout-mobile--secondary" style="min-height:640px">
  <div class="os-status"><span>9:41</span><span></span></div>
  {_home}
  <main class="layout-mobile__content">
    <div style="display:flex;flex-direction:column;gap:var(--spacing-12);padding-top:var(--spacing-12)">
      {_retro}
    </div>
  </main>
  {_ex('App Bar/Navigation Bar')}
</div>"""
WEB = f"""<div class="layout-web-list" style="min-height:640px">
  {_ex('LNB')}
  <main class="layout-web-list__body">
    <h1 class="text-heading-28-bold" style="margin:0 0 var(--spacing-32)">떡잎마을방범대</h1>
    <div class="layout-web-list__columns">
      <section>
        <h2 class="section-header">진행 중인 회고 <span class="section-header__count">1</span></h2>
        <div style="display:flex;flex-direction:column;gap:var(--spacing-12)">
          <div class="menu-anchor" style="display:block">{_rweb}</div>
        </div>
      </section>
    </div>
  </main>
</div>"""
TEMPLATES = (f'<section class="ex" id="template-mobile"><h2>Template/Mobile <small>.layout-mobile (+ --secondary)</small></h2>'
  '<p class="ex-note">모바일 화면 뼈대: 상태 바 → 앱 바 → 내용(좌우 20) → 하단 내비게이션. 하단 내비게이션은 메인 탭 화면(홈 · 실행목표 · 분석)에만 두고, 상세 · 작성 화면은 빼고 아래에 Button Group을 둔다. 상세 화면의 앱 바는 .app-bar--sub(Top App Bar 예시 두 번째).</p>'
  f'<div class="ex-stage ex-stage--mobile">{MOB}</div><pre class="ex-code">{H.escape(MOB)}</pre></section>'
  f'<section class="ex" id="template-web"><h2>Template/Web <small>.layout-web-list · .layout-web-work</small></h2>'
  '<p class="ex-note">List = 펼친 LNB + 본문(여백 40, 카드 열 296, 열 사이 40). Work = 접은 LNB(.lnb--folded) + .layout-web-work__list + .layout-web-work__panel. 메뉴를 열 때는 더보기 버튼을 감싼 요소에 .menu-anchor를 주고 그 안에 .menu를 넣는다.</p>'
  f'<div class="ex-stage">{WEB}</div><pre class="ex-code">{H.escape(WEB)}</pre></section>')
secs = []
for comp in C:
    if comp in ('Template/Web', 'Template/Mobile'): continue
    if comp not in EX: continue
    src, mk = EX[comp]
    cls = (C[comp].get('code') or {}).get('class') or ''
    secs.append(f'<section class="ex" id="{anchor(comp)}"><h2>{H.escape(comp)} <small>{H.escape(cls)}</small></h2><div class="ex-stage">{mk}</div><pre class="ex-code">{H.escape(mk)}</pre></section>')
page = f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Layer 컴포넌트 예시 마크업 v{VER}</title>
<link rel="stylesheet" href="layer.css">
<style>
 body {{ background: #fff; padding: 32px 24px 80px; max-width: 1100px; margin: 0 auto; }}
 .ex-intro p {{ color: #5d626c; font-size: 14px; line-height: 1.6; }}
 .ex {{ border-top: 1px solid #e4e8ee; padding: 28px 0; }}
 .ex h2 {{ font-size: 18px; margin: 0 0 12px; }} .ex h2 small {{ font-size: 12px; font-weight: 500; color: #8b909c; margin-left: 8px; font-family: ui-monospace, monospace; }}
 .ex-stage {{ padding: 20px; background: #f7f8fa; border-radius: 10px; overflow: auto; position: relative; }}
 .ex-stage .lnb {{ height: 640px; position: static; }}
 .ex-stage--mobile {{ display: flex; justify-content: center; }} .ex-stage--mobile .layout-mobile {{ margin: 0; }}
 .ex-code {{ margin: 12px 0 0; padding: 14px 16px; background: #f2f4f8; border-radius: 8px; font: 12px/1.6 ui-monospace, monospace; white-space: pre-wrap; word-break: break-all; color: #454952; max-height: 320px; overflow: auto; }}
 .ex-note {{ font-size: 14px; color: #5d626c; }}
</style></head><body>
<div class="ex-intro"><h1>Layer 컴포넌트 예시 마크업</h1>
<p>각 컴포넌트의 실제 HTML 구조입니다. 새 화면을 만들 때 여기 있는 마크업을 그대로 복사해 글자만 바꾸세요. 새 CSS로 컴포넌트를 다시 그리지 않습니다.<br>
필요한 파일: <code>layer.css</code> (스타일 전부), <code>layer-icons.js</code> (<code>data-icon</code> 아이콘 채우기), <code>logo/</code> · <code>illustrations/</code> · <code>fonts/</code>.</p></div>
{TEMPLATES}
{''.join(secs)}
<script src="layer-icons.js"></script>
</body></html>'''
(K / 'layer-examples.html').write_text(page)
print('css', len(CSS), 'icons', len(ALL), 'examples', len(EX), 'miss', miss)
print('names', sorted(ALL)[:80])
