"""Layer Skill — skill/layer-design-system/ (SKILL.md + references) and site/downloads/skill/.
Run after build_webkit.py (copies the web kit). Upload: zip the layer-design-system folder → Claude 설정 → 기능 → Skills."""
import pathlib, shutil
SRC = pathlib.Path('src/skill'); OUT = pathlib.Path('skill/layer-design-system'); KIT = pathlib.Path('site/kit')
if OUT.exists(): shutil.rmtree(OUT)
(OUT / 'references/web').mkdir(parents=True)
shutil.copy(SRC / 'SKILL.md', OUT / 'SKILL.md')
shutil.copy(SRC / 'checklist.md', OUT / 'references/checklist.md')
for src, dst in [('foundations/DESIGN.md', 'DESIGN.md'), ('foundations/components.json', 'components.json'), ('foundations/tokens.json', 'tokens.json')]:
    shutil.copy(src, OUT / 'references' / dst)
for f in ['layer-inline.css', 'layer-examples.html', 'layer-icons.js']:
    shutil.copy(KIT / f, OUT / 'references/web' / f)
for d in ['logo', 'illustrations']:
    shutil.copytree(KIT / d, OUT / 'references/web' / d)
D = pathlib.Path('site/downloads/skill'); D.mkdir(parents=True, exist_ok=True)
shutil.copy(SRC / 'SKILL.md', D / 'SKILL.md'); shutil.copy(SRC / 'checklist.md', D / 'checklist.md')
print('skill', sum(1 for _ in OUT.rglob('*') if _.is_file()), 'files')
