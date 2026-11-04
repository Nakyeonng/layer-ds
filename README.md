# Layer Design System

팀 회고 서비스 **레이어**의 디자인 시스템입니다. 모바일(375) · 웹(1440), 라이트 모드.
디자이너 · 개발자 · AI가 같은 이름으로 같은 값을 쓰도록 만든 토큰 · 컴포넌트 · 화면 틀과 AI용 파일을 담았습니다.

- **Figma 커뮤니티 파일**: https://www.figma.com/community/file/1699490552460986431/layer-ds
- **사용 조건**: [LICENSE.md](LICENSE.md) — 쓰기는 허용, 재배포 · 판매 금지

## 웹 키트 바로 쓰기 (jsDelivr)

```html
<!-- <head>에 한 줄: 스타일(layer.css 전체) + 아이콘 -->
<script src="https://cdn.jsdelivr.net/gh/Nakyeonng/layer-ds@v0.2.1/kit/layer.js"></script>
```

HTML 파일 · 사이트용입니다. Claude 채팅 아티팩트처럼 외부 주소를 모두 막는 미리보기에서는 [`kit/layer-inline.css`](kit/layer-inline.css)의 `@part base` + 쓰는 부품 줄을 `<style>`에 그대로 붙여 넣습니다. 일반 웹페이지라면 `<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Nakyeonng/layer-ds@v0.2.1/kit/layer.css">` + `layer-icons.js`도 됩니다.

- 컴포넌트 마크업: [`kit/layer-examples.html`](kit/layer-examples.html)을 복사해 글자만 바꿉니다.
- 아이콘: `<span class="icon icon-24" data-icon="add"></span>`
- 화면 뼈대: `.layout-mobile` · `.layout-web-list` · `.layout-web-work`

## 폴더

| 폴더 | 내용 |
|---|---|
| `kit/` | 웹 키트 — layer-inline.css(붙여 넣기용) · layer.js · layer.css · layer-icons.js · layer-examples.html · logo · illustrations · fonts |
| `skill/` | Claude Skill — layer-design-system(SKILL.md · 검수 체크리스트 · 자료). 폴더째 ZIP으로 묶어 Claude 설정 → 기능 → Skills에 올린다 |
| `site/` | 문서 사이트(정적 HTML)와 `downloads/`(DESIGN.md · components.json · tokens.json · AI 안내문) |
| `foundations/` | 토큰 · CSS 원본, 아이콘 · 로고 · 일러스트 원본 |
| `src/` | 위 파일을 만드는 스크립트, `src/data/figma_components.json`(Figma 컴포넌트 목록 스냅샷) |

## 다시 만들기 · 업데이트 순서

```bash
pip install beautifulsoup4
VERSION=0.2.1 ./build_all.sh
```

1. Figma 원본 파일을 고친다 → 커뮤니티 파일 **Publish update**
2. 컴포넌트 속성이 바뀌었으면 `src/data/figma_components.json`을 갱신한다
3. `VERSION=x.y.z ./build_all.sh` — AI 파일 · 웹 키트 · 사이트 · llms.txt를 다시 만든다
4. 커밋 → 태그 `vx.y.z` 푸시 → jsDelivr 주소의 버전을 올린다
5. 문서 사이트를 다시 게시한다
