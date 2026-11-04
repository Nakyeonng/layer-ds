"""Build tokens.json (W3C Design Tokens Community Group format) from the same sources as the CSS and Figma variables."""
import json, re, pathlib
F = pathlib.Path('foundations')
css = (F / 'color.css').read_text()

def fx(name, scopes=None, css_var=None):
    ext = {'com.figma': {'variable': name}}
    if scopes: ext['com.figma']['scopes'] = scopes
    if css_var: ext['web'] = {'css': f'var({css_var})'}
    return ext

T = {'$description': 'Layer Design System tokens — v0.2.1 (2026-11-03). Format: W3C Design Tokens (DTCG). '
                     'Names match Figma variables (Color, Color Role, Spacing, Radius collections) and CSS custom properties. '
                     'Use role tokens (color.text.*, color.bg.*, …) in components; palette steps are for Hover/Pressed and cases without a role.'}

# ── color palette ─────────────────────────────
pal = {}
for fam, step, hexv in re.findall(r'--color-([a-z]+)-(\d+):\s*#([0-9A-Fa-f]{6});', css):
    pal.setdefault(fam, {})[step] = {'$value': '#' + hexv.upper(), '$extensions': fx(f'color/{fam}/{step}', [], f'--color-{fam}-{step}')}
for step, a in re.findall(r'--color-opacity-(\d+):\s*rgb\(6 8 12 / ([\d.]+)\);', css):
    alpha = round(float(a) * 255)
    pal.setdefault('opacity', {})[step] = {'$value': f'#06080C{alpha:02X}', '$description': f'#06080C at {int(step)}% — shadows, dividers, dim',
                                           '$extensions': fx(f'color/opacity/{step}', [], f'--color-opacity-{step}')}
for fam in pal:
    pal[fam] = dict(sorted(pal[fam].items(), key=lambda kv: int(kv[0])))
PALETTE_NOTE = 'Palette steps color.gray.* · blue.* · purple.* · green.* · red.* · orange.* · opacity.* are hidden from Figma pickers; reach for the role groups (text, bg, border, overlay, status) first.'

# ── color roles ───────────────────────────────
ROLES = [
    ('text', 'primary', 'gray.900', '제목, 본문, 입력한 글자, 선택된 탭', ['TEXT_FILL']),
    ('text', 'secondary', 'gray.700', '아코디언 내용·제목 등 보조 글자', ['TEXT_FILL']),
    ('text', 'tertiary', 'gray.500', '안내 문구(placeholder), 팝업 부제, 선택 안 된 탭', ['TEXT_FILL']),
    ('text', 'disabled', 'gray.400', '비활성 버튼·칩·라벨·날짜 글자', ['TEXT_FILL']),
    ('text', 'inverse', 'gray.0', '진한 바탕 위 글자(Primary 버튼, 토스트, 선택된 칩)', ['TEXT_FILL']),
    ('text', 'accent', 'blue.600', 'Blue Ghost·Light Blue 버튼 글자, 오늘 날짜, 입력 중 글자 수', ['TEXT_FILL']),
    ('text', 'error', 'red.500', '입력 오류 안내, 위험 행동 글자(삭제 · 내보내기)', ['TEXT_FILL']),
    ('bg', 'surface', 'gray.0', '화면, 카드, 팝업, 바텀시트 바탕', ['FRAME_FILL', 'SHAPE_FILL']),
    ('bg', 'secondary', 'gray.100', '칩, Box 탭, 목록 카드, 아코디언, 비활성 바탕', ['FRAME_FILL', 'SHAPE_FILL']),
    ('bg', 'inverse', 'gray.900', 'Primary·Floating 버튼', ['FRAME_FILL', 'SHAPE_FILL']),
    ('bg', 'accent', 'blue.600', 'Blue 버튼, 선택된 칩·날짜, 체크된 체크박스·라디오', ['FRAME_FILL', 'SHAPE_FILL']),
    ('bg', 'accent-secondary', 'blue.100', 'Light Blue 버튼, Guide 툴팁', ['FRAME_FILL', 'SHAPE_FILL']),
    ('bg', 'selected', 'blue.200', '아코디언 Index 현재 항목', ['FRAME_FILL', 'SHAPE_FILL']),
    ('bg', 'toast', 'opacity.86', '토스트', ['FRAME_FILL', 'SHAPE_FILL']),
    ('border', 'default', 'gray.300', '입력창, Outlined 버튼 테두리', ['STROKE_COLOR']),
    ('border', 'divider', 'opacity.8', '탭 아래 구분선', ['STROKE_COLOR', 'FRAME_FILL', 'SHAPE_FILL']),
    ('border', 'focus', 'blue.600', '입력창 포커스, 키보드 Focus 표시(2px)', ['STROKE_COLOR']),
    ('overlay', 'dim', 'opacity.72', '모달 뒤 딤드(팝업 · 웹 모달 · 바텀시트) — 흐름을 멈추고 답을 받아야 할 때', ['FRAME_FILL', 'SHAPE_FILL']),
    ('status', 'error', 'red.500', '삭제 아이콘 바탕, 오류 아이콘', ['ALL_FILLS']),
]
color = {'$type': 'color', '$description': 'Palette (Figma collection "Color") and role tokens (collection "Color Role"). ' + PALETTE_NOTE + ' Hover/Pressed are not roles: move one/two palette steps from the default colour (see State).', **pal}
for grp, name, ref, use, scopes in ROLES:
    color.setdefault(grp, {})[name] = {'$value': '{color.' + ref + '}', '$description': use,
                                       '$extensions': fx(f'{grp}/{name}', scopes, f'--color-{grp}-{name}')}

# ── spacing ───────────────────────────────────
SP = {4: 'Stacked 버튼 사이, 아이콘과 글자, 체크박스와 라벨', 8: '칩·버튼 나란히, Side by Side 버튼, 컴포넌트 안 묶음', 12: '탭 사이, 제목과 부제, 숫자 동그라미와 글자',
      16: '카드 안 아이콘과 글자, 입력창 안쪽 위아래', 20: '화면 좌우 여백, 카드·토스트 안쪽 여백', 24: '바텀시트 본문 위아래, 날짜 선택 칸 사이', 32: '섹션 간격(작은): 상단 박스 ↔ 목록처럼 화면의 큰 덩어리 사이', 40: '섹션 간격(큰): 질문 제목 ↔ 선택지처럼 화면의 큰 덩어리 사이'}
spacing = {'$type': 'dimension', '$description': 'Six steps for gap and padding, plus section gaps 32 / 40 between large blocks of a screen. Values such as 13 / 15 / 18 come from fixed component heights and are not tokens.'}
for v, use in SP.items():
    spacing[str(v)] = {'$value': f'{v}px', '$description': use, '$extensions': fx(f'spacing/{v}', ['GAP'], f'--spacing-{v}')}
spacing['screen-x'] = {'$value': '{spacing.20}', '$description': '화면 좌우 여백(버튼 묶음, 바텀시트, 탭, 목록 행)', '$extensions': fx('spacing/screen-x', ['GAP'], '--spacing-screen-x')}


# ── layout ────────────────────────────────────
layout = {'$type': 'dimension', '$description': 'Screen widths, fixed web widths and template margins (Figma collection "Layout"). Start new screens from Template/Web (Type=List · Work) · Template/Mobile.'}
layout['mobile-width'] = {'$value': '375px', '$description': '모바일 기준 화면 너비(375 × 812)', '$extensions': fx('layout/mobile-width', ['WIDTH_HEIGHT'], '--layout-mobile-width')}
layout['web-width'] = {'$value': '1440px', '$description': '웹 기준 화면 너비(1440 × 900)', '$extensions': fx('layout/web-width', ['WIDTH_HEIGHT'], '--layout-web-width')}
layout['lnb'] = {'$value': '284px', '$description': '펼친 LNB 너비 — Web/List', '$extensions': fx('layout/lnb', ['WIDTH_HEIGHT'], '--layout-lnb')}
layout['lnb-folded'] = {'$value': '84px', '$description': '접은 LNB 너비 — Web/Work', '$extensions': fx('layout/lnb-folded', ['WIDTH_HEIGHT'], '--layout-lnb-folded')}
layout['card-column'] = {'$value': '296px', '$description': '웹 카드 · 목록 열 너비', '$extensions': fx('layout/card-column', ['WIDTH_HEIGHT'], '--layout-card-column')}
layout['side-panel'] = {'$value': '306px', '$description': 'Web/List 오른쪽 패널 너비(실행목표)', '$extensions': fx('layout/side-panel', ['WIDTH_HEIGHT'], '--layout-side-panel')}
layout['margin-list'] = {'$value': '{spacing.40}', '$description': 'Web/List 본문 좌우 여백 · 열 사이', '$extensions': fx('layout/margin-list', ['GAP'], '--layout-margin-list')}
layout['margin-work'] = {'$value': '{spacing.20}', '$description': 'Web/Work 여백 · 목록과 작업 패널 사이', '$extensions': fx('layout/margin-work', ['GAP'], '--layout-margin-work')}
layout['panel-padding'] = {'$value': '{spacing.40}', '$description': 'Web/Work 작업 패널 안쪽 좌우', '$extensions': fx('layout/panel-padding', ['GAP'], '--layout-panel-padding')}

# ── radius ────────────────────────────────────
radius = {'$type': 'dimension', '$description': 'Seven steps; the bigger the surface, the rounder the corner. Usage names point at a step.'}
for v, use in [(4, '체크박스, 삭제 아이콘 바탕'), (6, '작은 칩(38)'), (8, '칩 48, Box 탭, 툴팁, 목록 카드'), (10, '버튼 40'), (12, '버튼 48, 입력창, 카드, 토스트, 아코디언'), (20, '웹 모달'), (16, '팝업, 바텀시트(위 모서리)')]:
    radius[str(v)] = {'$value': f'{v}px', '$description': use, '$extensions': fx(f'radius/{v}', ['CORNER_RADIUS'], f'--radius-{v}')}
radius['full'] = {'$value': '999px', '$description': '원·알약 모양', '$extensions': fx('radius/full', ['CORNER_RADIUS'], '--radius-full')}
for n, ref, use in [('button', '12', '버튼 48'), ('button-sm', '10', '버튼 40'), ('button-xs', '8', '버튼 36(웹), Dropdown'), ('chip', '8', '칩 버튼 48'), ('chip-sm', '6', '칩 버튼 38'), ('field', '12', '입력창·선택창'),
                    ('card', '12', 'Two Choice 카드, 아코디언'), ('toast', '12', '토스트'), ('tooltip', '8', '툴팁'), ('list-card', '8', '아이콘 리스트 카드'),
                    ('checkbox', '4', '체크박스'), ('card-lg', '16', '웹의 넓은 섹션 카드(본문 928)'), ('modal', '16', '팝업, 바텀시트·날짜 선택(위 모서리)'), ('modal-lg', '20', '웹 모달(Modal (Web))'), ('pill', 'full', 'Floating 버튼, 아바타, 라디오, 날짜 칸, 진행 바, 스크롤 바')]:
    radius[n] = {'$value': '{radius.' + ref + '}', '$description': use, '$extensions': fx(f'radius/{n}', ['CORNER_RADIUS'], f'--radius-{n}')}

# ── typography ────────────────────────────────
font = {
    'family': {'$type': 'fontFamily', 'primary': {'$value': ['Pretendard', '-apple-system', 'BlinkMacSystemFont', 'Apple SD Gothic Neo', 'sans-serif']}},
    'weight': {'$type': 'fontWeight', 'medium': {'$value': 500}, 'semibold': {'$value': 600}, 'bold': {'$value': 700}},
}
TY = [('heading', '28-bold', 28, 'bold', 1.5, '웹 페이지 제목(1440)'), ('heading', '24-bold', 24, 'bold', 1.5, '홈 앱 바 제목'), ('title', '20-bold', 20, 'bold', 1.4, '바텀시트 큰 제목'), ('title', '18-bold', 18, 'bold', 1.4, '팝업 제목, 같은 너비 탭'),
      ('title', '22-bold', 22, 'bold', 1.4, '웹 모달 제목'), ('title', '16-bold', 16, 'bold', 1.4, '바텀시트 헤더 제목'), ('title', '15-bold', 15, 'bold', 1.4, '웹 섹션 제목, 웹 회고 카드 제목'), ('title', '14-bold', 14, 'bold', 1.4, '웹 소제목, 접기 제목, 이전/다음, 템플릿 카드 제목'), ('subtitle', '18-semibold', 18, 'semibold', 1.4, 'Text 탭, 서브 앱 바 제목, 달력 월'),
      ('subtitle', '16-semibold', 16, 'semibold', 1.4, '버튼 48, 아코디언 제목'), ('subtitle', '14-semibold', 14, 'semibold', 1.4, '버튼 40, 칩 38, Box 탭, 입력창 라벨'),
      ('body', '16-medium', 16, 'medium', 1.4, '칩 버튼 48, 토스트, 팝업 부제'), ('body', '15-medium', 15, 'medium', 1.4, '입력 글자, 체크박스 라벨, 날짜'), ('body', '15-medium-long', 15, 'medium', 1.8, '긴 글 읽기(회고 답변 카드 본문)'),
      ('body', '14-medium', 14, 'medium', 1.4, '목록 카드, 아코디언 내용, 오류 안내'), ('body', '13-medium', 13, 'medium', 1.4, '카드 설명(스페이스 카드)'), ('body', '12-semibold', 12, 'semibold', 1.4, '툴팁, 아코디언 번호'),
      ('body', '12-medium', 12, 'medium', 1.4, '글자 수, Guide 툴팁 본문'), ('caption', '11-semibold', 11, 'semibold', 1.4, 'Badge Outlined 상태 태그'), ('caption', '11-medium', 11, 'medium', 1.4, 'Navigation Bar 라벨'),
      ('caption', '10-bold', 10, 'bold', 1.4, '목록 카드 번호 동그라미'), ('caption', '10-medium', 10, 'medium', 1.4, '')]
typography = {'$type': 'typography', '$description': 'Text styles (Figma local text styles, same names). Letter spacing 0.'}
for grp, name, size, w, lh, use in TY:
    style = grp.capitalize() + '/' + name.split('-')[0] + ' ' + {'bold': 'Bold', 'semibold': 'SemiBold', 'medium': 'Medium'}[w] + (' Long' if name.endswith('-long') else '')
    tok = {'$value': {'fontFamily': '{font.family.primary}', 'fontWeight': '{font.weight.' + w + '}', 'fontSize': f'{size}px', 'lineHeight': lh, 'letterSpacing': '0px'},
           '$extensions': {'com.figma': {'textStyle': style}, 'web': {'class': f'.text-{grp}-{name}'}}}
    if use: tok['$description'] = use
    typography.setdefault(grp, {})[name] = tok

# ── shadow ────────────────────────────────────
def sh(y, blur, a):
    return {'color': f'#06080C{round(a * 255):02X}', 'offsetX': '0px', 'offsetY': f'{y}px', 'blur': f'{blur}px', 'spread': '0px'}
shadow = {'$type': 'shadow', '$description': 'Elevation (Figma local effect styles Shadow/100–400).',
          '100': {'$value': [sh(4, 12, .04)], '$extensions': {'com.figma': {'effectStyle': 'Shadow/100'}, 'web': {'css': 'var(--shadow-100)'}}},
          '200': {'$value': [sh(4, 8, .12), sh(1, 4, .08)], '$extensions': {'com.figma': {'effectStyle': 'Shadow/200'}, 'web': {'css': 'var(--shadow-200)'}}},
          '300': {'$value': [sh(4, 12, .12), sh(4, 8, .08)], '$extensions': {'com.figma': {'effectStyle': 'Shadow/300'}, 'web': {'css': 'var(--shadow-300)'}}},
          '400': {'$value': [sh(4, 12, .22), sh(4, 8, .08)], '$extensions': {'com.figma': {'effectStyle': 'Shadow/400'}, 'web': {'css': 'var(--shadow-400)'}}},
          'card': {'$value': '{shadow.100}', '$description': '카드'},
          'floating-button': {'$value': '{shadow.200}', '$description': 'Floating 버튼'},
          'layer': {'$value': '{shadow.300}', '$description': '화면 위에 겹치는 층'},
          'modal': {'$value': '{shadow.400}', '$description': '팝업, 바텀시트'}}

# ── focus ring (code only) ────────────────────
focus = {'ring': {'$type': 'border', '$value': {'color': '{color.border.focus}', 'width': '2px', 'style': 'solid'},
                  '$description': '키보드 Focus 표시(코드 전용). 떨어진 요소는 바깥 2px, 탭·내비게이션은 안쪽 2px.'}}

T.update({'color': color, 'spacing': spacing, 'layout': layout, 'radius': radius, 'font': font, 'typography': typography, 'shadow': shadow, 'focus': focus})

# validate references
flat = {}
def walk(o, path):
    if isinstance(o, dict):
        if '$value' in o: flat['.'.join(path)] = o['$value']
        for k, v in o.items():
            if not k.startswith('$'): walk(v, path + [k])
walk(T, [])
bad = []
def refs(v):
    if isinstance(v, str): return re.findall(r'\{([^}]+)\}', v)
    if isinstance(v, dict): return sum((refs(x) for x in v.values()), [])
    if isinstance(v, list): return sum((refs(x) for x in v), [])
    return []
for k, v in flat.items():
    for r in refs(v):
        if r not in flat: bad.append((k, r))
out = F / 'tokens.json'
out.write_text(json.dumps(T, ensure_ascii=False, indent=2) + '\n')
print('tokens', len(flat), 'bad refs', bad, out)
