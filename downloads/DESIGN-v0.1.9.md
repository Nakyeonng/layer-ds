---
version: alpha
name: Layer
description: 회고 앱 "레이어"의 모바일 디자인 시스템 (라이트 모드, 375 기준)
colors:
  primary: "#212329"
  on-primary: "#ffffff"
  accent: "#6c9cfa"
  surface: "#ffffff"
  on-surface: "#212329"
  error: "#f03e3e"
  text-primary: "#212329"
  text-secondary: "#666b75"
  text-tertiary: "#a9afbb"
  text-disabled: "#ced2da"
  text-inverse: "#ffffff"
  text-accent: "#6c9cfa"
  text-error: "#f03e3e"
  bg-surface: "#ffffff"
  bg-secondary: "#f2f4f8"
  bg-inverse: "#212329"
  bg-accent: "#6c9cfa"
  bg-accent-secondary: "#e9f0ff"
  bg-selected: "#e2ebfe"
  bg-toast: "#06080cdb"
  border-default: "#dfe3ea"
  border-divider: "#06080c14"
  border-focus: "#6c9cfa"
  overlay-dim: "#06080cb8"
  status-error: "#f03e3e"
  gray-300: "#dfe3ea"
  gray-400: "#ced2da"
  gray-600: "#8b909c"
  gray-700: "#666b75"
  gray-800: "#454952"
typography:
  heading-28-bold:
    fontFamily: Pretendard
    fontSize: 28px
    fontWeight: 700
    lineHeight: 1.5
    letterSpacing: 0px
  heading-24-bold:
    fontFamily: Pretendard
    fontSize: 24px
    fontWeight: 700
    lineHeight: 1.5
    letterSpacing: 0px
  title-20-bold:
    fontFamily: Pretendard
    fontSize: 20px
    fontWeight: 700
    lineHeight: 1.4
    letterSpacing: 0px
  title-18-bold:
    fontFamily: Pretendard
    fontSize: 18px
    fontWeight: 700
    lineHeight: 1.4
    letterSpacing: 0px
  title-22-bold:
    fontFamily: Pretendard
    fontSize: 22px
    fontWeight: 700
    lineHeight: 1.4
    letterSpacing: 0px
  title-16-bold:
    fontFamily: Pretendard
    fontSize: 16px
    fontWeight: 700
    lineHeight: 1.4
    letterSpacing: 0px
  title-15-bold:
    fontFamily: Pretendard
    fontSize: 15px
    fontWeight: 700
    lineHeight: 1.4
    letterSpacing: 0px
  title-14-bold:
    fontFamily: Pretendard
    fontSize: 14px
    fontWeight: 700
    lineHeight: 1.4
    letterSpacing: 0px
  subtitle-18-semibold:
    fontFamily: Pretendard
    fontSize: 18px
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: 0px
  subtitle-16-semibold:
    fontFamily: Pretendard
    fontSize: 16px
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: 0px
  subtitle-14-semibold:
    fontFamily: Pretendard
    fontSize: 14px
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: 0px
  body-16-medium:
    fontFamily: Pretendard
    fontSize: 16px
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: 0px
  body-15-medium:
    fontFamily: Pretendard
    fontSize: 15px
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: 0px
  body-15-medium-long:
    fontFamily: Pretendard
    fontSize: 15px
    fontWeight: 500
    lineHeight: 1.8
    letterSpacing: 0px
  body-14-medium:
    fontFamily: Pretendard
    fontSize: 14px
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: 0px
  body-13-medium:
    fontFamily: Pretendard
    fontSize: 13px
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: 0px
  body-12-semibold:
    fontFamily: Pretendard
    fontSize: 12px
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: 0px
  body-12-medium:
    fontFamily: Pretendard
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: 0px
  caption-11-semibold:
    fontFamily: Pretendard
    fontSize: 11px
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: 0px
  caption-11-medium:
    fontFamily: Pretendard
    fontSize: 11px
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: 0px
  caption-10-bold:
    fontFamily: Pretendard
    fontSize: 10px
    fontWeight: 700
    lineHeight: 1.4
    letterSpacing: 0px
  caption-10-medium:
    fontFamily: Pretendard
    fontSize: 10px
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: 0px
rounded:
  r4: 4px
  r6: 6px
  r8: 8px
  r10: 10px
  r12: 12px
  r20: 20px
  r16: 16px
  full: 999px
  button: 12px
  button-sm: 10px
  button-xs: 8px
  chip: 8px
  chip-sm: 6px
  field: 12px
  card: 12px
  toast: 12px
  tooltip: 8px
  list-card: 8px
  checkbox: 4px
  card-lg: 16px
  modal: 16px
  modal-lg: 20px
  pill: 999px
spacing:
  s4: 4px
  s8: 8px
  s12: 12px
  s16: 16px
  s20: 20px
  s24: 24px
  s32: 32px
  s40: 40px
  screen-x: 20px
  screen-width: 375px
  layout-margin-list: 40px
  layout-margin-work: 20px
  layout-panel-padding: 40px
  layout-lnb: 284px
  layout-lnb-folded: 84px
  layout-card-column: 296px
  layout-side-panel: 306px
  web-width: 1440px
components:
  button-primary:
    backgroundColor: "{colors.bg-inverse}"
    textColor: "{colors.text-inverse}"
    typography: "{typography.subtitle-16-semibold}"
    rounded: "{rounded.button}"
    height: 48px
    padding: 13px 20px
  button-primary-hover:
    backgroundColor: "{colors.gray-800}"
  button-primary-pressed:
    backgroundColor: "{colors.gray-700}"
  button-primary-disabled:
    backgroundColor: "{colors.bg-secondary}"
    textColor: "{colors.text-disabled}"
  button-secondary:
    backgroundColor: "{colors.gray-300}"
    textColor: "{colors.text-primary}"
    rounded: "{rounded.button}"
    height: 48px
  button-blue:
    backgroundColor: "{colors.bg-accent}"
    textColor: "{colors.text-inverse}"
    rounded: "{rounded.button}"
    height: 48px
  button-light-blue:
    backgroundColor: "{colors.bg-accent-secondary}"
    textColor: "{colors.text-accent}"
    rounded: "{rounded.button}"
    height: 48px
  button-small:
    typography: "{typography.subtitle-14-semibold}"
    rounded: "{rounded.button-sm}"
    height: 40px
    padding: 10px 16px
  button-xsmall:
    typography: "{typography.subtitle-14-semibold}"
    rounded: "{rounded.button-xs}"
    height: 36px
    padding: 8px 12px
  button-ghost:
    backgroundColor: "{colors.bg-surface}"
    textColor: "{colors.text-primary}"
    rounded: "{rounded.button}"
    height: 48px
  button-floating:
    backgroundColor: "{colors.bg-inverse}"
    textColor: "{colors.text-inverse}"
    typography: "{typography.subtitle-14-semibold}"
    rounded: "{rounded.pill}"
    height: 48px
  chip:
    backgroundColor: "{colors.bg-secondary}"
    textColor: "{colors.gray-800}"
    typography: "{typography.body-16-medium}"
    rounded: "{rounded.chip}"
    height: 48px
    padding: 13px 20px
  chip-selected:
    backgroundColor: "{colors.bg-accent}"
    textColor: "{colors.text-inverse}"
  chip-small:
    typography: "{typography.subtitle-14-semibold}"
    rounded: "{rounded.chip-sm}"
    height: 38px
  choice-card:
    backgroundColor: "{colors.bg-secondary}"
    typography: "{typography.body-16-medium}"
    rounded: "{rounded.card}"
    height: 163px
  input-field:
    backgroundColor: "{colors.bg-surface}"
    textColor: "{colors.text-primary}"
    typography: "{typography.body-15-medium}"
    rounded: "{rounded.field}"
    padding: 15px 13px
  tab-text:
    textColor: "{colors.text-tertiary}"
    typography: "{typography.subtitle-18-semibold}"
    height: 52px
  tab-text-selected:
    textColor: "{colors.text-primary}"
  tab-box:
    backgroundColor: "{colors.bg-secondary}"
    textColor: "{colors.gray-800}"
    typography: "{typography.subtitle-14-semibold}"
    rounded: "{rounded.r8}"
    height: 38px
  tab-box-selected:
    backgroundColor: "{colors.gray-800}"
    textColor: "{colors.text-inverse}"
  list-card:
    backgroundColor: "{colors.bg-secondary}"
    typography: "{typography.body-14-medium}"
    rounded: "{rounded.list-card}"
    padding: 15px 12px
  popup:
    backgroundColor: "{colors.bg-surface}"
    rounded: "{rounded.modal}"
    width: 315px
    padding: 30px 20px 20px
  bottom-sheet:
    backgroundColor: "{colors.bg-surface}"
    rounded: "{rounded.modal}"
    width: 375px
  toast:
    backgroundColor: "{colors.bg-toast}"
    textColor: "{colors.text-inverse}"
    typography: "{typography.body-16-medium}"
    rounded: "{rounded.toast}"
    width: 335px
    padding: 18px 20px
  tooltip:
    backgroundColor: "{colors.bg-accent}"
    textColor: "{colors.text-inverse}"
    typography: "{typography.body-12-semibold}"
    rounded: "{rounded.tooltip}"
    padding: 10px 14px
  app-bar:
    backgroundColor: "{colors.bg-surface}"
    textColor: "{colors.text-primary}"
    typography: "{typography.subtitle-18-semibold}"
    height: 58px
  navigation-bar:
    backgroundColor: "{colors.bg-surface}"
    textColor: "{colors.gray-600}"
    typography: "{typography.caption-11-medium}"
    height: 54px
  badge:
    backgroundColor: "{colors.bg-accent-secondary}"
    textColor: "{colors.text-accent}"
    typography: "{typography.body-12-semibold}"
    rounded: "{rounded.r4}"
    height: 22px
    padding: 0 6px
  badge-white:
    backgroundColor: "{colors.bg-surface}"
    textColor: "{colors.text-accent}"
  badge-gray:
    backgroundColor: "{colors.bg-secondary}"
    textColor: "{colors.gray-800}"
    height: 25px
    padding: 4px 8px
  avatar:
    backgroundColor: "{colors.gray-400}"
    rounded: "{rounded.pill}"
    size: 32px
---

# Layer Design System

> 이 파일은 AI 에이전트와 사람이 같이 읽는 레이어 디자인 시스템 요약입니다. 위 YAML의 colors에는 역할 토큰과 컴포넌트가 쓰는 팔레트 단계만 넣었고, 전체 팔레트 55색은 tokens.json에 있습니다. 정확한 값은 `layer-tokens-v0.1.9.json`, Figma 컴포넌트 키와 속성은 `components.json`에 있습니다. **Figma 작업에서는 컴포넌트를 새로 그리지 말고 `components.json`의 라이브러리 인스턴스를 불러와 쓰세요.**

## Overview

레이어는 팀과 개인이 회고를 쓰고, 실행 목표를 정하고, 결과를 분석하는 모바일 앱입니다. 화면은 **차분하고 정돈된** 인상을 줍니다. 흰 바탕 위에 짙은 회색 글자와 버튼을 쓰고, 파란색(Blue 600)은 선택과 강조에만 아껴 씁니다. 장식은 일러스트가 맡고, UI 자체는 단순한 면과 넉넉한 여백으로 구성합니다.

- 기준 화면: iPhone 375 × 812, 라이트 모드만
- 글꼴: Pretendard 한 가지
- 말투: 부드러운 해요체 ("회고를 저장했어요", "작성을 그만둘까요?")

## Colors

색은 **역할 이름**으로 고릅니다. 팔레트 단계(gray-500 등)는 역할이 없는 곳과 Hover·Pressed에서만 씁니다.

- **글자:** `text-primary`(Gray 900) 제목·본문 · `text-secondary`(Gray 700) 보조 · `text-tertiary`(Gray 500) 안내 문구·선택 안 된 탭 · `text-disabled`(Gray 400) · `text-inverse`(흰색, 진한 바탕 위) · `text-accent`(Blue 600) · `text-error`(Red 500, 입력 오류 · 위험 행동)
- **바탕:** `bg-surface`(흰색) 화면·카드·모달 · `bg-secondary`(Gray 100) 칩·탭·목록 카드·비활성 · `bg-inverse`(Gray 900) Primary 버튼 · `bg-accent`(Blue 600) 선택·Blue 버튼 · `bg-accent-secondary`(Blue 100) · `bg-selected`(Blue 200) · `bg-toast`(86% 검정)
- **테두리:** `border-default`(Gray 300) 입력창 · `border-divider`(8% 검정) · `border-focus`(Blue 600)
- **딤드:** `overlay-dim`(72% 검정)은 모달 뒤(팝업 · 웹 모달 · 바텀시트 — 흐름을 멈추고 답을 받을 때)에만. 드롭다운 · 더보기로 여는 **Popover · Menu는 딤드 없이** 그림자(Shadow 300)로만 띄운다.
- **기타:** `status-error`(Red 500) 삭제·오류. 오류 · 위험 색은 Red 500 하나.

**상태 규칙:** Hover는 기본색에서 팔레트 한 단계, Pressed는 두 단계 옮깁니다(밝은 색은 진해지고, Gray 900은 800 → 700으로 밝아짐). Disabled는 `bg-secondary` + `text-disabled`.

## Typography

Pretendard 하나로 15단계를 씁니다. 행간은 140%(Heading 24만 150%), 자간 0.

- **Heading 24 Bold:** 홈 앱 바 제목
- **Title 20 / 18 / 16 Bold:** 바텀시트 큰 제목 / 팝업 제목·같은 너비 탭 / 바텀시트 헤더
- **Subtitle 18 / 16 / 14 SemiBold:** 글자 탭·서브 앱 바 제목 / 버튼 48 / 버튼 40·칩 38·입력창 라벨
- **Body 16 / 15 / 14 / 12 Medium, 12 SemiBold:** 칩·토스트·팝업 부제 / 입력 글자·체크박스 라벨 / 목록·아코디언 내용 / 글자 수 / 툴팁
- **Caption 11 Medium, 10 Bold:** 내비게이션 라벨 / 번호 동그라미

## Layout

**새 화면은 반드시 템플릿에서 시작한다.** 템플릿 안의 앱 바 · 내비게이션 · LNB는 **노출된 인스턴스(nested)**라서 템플릿 인스턴스에서 바로 속성(Title · Style · On · Current)을 바꾼다. 컴포넌트 안의 탭 이름 · 배지 문구 · 빈 상태 문구도 components.json의 `nested`에 적힌 대로 안쪽 인스턴스 속성으로 바꾼다.
- 흰 카드(Shadow 100)를 쌓는 모바일 목록 화면은 `Template/Mobile` **Background=Secondary**(Gray 100). 그 밖은 Surface.
- 목록 · 열 위 제목과 개수는 **Section Header**(Size=16 웹 · 18 모바일). 개수를 Badge로 만들지 않는다. Figma `Template/Web`(Type=List · Work) · `Template/Mobile` 인스턴스를 놓고 슬롯에 내용을 채운다. LNB · 앱 바 · 여백의 위치를 직접 계산하지 않는다. 값은 `layout.*` 토큰, 가이드는 그리드 스타일 `Layout/*`.

- **Web/List**(목록 · 대시보드: 스페이스, 모달 뒤 배경): 펼친 LNB **284** + 본문 여백 **40**(`layout-margin-list`, 위 28). 카드 열 **296**(`layout-card-column`) × n, 열 사이 40, 오른쪽 패널 **306**(`layout-side-panel`). 넓어진 본문은 **열과 패널 사이 간격**으로 흡수(패널은 오른쪽 정렬, 너비 고정).
- **Web/Work**(작성 · 분석: 목록을 보며 오른쪽에서 작업): 접은 LNB **84** + 여백 **20**(`layout-margin-work`) + 목록 열 296 + 사이 20 + 작업 패널(남은 너비, 화면 오른쪽 끝에 붙는 흰 시트, 안쪽 좌우 **40** `layout-panel-padding`, 위아래 24).
- **Mobile**: 기준 기기 **375 × 812**(393 상태 바는 시스템 영역 예시일 뿐). 위에서부터 상태 바 44 → 앱 바 58(Show App Bar) → 본문(좌우 20) → Navigation Bar 88(Show Navigation Bar) 또는 Button Group.
- 웹 홈 대시보드(빈 상태)는 본문 가운데 정렬(최대 928)로, 아직 템플릿 밖의 예외.
- 웹은 형태가 다양하다. 두 Type에 맞지 않는 새 형태가 반복되면 템플릿 밖에서 화면을 짜지 말고 **`Template/Web`에 Type을 추가**해 값(LNB 상태 · 여백 · 열)을 정한 뒤 쓴다.
- 화면 너비 **375**, 좌우 여백 **20**(`screen-x`). 화면의 큰 덩어리 사이(제목 ↔ 선택지, 상단 박스 ↔ 목록)는 **32 · 40**(섹션 간격), 그 밖의 간격은 4~24. 카드·토스트·팝업 안 콘텐츠 너비는 **335**.
- OS 상태 바 · 홈 표시줄(App Bar/OS Bar, Status/Safe Area)은 iOS·Android가 그리는 시스템 영역. 안의 부품(Time · Home Indicator 등)은 플랫폼 키트에서 가져온 **원격 인스턴스를 그대로 쓴다** — 로컬 컴포넌트로 교체하거나 토큰에 연결하지 않으며, 원격 인스턴스 점검에서 예외.
- 위에서 아래로: OS 상태 바(44) → 앱 바(58) → 본문 → 하단 CTA(Button Group, 안전 영역 34 포함) 또는 Navigation Bar.
- 간격은 **4 · 8 · 12 · 16 · 20 · 24** 여섯 단계. 가까운 관계일수록 좁게: 아이콘과 글자 4~8, 나란한 칩·버튼 8, 제목과 부제 12, 묶음 사이 16~24.
- 여백이 0인 쪽은 토큰 없이 0으로 둔다(spacing 토큰은 4부터).
- 13 · 15 · 18 같은 값은 버튼·입력창 높이를 맞추려고 컴포넌트 안에서 생긴 값이라 화면에 직접 쓰지 않습니다.
- Don't: 웹 본문에 여백 18 · 28 · 30 · 68처럼 템플릿에 없는 값을 쓰지 않는다. Web/List는 40, Web/Work는 20.

## Elevation & Depth

그림자는 네 단계(Shadow 100 ~ 400)이고 색은 모두 #06080C에 투명도만 다릅니다.

- **Shadow 100:** 카드 · **200:** Floating 버튼 · **300:** 화면 위에 겹치는 층 · **400:** 팝업·바텀시트
- 깊이는 그림자보다 **바탕색 차이**(흰색 위 Gray 100 면)로 먼저 표현합니다. 모달 뒤에는 `overlay-dim`을 깝니다.

## Shapes

면이 클수록 더 둥글게 합니다: 체크박스 4 → 칩·툴팁 8 → 버튼 40은 10 → 버튼 48·입력창·카드 12 → 팝업·바텀시트 16(바텀시트는 위 모서리만). 원과 알약은 `pill`(Floating 버튼, 아바타, 라디오, 날짜 칸, 진행 바).

## Components

**Figma에서는 라이브러리 인스턴스를 불러와 속성만 바꿉니다.** 키·속성·부분별 토큰은 `components.json`을 보세요. 위 YAML의 components 값은 코드나 다른 도구에서 비슷하게 재현할 때 쓰는 요약입니다.

### Buttons
- **Filled**(Primary · Secondary · White · Blue · Light Blue), **Ghost**, **Outlined**, **Floating**. 크기 48(기본) · 40.
- 화면 하단 CTA는 **Button Group**: Single · Side by Side(Secondary + Primary) · Stacked(Primary 위, Ghost 아래).

### Selection
- **Chip/Multi Choice**(여러 개 선택, 48 · 38), **Multi Choice with Icon**, **Two Choice**(둘 중 하나, 163 높이 카드 두 개).
- **Controls/Checkbox · Radio**, **List/Checkbox List**(필터 목록 행).

### Inputs
- **Fields/Text Input · Text Area · Select Field.** 포커스 Blue 600 테두리, 오류여도 테두리는 Blue 600 유지 + 아래 Red 500 안내.
- **전체 화면 작성 영역**(질문 제목 아래가 통째로 입력칸인 화면): 테두리 없이 Body 15 Medium Long. 안내 문구는 **Gray 400** — Gray 500이면 이미 쓴 글처럼 보이기 때문. 입력창 컴포넌트의 안내 문구는 그대로 Gray 500.
- 글자 버튼은 **Button/Text Button** 하나: Accent(앱 바 오른쪽 완료 · 마치기, Subtitle 16 SemiBold Blue) · Neutral(목록 머리 삭제 · 편집, Body 14 Medium Gray 500). 누를 수 없을 때 **Disabled(Gray 400)**.
- 아이콘만 있는 버튼은 Filled Button의 Show Label을 끈다(예: 질문 추가 + — Light Blue 40, 너비 채움).

### Navigation
- **App Bar/Top App Bar**(Home · Sub), **App Bar/Navigation Bar**(홈 · 실행 목표 · 분석, 메인 탭 화면에만), **Tabs**(Text Tabs — 모바일 · 웹 공통, Size 18 · 14, 높이 40 · 여백 없음 · 칸 수는 Show Tab 3 · 4 · 구분선 Show Divider / Text Fixed Tabs / Box Tabs), **Progress Bar**(단계 흐름).

### Overlays & Feedback
- **Popup**(가운데 확인 모달, 한 번에 하나), **Bottom Sheet**(Short: 내용 높이 · Long: 670 고정), **Date Time Picker**(오늘 이전 날짜는 Disabled), **Toast**(3초 결과 알림), **Tooltips**(Function · Hover · Guide).

### Lists & Labels
- **List/Icon List**(번호 카드, 순서 변경·삭제 · 고정 질문은 Action=None, Marker=Star ★), **Accordion**(Index Title · Index · Contents).
- **Empty State**(안내 1~2줄 Gray 500 + 선택 아이콘). 흰 카드가 틀이면 테두리 없이(Border=None), 카드 안에서 다른 내용과 함께 있으면 점선(Border=Dashed).
- **웹(1440)**: 왼쪽 **LNB**(펼침 284 · 접힘 84) + 본문(폭 928, 가운데). 페이지 제목 Heading 28 Bold, 섹션 제목 **Title 15 Bold**, 넓은 섹션 카드는 radius card-lg(16). 상단 필터는 **Dropdown**(높이 36), 버튼은 웹에서 주로 **Size 36**(좌우 12 · 모서리 8 · 아이콘 18). 주요 행동은 Button 36 Blue. **Size 40**은 작성 패널 아래처럼 한 영역을 마무리하는 행동(임시저장 · 작성 완료)에, **Size 48**은 웹 모달 아래 버튼(이전 · 다음)에 쓴다.
- **Modal (Web)**(520 × 652, 모서리 20 radius.modal-lg): 제목(Title 22 Bold, 선택) + 닫기 · 단계 막대 · 내용(Content **슬롯** — 질문과 입력을 직접 넣음) · 버튼 48 두 개(Show Footer). 목록형(템플릿 리스트)은 제목 + 버튼 없음 · 바탕 Gray 100. 확인만 받으면 Popup.
- **Popover**(280, 흰 바탕 · 모서리 12 · Shadow 300, 제목 Title 16 Bold + 개수 + Text Button Neutral, 내용 슬롯) — 버튼 아래 가볍게 뜨는 패널. 딤드 없음.
- **Menu**(165, 모서리 8 · Shadow 300, 위아래 6) + **Menu/Menu Item**(36, Subtitle 14 SemiBold, Default Gray 800 · Danger Red 500, Hover Gray 100) — 더보기 행동 목록. 위험 행동은 맨 아래 Danger.
- **List/Member Item**(Type=Add · Member, 32 높이 · 사이 12, Body 15 Medium) — 팀원 목록. 대표자는 Profile의 Show Leader(왕관).
- **Info Banner**(Gray 200 한 줄 안내, 정보 아이콘 + Body 12 Medium Gray 600). 강조 팁은 Guide Tooltip.
- 웹 소제목 · 접기 제목 · 이전/다음 · 템플릿 카드 제목은 **Title 14 Bold**, 웹 모달 제목은 **Title 22 Bold**.
- **회고 작성 패널(웹)**: 위 **Question Tag**(사전질문 1, 읽기 전용) + **Button/Pager**(이전 · 다음 32), 오른쪽 **Question Index (Web)**(줄 상태 Unanswered Gray 600 · Current Blue 50 · Answered Gray 900). 패널이 열리면 왼쪽 실행목표는 **Accordion/Section (Web)**으로 접고, 지금 작성 중인 회고 카드는 **Card/Retro (Web) Selected=On**(한 열에 하나).
- **List/Menu Item**(설정 목록 한 줄 48, Right = Chevron · Value · None). 흰 카드(모서리 12, Shadow 100) 안에 쌓고 그룹 제목은 Subtitle 14 SemiBold Gray 600. 프로필 행은 **Avatar 42**.
- **Segmented Control**(2~3칸 기준 전환, 예: 분석 개인 · 팀). 선택 칸 Gray 700. 내용 영역을 나누면 Tabs.
- 회색 요약 상자(분석 카드 등)는 **Gray 100(bg/secondary)** 100%. 투명도를 섞은 회색은 쓰지 않는다.
- **Badge**(읽기 전용 상태 라벨: "진행 중 1", D-day). Blue는 흰·회색 바탕 위, White는 연파랑 카드 위, Gray는 사람 이름. 크기 22(제목 옆) · 25(카드 머리 이름표). 누를 수 있으면 Chip을 씁니다. **Style=Outlined**(Caption 11 SemiBold, 테두리 1px)는 웹 회고 카드의 진행 상태 — Gray 작성 전 · Blue 작성 중 · Green 제출 완료 · Dark 분석 완료.
- **Card/**: Space(홈 스페이스, 제목 한 줄 말줄임) · Retro (Mobile)(연파랑 진행 중 회고) · Answer(답변, Body 15 Medium Long) · Retro (Web)(296, Status × Deadline) · Goal (Web)(실행목표 패널의 회고별 목표 묶음, Badge On/Off). 카드를 직접 그리지 말고 이 컴포넌트를 씁니다.
- **Card/** 추가: Retro (Mobile) Status=Open · Closed, Goal (Mobile), Answer(Platform × Type=Text · Emotion · Score), Question Group (Web), Template(Default · Custom) · Template Detail · Template Summary.
- **Analysis/**(회고 결과): Section Title · Progress Panel(Satisfaction 도넛 + Goal Rate 막대) · Keyword Group + Keyword Item(Good · Bad · Improve) · Highlight Title(모바일). 차트 모양은 예시, 실제 비율은 데이터로 그린다. 분석 블록을 직접 그리지 않는다.

## Illustration & Icons

- 일러스트 20종: **Content**(빈 화면·상황), **Retro**(회고 방식 설명), **Splash**(온보딩), **Banner**. 원본 500을 120(팝업) · 160(카드·바텀시트) · 200(빈 화면) · 280(스플래시)으로 줄여 씁니다.
- 선 아이콘 24(버튼 안 18·16), 색은 글자 색을 따릅니다. 그래픽 아이콘은 Color(기본) · White(파란 바탕 위, 또는 Gray 200 원 40px 안의 썸네일 — 홈 스페이스 카드). 그래픽 아이콘은 28이 기본, 카드 안 인원 수처럼 좁은 줄에서는 24.

## Do's and Don'ts

- Do: 화면당 Primary 버튼은 하나. 하단 CTA는 Button Group에 넣는다.
- Do: 색은 역할 토큰부터 고르고, 숫자 값 대신 토큰을 쓴다.
- Do: 결과 알림은 Toast, 결정이 필요하면 Popup, 고르거나 입력할 것이 많으면 Bottom Sheet.
- Do: 빈 화면에는 Content 일러스트(200)와 짧은 해요체 안내 한 줄, 행동 버튼 하나.
- Don't: 컴포넌트를 도형으로 다시 그리지 않는다(Figma 인스턴스 · 코드 클래스 사용).
- Don't: 파란색을 장식으로 쓰지 않는다. 선택·강조·링크에만.
- Don't: Popup을 두 개 겹치거나, Popup 위에 Bottom Sheet를 띄우지 않는다.
- Don't: Navigation Bar를 작성 흐름이나 바텀시트 화면에 두지 않는다.
- Don't: 회색 글자(text-tertiary)를 본문에 쓰지 않는다. 안내 문구·보조 정보에만.
