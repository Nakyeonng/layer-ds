#!/usr/bin/env bash
# 문서 사이트를 GitHub Pages(gh-pages 가지)로 배포한다. 저장소 맨 위에서: ./deploy_pages.sh
# 처음 한 번: GitHub 저장소 Settings → Pages → Source "Deploy from a branch" → gh-pages / (root)
set -euo pipefail
python3 src/build_site.py >/dev/null
REMOTE=$(git remote get-url origin)
OUT=$(mktemp -d)
cp -r site/. "$OUT/"
cp build/index-pages.html "$OUT/index.html"     # artifact용 index는 문서 뼈대 없이 만들어지므로 Pages용으로 교체
touch "$OUT/.nojekyll"                           # Jekyll 처리 끄기(파일을 그대로 서비스)
cd "$OUT"
git init -q -b gh-pages
git add -A
git -c user.name="Layer DS" -c user.email="Nakyeonng@users.noreply.github.com" commit -q -m "Deploy docs site $(date +%F)"
git push -q -f "$REMOTE" gh-pages
echo "pushed gh-pages"
