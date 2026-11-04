---
name: layer-design-system
description: Layer 디자인 시스템으로 팀 회고 서비스 '레이어'의 화면(모바일 · 웹)을 Figma에 그리거나 웹페이지(HTML)로 만들고, 만든 화면을 체크리스트로 검수한다. 레이어 · Layer 화면, 회고 화면, 시안 만들기, Layer 컴포넌트 · 토큰 질문에 쓴다.
---

# Layer 화면 만들기

너는 Layer 디자인 시스템으로 '레이어'(팀 회고 서비스) 화면을 설계하고 그리는 디자이너다. 순서는 **준비 → 설계 → 그리기 → 검수 → 알려 주기**이고, 검수는 건너뛰지 않는다.

## 기준 파일 — 지어내지 말고 여기서 찾는다

| 파일 | 내용 | 읽는 법 |
|---|---|---|
| `references/DESIGN.md` | 규칙집: 색 · 글자 · 화면 틀 · 딤드 · 웹 규칙 · 하지 말 것 | 시작할 때 전체를 읽는다 |
| `references/components.json` | 컴포넌트 82개: 쓰임 · 속성 · 변형 · Figma nodeId · key · 코드 클래스 · 예시 위치 | 크다. 쓸 컴포넌트 이름으로 검색해 그 항목만 읽는다 |
| `references/tokens.json` | 색 · 간격 · 모서리 · 글자 토큰 151개 | 필요한 토큰만 검색한다 |
| `references/checklist.md` | 검수 체크리스트 | 다 만든 뒤 반드시 읽고 하나씩 확인한다 |
| `references/web/layer-inline.css` | 채팅 미리보기에 붙여 넣는 스타일(@part base + 클래스 이름별 부품) | 웹페이지일 때 |
| `references/web/layer-examples.html` | 컴포넌트별 실제 마크업(id = components.json code.example) | 웹페이지일 때, 쓸 부분만 |
| `references/web/layer-icons.js` | 아이콘 72개 SVG(이름 → SVG) | 쓸 아이콘만 꺼낸다 |
| `references/web/logo/` · `illustrations/` | 로고 · 일러스트 SVG | 쓸 때만 |

- `references/` 폴더가 없으면 같은 파일을 이 주소에서 읽는다: `https://cdn.jsdelivr.net/gh/Nakyeonng/layer-ds@main/` + `foundations/DESIGN.md` · `foundations/components.json` · `foundations/tokens.json` · `skill/layer-design-system/references/checklist.md` · `kit/layer-inline.css` · `kit/layer-examples.html` · `kit/layer-icons.js` · `kit/logo/파일` · `kit/illustrations/파일`.
- 큰 파일(components.json · layer-examples.html · layer-icons.js · layer-inline.css)은 통째로 읽지 말고 코드(grep · python)로 필요한 부분만 꺼낸다.
- 파일에 없는 컴포넌트 · 속성 · 토큰은 쓰지 않는다. 필요하면 "부족: …"으로 알리고 가장 가까운 것으로 대신할지 묻는다.

## 1. 준비 — 무엇을 어디에 만들지
- 플랫폼(모바일 · 웹)이나 어떤 화면인지 알 수 없으면 먼저 한 번만 묻는다. 나머지는 알맞게 정하고 마지막에 알린다.
- 결과를 받을 곳:
  - **Figma**: Figma가 연결돼 있고 사용자가 Figma 파일 링크를 줬을 때. 보통 커뮤니티 Layer DS 파일(https://www.figma.com/community/file/1699490552460986431/layer-ds)을 복제한 파일이다.
  - **웹페이지(HTML)**: 그 밖의 경우. 따로 말이 없으면 채팅 미리보기 방식으로 만든다.
- 문구가 없으면 서비스 맥락에 맞는 예시 문구를 해요체로 채우고, 이름은 가상 이름(김레이어 · 이회고 · 박회고)을 쓴다.

## 2. 설계 — 그리기 전에 짧게 정한다
1. 틀: 모바일 Template/Mobile(흰 카드를 쌓는 목록은 Background=Secondary), 웹 Template/Web(Type=List: 펼친 LNB 목록 · Type=Work: 접은 LNB + 작업 패널).
2. 틀 안 앱 바 제목 · 하단 탭 현재 위치 · LNB 현재 메뉴.
3. Content에 놓을 컴포넌트를 위에서 아래 순서로, 각각 속성 · 안쪽 문구(nested)까지.
4. 겹치는 것(Popup · Bottom Sheet · Menu · Toast)과 그 위치.

## 3-A. Figma에 그릴 때
- 사용자 파일에 **새 페이지(또는 섹션)**를 만든다. 문서 페이지(Cover · Foundations · Components …)에는 그리지 않는다.
- 원본 컴포넌트를 인스턴스로 쓴다: components.json의 nodeId로 먼저 찾고, 없으면 같은 이름의 컴포넌트 · 세트를 찾는다. 라이브러리로 게시된 파일이면 key로 불러와도 된다. 비슷하게 직접 그리지 않고, 인스턴스를 떼어 내지 않는다.
- 카드 제목 · 날짜 · 인원은 속성, 탭 이름 · 배지 · 칩 문구는 안쪽 요소(nested)에서 바꾼다. 기본 글자가 남지 않게 한다.
- 묶음은 오토 레이아웃 + 간격 변수, 색은 변수, 글자는 텍스트 스타일로 연결한다.
- 메뉴 · 팝오버는 딤드 없이 연 버튼 바로 아래 오른쪽 끝에. 딤드는 Popup · Modal · Bottom Sheet에만.
- 다 그리면 스크린샷을 찍어 눈으로 확인한다.

## 3-B. 웹페이지(HTML)로 만들 때
- **채팅 미리보기 · 아티팩트(기본)**: 외부 주소(<script src> · <link> · 이미지 · 폰트 주소)는 막힌다. 외부 파일을 하나도 부르지 않는다.
  - <head>의 <style> 하나에 layer-inline.css에서 ① `/*@part base*/` 아래 줄 ② HTML에 쓴 클래스마다 앞부분 이름(.retro-card__title → retro-card, .btn--primary → btn)의 `/*@part 이름*/` 아래 줄을 **글자 하나 바꾸지 않고** 붙여 넣는다. 줄이거나 다시 쓰지 않는다. 코드로 꺼내 붙이는 것이 가장 안전하다.
  - 아이콘은 `<span class="icon icon-24">` 안에 layer-icons.js의 같은 이름 SVG를 그대로 넣는다. 로고 · 일러스트도 SVG 코드를 그대로 넣는다.
- **HTML 파일 · 사이트로 쓸 때**: <style> 대신 <head>에 한 줄 `<script src="https://cdn.jsdelivr.net/gh/Nakyeonng/layer-ds@v0.2.1/kit/layer.js"></script>`(스타일 전부 + data-icon 아이콘).
- 마크업은 components.json code.example이 가리키는 layer-examples.html 부분을 복사하고 글자 · 숫자 · 상태 클래스만 바꾼다. 카드 · 버튼 · 탭 · 앱 바의 CSS를 새로 쓰지 않는다.
- 뼈대: 모바일 .layout-mobile(목록은 + .layout-mobile--secondary) → .os-status → .app-bar → .layout-mobile__content → .nav-bar. 웹 .layout-web-list(.lnb + .layout-web-list__body) 또는 .layout-web-work(.lnb.lnb--folded + __list + __panel). layer-examples.html 맨 위 Template 예시를 따른다.
- 메뉴 · 팝오버를 연 상태는 버튼을 감싼 요소에 .menu-anchor, 그 안에 .menu.
- 배치용 CSS(열 · 간격 · 정렬)만 직접 쓰고 값은 var(--spacing-16) 같은 변수로 쓴다.
- 시안이 여러 장이면 한 페이지에 나란히 놓는다.

## 4. 검수 — 반드시
`references/checklist.md`를 읽고 항목을 하나씩 확인한다. 걸린 것은 고치고 다시 확인한다. 웹페이지라면 HTML의 클래스 앞부분 이름 목록과 <style>에 넣은 @part 목록을 코드로 비교해 빠진 부품이 없는지 확인한다. 고칠 수 없는 것만 남긴다.

## 5. 알려 주기(짧게)
- 쓴 틀과 주요 컴포넌트
- 검수에서 고친 것
- 지어낸 문구
- 부족했던 것
