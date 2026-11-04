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
  error: "#fb5c5c"
  text-primary: "#212329"
  text-secondary: "#666b75"
  text-tertiary: "#a9afbb"
  text-disabled: "#ced2da"
  text-inverse: "#ffffff"
  text-accent: "#6c9cfa"
  text-error: "#fb5c5c"
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
  status-error: "#fb5c5c"
  gray-300: "#dfe3ea"
  gray-400: "#ced2da"
  gray-600: "#8b909c"
  gray-700: "#666b75"
  gray-800: "#454952"
typography:
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
  title-16-bold:
    fontFamily: Pretendard
    fontSize: 16px
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
  r16: 16px
  full: 999px
  button: 12px
  button-sm: 10px
  chip: 8px
  chip-sm: 6px
  field: 12px
  card: 12px
  toast: 12px
  tooltip: 8px
  list-card: 8px
  checkbox: 4px
  modal: 16px
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

> 이 파일은 AI 에이전트와 사람이 같이 읽는 레이어 디자인 시스템 요약입니다. 위 YAML의 colors에는 역할 토큰과 컴포넌트가 쓰는 팔레트 단계만 넣었고, 전체 팔레트 55색은 tokens.json에 있습니다. 정확한 값은 `layer-tokens-v0.1.4.json`, Figma 컴포넌트 키와 속성은 `components.json`에 있습니다. **Figma 작업에서는 컴포넌트를 새로 그리지 말고 `components.json`의 라이브러리 인스턴스를 불러와 쓰세요.**

## Overview

레이어는 팀과 개인이 회고를 쓰고, 실행 목표를 정하고, 결과를 분석하는 모바일 앱입니다. 화면은 **차분하고 정돈된** 인상을 줍니다. 흰 바탕 위에 짙은 회색 글자와 버튼을 쓰고, 파란색(Blue 600)은 선택과 강조에만 아껴 씁니다. 장식은 일러스트가 맡고, UI 자체는 단순한 면과 넉넉한 여백으로 구성합니다.

- 기준 화면: iPhone 375 × 812, 라이트 모드만
- 글꼴: Pretendard 한 가지
- 말투: 부드러운 해요체 ("회고를 저장했어요", "작성을 그만둘까요?")

## Colors

색은 **역할 이름**으로 고릅니다. 팔레트 단계(gray-500 등)는 역할이 없는 곳과 Hover·Pressed에서만 씁니다.

- **글자:** `text-primary`(Gray 900) 제목·본문 · `text-secondary`(Gray 700) 보조 · `text-tertiary`(Gray 500) 안내 문구·선택 안 된 탭 · `text-disabled`(Gray 400) · `text-inverse`(흰색, 진한 바탕 위) · `text-accent`(Blue 600) · `text-error`(Red 400)
- **바탕:** `bg-surface`(흰색) 화면·카드·모달 · `bg-secondary`(Gray 100) 칩·탭·목록 카드·비활성 · `bg-inverse`(Gray 900) Primary 버튼 · `bg-accent`(Blue 600) 선택·Blue 버튼 · `bg-accent-secondary`(Blue 100) · `bg-selected`(Blue 200) · `bg-toast`(86% 검정)
- **테두리:** `border-default`(Gray 300) 입력창 · `border-divider`(8% 검정) · `border-focus`(Blue 600)
- **기타:** `overlay-dim`(72% 검정) 팝업·바텀시트 뒤 · `status-error`(Red 400) 삭제·오류

**상태 규칙:** Hover는 기본색에서 팔레트 한 단계, Pressed는 두 단계 옮깁니다(밝은 색은 진해지고, Gray 900은 800 → 700으로 밝아짐). Disabled는 `bg-secondary` + `text-disabled`.

## Typography

Pretendard 하나로 15단계를 씁니다. 행간은 140%(Heading 24만 150%), 자간 0.

- **Heading 24 Bold:** 홈 앱 바 제목
- **Title 20 / 18 / 16 Bold:** 바텀시트 큰 제목 / 팝업 제목·같은 너비 탭 / 바텀시트 헤더
- **Subtitle 18 / 16 / 14 SemiBold:** 글자 탭·서브 앱 바 제목 / 버튼 48 / 버튼 40·칩 38·입력창 라벨
- **Body 16 / 15 / 14 / 12 Medium, 12 SemiBold:** 칩·토스트·팝업 부제 / 입력 글자·체크박스 라벨 / 목록·아코디언 내용 / 글자 수 / 툴팁
- **Caption 11 Medium, 10 Bold:** 내비게이션 라벨 / 번호 동그라미

## Layout

- 화면 너비 **375**, 좌우 여백 **20**(`screen-x`). 화면의 큰 덩어리 사이(제목 ↔ 선택지, 상단 박스 ↔ 목록)는 **32 · 40**(섹션 간격), 그 밖의 간격은 4~24. 카드·토스트·팝업 안 콘텐츠 너비는 **335**.
- 위에서 아래로: OS 상태 바(44) → 앱 바(58) → 본문 → 하단 CTA(Button Group, 안전 영역 34 포함) 또는 Navigation Bar.
- 간격은 **4 · 8 · 12 · 16 · 20 · 24** 여섯 단계. 가까운 관계일수록 좁게: 아이콘과 글자 4~8, 나란한 칩·버튼 8, 제목과 부제 12, 묶음 사이 16~24.
- 13 · 15 · 18 같은 값은 버튼·입력창 높이를 맞추려고 컴포넌트 안에서 생긴 값이라 화면에 직접 쓰지 않습니다.

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
- **Fields/Text Input · Text Area · Select Field.** 포커스 Blue 600 테두리, 오류여도 테두리는 Blue 600 유지 + 아래 Red 400 안내.

### Navigation
- **App Bar/Top App Bar**(Home · Sub), **App Bar/Navigation Bar**(홈 · 실행 목표 · 분석, 메인 탭 화면에만), **Tabs**(Text Tabs · Text Fixed Tabs · Box Tabs), **Progress Bar**(단계 흐름).

### Overlays & Feedback
- **Popup**(가운데 확인 모달, 한 번에 하나), **Bottom Sheet**(Short: 내용 높이 · Long: 670 고정), **Date Time Picker**, **Toast**(3초 결과 알림), **Tooltips**(Function · Hover · Guide).

### Lists & Labels
- **List/Icon List**(번호 카드, 순서 변경·삭제), **Accordion**(Index Title · Index · Contents).
- **Badge**(읽기 전용 상태 라벨: "진행 중 1", D-day). Blue는 흰·회색 바탕 위, White는 연파랑 카드 위, Gray는 사람 이름. 크기 22(제목 옆) · 25(카드 머리 이름표). 누를 수 있으면 Chip을 씁니다.

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
