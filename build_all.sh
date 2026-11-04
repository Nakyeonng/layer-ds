#!/usr/bin/env bash
# Layer DS 전체 다시 만들기. 저장소 맨 위 폴더에서 실행: ./build_all.sh
# 필요: python3 + beautifulsoup4 (pip install beautifulsoup4)
set -euo pipefail
VERSION="${VERSION:-0.2.1}"
python3 src/build_tokens_json.py          # foundations/tokens.json
python3 src/build_design_md.py            # foundations/DESIGN.md
python3 src/build_components_json.py      # foundations/components.json (Figma 스냅샷: src/data/figma_components.json)
cp foundations/tokens.json      "site/downloads/layer-tokens-v${VERSION}.json"
cp foundations/DESIGN.md        "site/downloads/DESIGN-v${VERSION}.md"
cp foundations/components.json  "site/downloads/layer-components-v${VERSION}.json"
python3 src/build_site.py                 # site/*.html
python3 src/build_webkit.py               # site/kit/* — 예시 마크업을 site/*.html에서 가져오므로 사이트 다음에
python3 src/build_llms.py                 # site/llms.txt · llms-full.txt
rm -rf kit && cp -r site/kit kit          # jsDelivr로 배포하는 웹 키트
python3 src/build_skill.py                # skill/layer-design-system — Claude Skill(SKILL.md + references)
echo "done v${VERSION}"
