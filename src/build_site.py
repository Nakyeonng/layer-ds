import json, re, html, pathlib, base64

R = pathlib.Path('site')
F = pathlib.Path('foundations')
I = json.load(open(F / 'icons/_src/assets_nav.json'))
G = json.load(open(F / 'icons/_src/graphic.json'))
A = F / 'components/assets'
FIGMA = 'https://www.figma.com/community/file/1699490552460986431/layer-ds'
UPDATED = '2026-11-04'
esc = html.escape

# ── helpers ───────────────────────────────────────────────
def mono(svg): return svg.replace('fill="#212329"', 'fill="currentColor"').replace('fill="black"', 'fill="currentColor"')
def bare(svg): return re.sub(r'^<svg width="[\d.]+" height="[\d.]+"', '<svg aria-hidden="true" focusable="false"', svg)
def icon(name, cls='icon icon-24'): return f'<span class="{cls}">{bare(mono(I[name]))}</span>'
def gicon(key, cls='icon icon-graphic'): return f'<span class="{cls}">{bare(G[key])}</span>'
def asset(n): return (A / f'{n}.svg').read_text()
def kebab(s): return re.sub(r'[_\s]+', '-', s).lower()
def chip(kind, text): return f'<span class="chip chip--{kind}">{text}</span>'
def code(src, lang=''):
    return f'<div class="code"><pre><code>{esc(src.strip())}</code></pre><button type="button" class="copy" data-copy-pre>복사</button></div>'
def table(head, rows, num_cols=()):
    th = ''.join(f'<th{" class=\"num\"" if i in num_cols else ""} scope="col">{h}</th>' for i, h in enumerate(head))
    trs = ''.join('<tr>' + ''.join(f'<td{" class=\"num\"" if i in num_cols else ""}>{c}</td>' for i, c in enumerate(r)) + '</tr>' for r in rows)
    return f'<div class="table-wrap"><table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'
def callout(kind, label, date, text):
    return f'<div class="callout">{chip(kind, label)}<div><time datetime="{date}">{date}</time><p class="cbody">{text}</p></div></div>'
def figma_link(node, label='Figma 파일'): return f'<a href="{FIGMA}" target="_blank" rel="noopener" title="Figma 커뮤니티 파일에서 열기">{label}</a>'

# ── navigation ────────────────────────────────────────────
PAGES = [
    ('index', '소개', 'start', None), ('updates', '업데이트', 'start', None), ('figma-file', 'Figma 파일 쓰기', 'start', None), ('ai-guide', 'AI로 화면 만들기', 'start', None),
    ('logo', 'Logo', 'brand', 'ok'), ('illustration', 'Illustration', 'brand', 'ok'),
    ('tokens', 'Tokens', 'found', 'ok'), ('color', 'Color', 'found', 'wait'), ('typography', 'Typography', 'found', 'ok'),
    ('elevation', 'Elevation', 'found', 'ok'), ('iconography', 'Iconography', 'found', 'ok'), ('spacing', 'Spacing', 'found', 'ok'), ('layout', 'Layout', 'found', 'ok'), ('radius', 'Radius', 'found', 'ok'), ('state', 'State', 'found', 'ok'),
    ('accordion', 'Accordion', 'comp', 'ok'), ('app-bar', 'App Bar', 'comp', 'ok'), ('bottom-sheet', 'Bottom Sheet', 'comp', 'ok'), ('button', 'Button', 'comp', 'ok'), ('chip-button', 'Chip Button', 'comp', 'ok'), ('controls', 'Controls', 'comp', 'ok'), ('date-picker', 'Date Time Picker', 'comp', 'ok'), ('fields', 'Fields', 'comp', 'ok'), ('lists', 'Lists', 'comp', 'ok'), ('navigation-bar', 'Navigation Bar', 'comp', 'ok'), ('popup', 'Popup', 'comp', 'ok'), ('progress-bar', 'Progress Bar', 'comp', 'ok'), ('scroll-bar', 'Scroll Bar', 'comp', 'ok'), ('tabs', 'Tabs', 'comp', 'ok'), ('toast', 'Toast', 'comp', 'ok'), ('tooltip', 'Tooltip', 'comp', 'ok'), ('avatar', 'Avatar', 'comp', 'ok'), ('badge', 'Badge', 'comp', 'ok'), ('empty-state', 'Empty State', 'comp', 'ok'), ('cards', 'Cards', 'comp', 'ok'), ('dropdown', 'Dropdown', 'comp', 'ok'), ('popover', 'Popover · Menu', 'comp', 'ok'), ('analysis', 'Analysis', 'comp', 'ok'), ('writing-panel', 'Writing Panel', 'comp', 'ok'),
]
SOON = {'found': [], 'comp': []}
GROUPS = [('start', '시작하기'), ('brand', 'Brand'), ('found', 'Foundations'), ('comp', 'Components')]
LOGO = pathlib.Path('foundations/logo')
def logo_svg(n, label=None):
    t = (LOGO / f'{n}.svg').read_text()
    a = f'role="img" aria-label="{label}"' if label else 'aria-hidden="true" focusable="false"'
    return re.sub(r'^<svg width="[\d.]+" height="[\d.]+"', f'<svg {a}', t)

def nav_html(cur):
    out = []
    for g, gname in GROUPS:
        items = []
        for pid, label, grp, st in PAGES:
            if grp != g: continue
            curattr = ' aria-current="page"' if pid == cur else ''
            items.append(f'<li><a href="{pid}.html"{curattr}>{label}</a></li>')
        for s in SOON.get(g, []):
            items.append(f'<li><span class="soon">{s}<em>준비 중</em></span></li>')
        out.append(f'<div class="nav-group"><h2>{gname}</h2><ul>{"".join(items)}</ul></div>')
    return ''.join(out)

def brand():
    return (f'<a class="brand" href="index.html" aria-label="Layer Design System 홈">'
            f'<span class="brand-logo brand-logo--light">{logo_svg("logo-horizontal-basic")}</span>'
            f'<span class="brand-logo brand-logo--dark">{logo_svg("logo-horizontal-on-dark")}</span>'
            f'<span class="brand-sub">Design System</span></a>')

def pager(pid):
    ids = [p[0] for p in PAGES]; i = ids.index(pid)
    prev = PAGES[i - 1] if i > 0 else None; nxt = PAGES[i + 1] if i < len(PAGES) - 1 else None
    a = f'<a href="{prev[0]}.html"><small>이전</small>{prev[1]}</a>' if prev else ''
    b = f'<a href="{nxt[0]}.html"><small>다음</small>{nxt[1]}</a>' if nxt else ''
    return f'<nav class="pager" aria-label="페이지 이동">{a}{b}</nav>'

SCRIPT = r'''<script>
(function () {
  var top = document.getElementById('to-top');
  if (top) {
    var tick = false;
    function show() { tick = false; top.classList.toggle('is-shown', window.scrollY > 480); }
    window.addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(show); } }, { passive: true });
    show();
    top.addEventListener('click', function () {
      var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
      var h = document.querySelector('.content h1'); if (h) { h.setAttribute('tabindex', '-1'); h.focus({ preventScroll: true }); }
    });
  }
})();
(function () {
  var toast = document.getElementById('toast'), t;
  function say(msg) { if (!toast) return; toast.textContent = msg; toast.classList.add('show'); clearTimeout(t); t = setTimeout(function () { toast.classList.remove('show'); }, 1400); }
  function copy(text, btn, msg) {
    function done() { say(msg || '복사했어요'); if (btn && btn.classList.contains('copy')) { var label = btn.getAttribute('data-label') || btn.textContent; btn.setAttribute('data-label', label); btn.textContent = '복사됨'; btn.classList.add('is-done'); setTimeout(function () { btn.textContent = label; btn.classList.remove('is-done'); }, 1200); } }
    try {
      navigator.clipboard.writeText(text).then(done, function () { fallback(text); });
    } catch (e) { fallback(text); }
    function fallback(s) { var r = document.createRange(), p = document.createElement('span'); p.textContent = s; p.style.position = 'fixed'; p.style.opacity = '0'; document.body.appendChild(p); r.selectNodeContents(p); var sel = getSelection(); sel.removeAllRanges(); sel.addRange(r); say('선택했어요. 복사해 주세요'); setTimeout(function () { p.remove(); }, 4000); }
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-copy]');
    if (b) { copy(b.getAttribute('data-copy'), b, b.getAttribute('data-copy-msg')); return; }
    var p = e.target.closest('[data-copy-pre]');
    if (p) { copy(p.parentNode.querySelector('pre').innerText, p); }
  });
  document.querySelectorAll('.js-nav').forEach(function (nav) {
    nav.addEventListener('click', function (e) {
      var item = e.target.closest('.nav-item'); if (!item) return;
      e.preventDefault();
      nav.querySelectorAll('.nav-item').forEach(function (n) { n.removeAttribute('aria-current'); });
      item.setAttribute('aria-current', 'page');
    });
  });
  document.addEventListener('click', function (e) {
    var c = e.target.closest('.chip-button:not(.cb-static):not(.dp-hour)');
    if (c && !c.disabled) {
      var pair = c.closest('.chip-pair');
      if (pair) pair.querySelectorAll('.chip-button').forEach(function (b) { b.setAttribute('aria-pressed', b === c ? 'true' : 'false'); });
      else c.setAttribute('aria-pressed', c.getAttribute('aria-pressed') === 'true' ? 'false' : 'true');
    }
    var pbBtn = e.target.closest('[data-pb]');
    if (pbBtn) {
      var bar = document.querySelector('#pb-live .progress-bar'); var steps = bar.querySelectorAll('.progress-bar__step');
      var n = Math.max(0, Math.min(steps.length, +bar.getAttribute('aria-valuenow') + +pbBtn.getAttribute('data-pb')));
      steps.forEach(function (s, i) { s.classList.toggle('is-done', i < n); });
      bar.setAttribute('aria-valuenow', n); bar.setAttribute('aria-label', steps.length + '단계 중 ' + n + '단계');
    }
  });
  document.querySelectorAll('.js-tablist').forEach(function (list) {
    list.addEventListener('click', function (e) {
      var t = e.target.closest('[role="tab"]'); if (!t) return;
      list.querySelectorAll('[role="tab"]').forEach(function (b) { b.setAttribute('aria-selected', b === t ? 'true' : 'false'); });
    });
  });
  window.dsWire = function (root) {
  root.querySelectorAll('.box-tabs--scroll, .dtp__hours').forEach(function (el) {
    function fog() { var max = el.scrollWidth - el.clientWidth;
      el.style.setProperty('--fog-l', el.scrollLeft > 1 ? '40px' : '0px');
      el.style.setProperty('--fog-r', el.scrollLeft < max - 1 ? '40px' : '0px'); }
    el.addEventListener('scroll', fog, { passive: true }); fog();
  });
  root.querySelectorAll('.scroll-area').forEach(function (el) {
    var t; el.addEventListener('scroll', function () { el.classList.add('is-scrolling'); clearTimeout(t); t = setTimeout(function () { el.classList.remove('is-scrolling'); }, 800); }, { passive: true });
    el.addEventListener('mouseenter', function () { el.classList.add('is-hover'); });
    el.addEventListener('mouseleave', function () { el.classList.remove('is-hover'); });
    if (el.matches(':hover')) el.classList.add('is-hover');
  });
  };
  window.dsWire(document);
  document.querySelectorAll('.acc__head').forEach(function (h) {
    if (h.closest('.ac-static')) return;
    h.addEventListener('click', function () { var a = h.closest('.acc'); var o = a.classList.toggle('is-open'); h.setAttribute('aria-expanded', o); });
  });
  document.querySelectorAll('.js-idx').forEach(function (b) {
    var panel = b.parentNode.querySelector('.acc-index');
    b.addEventListener('click', function () { panel.hidden = !panel.hidden; b.hidden = !panel.hidden; });
    panel.querySelector('.acc-index__header').addEventListener('click', function () { panel.hidden = true; b.hidden = false; });
    panel.querySelectorAll('.acc-index__item').forEach(function (it) {
      it.addEventListener('click', function () { panel.querySelectorAll('.acc-index__item').forEach(function (x) { x.removeAttribute('aria-current'); }); it.setAttribute('aria-current', 'true'); });
    });
  });
  document.querySelectorAll('[data-show-toast]').forEach(function (b) {
    b.addEventListener('click', function () {
      var host = document.getElementById(b.getAttribute('data-show-toast')), tpl = document.getElementById(b.getAttribute('data-toast-tpl'));
      host.innerHTML = tpl.innerHTML; var el = host.firstElementChild;
      requestAnimationFrame(function () { el.classList.add('is-shown'); });
      clearTimeout(host._t); host._t = setTimeout(function () { el.classList.remove('is-shown'); }, 3000);
    });
  });
  document.querySelectorAll('.js-dtp').forEach(function (root) {
    var now = new Date(), today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    var view = new Date(now.getFullYear(), now.getMonth(), 1), picked = null, hour = null, mer = 'am';
    var grid = root.querySelector('.dtp__days'), title = root.querySelector('.dtp__month-title'), cta = root.querySelector('.dtp__cta .btn');
    var time = root.querySelector('.dtp__time'), hours = root.querySelectorAll('.dtp__hours .chip-button'), tabs = root.querySelectorAll('.dtp__time .tab');
    function same(a, b) { return a && b && a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth() && a.getDate() === b.getDate(); }
    function sync() { cta.disabled = !(picked && hour); var was = time.hidden; time.hidden = !picked; if (was && !time.hidden) root.querySelector('.dtp__hours').dispatchEvent(new Event('scroll')); }
    function draw() {
      var y = view.getFullYear(), m = view.getMonth(), lead = new Date(y, m, 1).getDay(), n = new Date(y, m + 1, 0).getDate(), html = '';
      title.textContent = y + '년 ' + (m + 1) + '월';
      for (var i = 0; i < lead; i++) html += '<li></li>';
      for (var d = 1; d <= n; d++) {
        var dt = new Date(y, m, d);
        html += '<li><button type="button" class="dtp__day" data-d="' + d + '" aria-pressed="' + (same(dt, picked) ? 'true' : 'false') + '"' +
                (same(dt, today) ? ' aria-current="date"' : '') + (dt < today ? ' disabled' : '') + '>' + d + '</button></li>';
      }
      grid.innerHTML = html; sync();
    }
    function clearHours() { hour = null; hours.forEach(function (c) { c.setAttribute('aria-pressed', 'false'); }); }
    root.querySelector('[data-dtp-prev]').addEventListener('click', function () { view.setMonth(view.getMonth() - 1); draw(); });
    root.querySelector('[data-dtp-next]').addEventListener('click', function () { view.setMonth(view.getMonth() + 1); draw(); });
    grid.addEventListener('click', function (e) {
      var b = e.target.closest('.dtp__day'); if (!b || b.disabled) return;
      picked = new Date(view.getFullYear(), view.getMonth(), +b.getAttribute('data-d')); draw();
    });
    tabs.forEach(function (t) { t.addEventListener('click', function () {
      mer = t.getAttribute('data-mer'); tabs.forEach(function (x) { x.setAttribute('aria-selected', x === t ? 'true' : 'false'); }); clearHours(); sync();
    }); });
    hours.forEach(function (c) { c.addEventListener('click', function () {
      hours.forEach(function (x) { x.setAttribute('aria-pressed', x === c ? 'true' : 'false'); }); hour = c.textContent; sync();
    }); });
    cta.addEventListener('click', function () {
      if (!picked || !hour) return;
      say(picked.getFullYear() + '년 ' + (picked.getMonth() + 1) + '월 ' + picked.getDate() + '일 ' + (mer === 'am' ? '오전 ' : '오후 ') + hour + '을 골랐어요');
    });
    root.querySelector('[data-dtp-close]').addEventListener('click', function () {
      picked = null; mer = 'am'; view = new Date(now.getFullYear(), now.getMonth(), 1); clearHours();
      tabs.forEach(function (x, i) { x.setAttribute('aria-selected', i === 0 ? 'true' : 'false'); }); draw();
    });
    draw();
  });
  (function () {
    var dim = document.getElementById('popup-dim'); if (!dim) return;
    document.querySelectorAll('[data-popup]').forEach(function (b) { b.addEventListener('click', function () {
      dim.innerHTML = document.getElementById('pp-' + b.getAttribute('data-popup')).innerHTML; dim.hidden = false;
      var f = dim.querySelector('.btn'); if (f) f.focus();
    }); });
    dim.addEventListener('click', function (e) { if (e.target === dim || e.target.closest('.btn')) { dim.hidden = true; dim.innerHTML = ''; } });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !dim.hidden) { dim.hidden = true; dim.innerHTML = ''; } });
  })();
  (function () {
    var dim = document.getElementById('bsheet-dim'); if (!dim) return;
    function close() { dim.hidden = true; dim.innerHTML = ''; }
    document.querySelectorAll('[data-bsheet]').forEach(function (b) { b.addEventListener('click', function () {
      dim.innerHTML = document.getElementById('bs-' + b.getAttribute('data-bsheet')).innerHTML; dim.hidden = false;
      window.dsWire(dim);
      var f = dim.querySelector('.bsheet__close'); if (f) f.focus();
      dim.querySelectorAll('[role=tablist]').forEach(function (tl) { tl.addEventListener('click', function (e) {
        var t = e.target.closest('[role=tab]'); if (!t) return;
        tl.querySelectorAll('[role=tab]').forEach(function (x) { x.setAttribute('aria-selected', x === t ? 'true' : 'false'); });
      }); });
      dim.querySelectorAll('.chip-button--card').forEach(function (c) { c.addEventListener('click', function () {
        dim.querySelectorAll('.chip-button--card').forEach(function (x) { x.setAttribute('aria-pressed', x === c ? 'true' : 'false'); });
      }); });
    }); });
    dim.addEventListener('click', function (e) { if (e.target === dim || e.target.closest('.bsheet__close') || e.target.closest('.bsheet__footer .btn')) close(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !dim.hidden) close(); });
  })();
  (function () {
    var btns = document.querySelectorAll('[data-dl]'); if (!btns.length) return;
    var msg = document.getElementById('tk-msg'); var dlp = null;
    function note(t) { if (msg) msg.textContent = t; }
    var CRC = (function () { var t = [], c, n, k; for (n = 0; n < 256; n++) { c = n; for (k = 0; k < 8; k++) c = c & 1 ? 0xEDB88320 ^ (c >>> 1) : c >>> 1; t[n] = c >>> 0; } return t; })();
    function crc32(u) { var c = 0xFFFFFFFF; for (var i = 0; i < u.length; i++) c = CRC[(c ^ u[i]) & 255] ^ (c >>> 8); return (c ^ 0xFFFFFFFF) >>> 0; }
    // spec: "zipName|folder|src=name,src=name" — STORE-only zip built from files the site already serves
    function makeZip(spec) {
      var parts = spec.split('|'), folder = parts[0], list = parts[1].split(',').map(function (x) { return x.split('='); });
      return Promise.all(list.map(function (p) { return fetch(p[0]).then(function (r) { if (!r.ok) throw new Error(r.status); return r.arrayBuffer(); }); })).then(function (bufs) {
        var enc = new TextEncoder(), chunks = [], central = [], off = 0;
        function le(n, b) { var a = new Uint8Array(b); for (var i = 0; i < b; i++) a[i] = (n >>> (8 * i)) & 255; return a; }
        bufs.forEach(function (buf, i) {
          var data = new Uint8Array(buf), name = enc.encode(folder + '/' + list[i][1]), crc = crc32(data), sz = data.length;
          var head = [le(0x04034b50, 4), le(20, 2), le(0x0800, 2), le(0, 2), le(0, 2), le(0x5D63, 2), le(crc, 4), le(sz, 4), le(sz, 4), le(name.length, 2), le(0, 2), name];
          central.push([le(0x02014b50, 4), le(20, 2), le(20, 2), le(0x0800, 2), le(0, 2), le(0, 2), le(0x5D63, 2), le(crc, 4), le(sz, 4), le(sz, 4), le(name.length, 2), le(0, 2), le(0, 2), le(0, 2), le(0, 2), le(0, 4), le(off, 4), name]);
          head.forEach(function (h) { chunks.push(h); off += h.length; }); chunks.push(data); off += sz;
        });
        var cstart = off, clen = 0; central.forEach(function (c) { c.forEach(function (h) { chunks.push(h); clen += h.length; }); });
        chunks.push(le(0x06054b50, 4), le(0, 2), le(0, 2), le(list.length, 2), le(list.length, 2), le(clen, 4), le(cstart, 4), le(0, 2));
        return new Blob(chunks, { type: 'application/zip' });
      });
    }
    if (window.claude && window.claude.use) { window.claude.use('downloads').then(function (d) { dlp = d; }); }
    btns.forEach(function (b) { b.addEventListener('click', function () {
      var path = b.getAttribute('data-dl'), name = b.getAttribute('data-dl-name');
      var isZip = b.hasAttribute('data-zip');
      (isZip ? makeZip(b.getAttribute('data-zip')) : fetch(path).then(function (r) { if (!r.ok) throw new Error(r.status); return r.text(); })).then(function (text) {
        if (dlp) return dlp.save({ filename: name, data: text }).then(function () { note(name + ' 파일을 저장했어요.'); }, function (e) {
          if (e && e.code === 'declined') note('저장을 취소했어요.'); else note('여기서는 저장할 수 없어요. 잠시 뒤 다시 눌러 주세요.'); });
        var a = document.createElement('a'); a.href = URL.createObjectURL((isZip ? text : new Blob([text], { type: 'application/json' }))); a.download = name; document.body.appendChild(a); a.click(); a.remove();
        note(name + ' 파일을 내려받았어요.');
      }).catch(function () { note('파일을 불러오지 못했어요. 잠시 뒤 다시 눌러 주세요.'); });
    }); });
  })();
  // Korean IME can push one extra syllable past maxlength while composing; trim when composition ends.
  function countField(el) {
    var max = +el.getAttribute('maxlength');
    if (el.value.length > max) el.value = el.value.slice(0, max);
    var c = el.parentNode.querySelector('.field__count'), n = el.value.length;
    if (c) c.innerHTML = n ? '<b>' + n + '</b>/' + max : '0/' + max;
  }
  document.addEventListener('input', function (e) {
    var el = e.target.closest('[data-count]'); if (!el || e.isComposing) return; countField(el);
  });
  document.addEventListener('compositionend', function (e) {
    var el = e.target.closest('[data-count]'); if (el) countField(el);
  });
  function label() {
    var cur = document.documentElement.getAttribute('data-theme');
    var isDark = cur ? cur === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
    var t = isDark ? '라이트 모드로 바꾸기' : '다크 모드로 바꾸기';
    document.querySelectorAll('[data-theme-toggle]').forEach(function (b) { b.setAttribute('aria-label', t); b.setAttribute('title', t); });
  }
  label();
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-theme-toggle]'); if (!b) return;
    e.preventDefault(); e.stopPropagation();
    var root = document.documentElement, cur = root.getAttribute('data-theme');
    var isDark = cur ? cur === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
    var next = isDark ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('layer-ds-theme', next); } catch (err) {}
    say(next === 'dark' ? '다크 모드로 바꿨어요' : '라이트 모드로 바꿨어요');
    label();
  });
})();
</script>'''

HEAD_LINKS = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="css/site.css">
<link rel="stylesheet" href="css/typography.css">
<link rel="stylesheet" href="css/color.css">
<link rel="stylesheet" href="css/elevation.css">
<link rel="stylesheet" href="css/icons.css">
<link rel="stylesheet" href="css/components.css">
<link rel="stylesheet" href="css/buttons.css">
<link rel="stylesheet" href="css/chips.css">
<link rel="stylesheet" href="css/fields.css">
<link rel="stylesheet" href="css/tabs.css">
<link rel="stylesheet" href="css/controls.css">
<link rel="stylesheet" href="css/lists.css">
<link rel="stylesheet" href="css/feedback.css">
<link rel="stylesheet" href="css/date-picker.css">
<link rel="stylesheet" href="css/popup.css">
<link rel="stylesheet" href="css/bottom-sheet.css">
<link rel="stylesheet" href="css/radius.css">
<link rel="stylesheet" href="css/spacing.css">
<link rel="stylesheet" href="css/layout.css">
<link rel="stylesheet" href="css/illustration.css">
<link rel="stylesheet" href="css/badge.css">
<link rel="stylesheet" href="css/cards.css">
<link rel="stylesheet" href="css/analysis.css">
<link rel="stylesheet" href="css/writing.css">
<link rel="stylesheet" href="css/pages.css">'''

MOON = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M13.5 9.6A5.6 5.6 0 0 1 6.4 2.5a5.6 5.6 0 1 0 7.1 7.1Z" fill="currentColor"/></svg>'
SUN = '<svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="3.2" fill="currentColor"/><g stroke="currentColor" stroke-width="1.4" stroke-linecap="round"><path d="M8 1.2v1.6M8 13.2v1.6M1.2 8h1.6M13.2 8h1.6M3.2 3.2l1.1 1.1M11.7 11.7l1.1 1.1M3.2 12.8l1.1-1.1M11.7 4.3l1.1-1.1"/></g></svg>'
def toggle():
    return (f'<button type="button" class="theme-toggle" data-theme-toggle aria-label="다크 모드로 바꾸기" title="다크 모드로 바꾸기">'
            f'<span class="to-dark">{MOON}</span><span class="to-light">{SUN}</span></button>')

# Runs before first paint: apply the saved choice so pages don't flash.
EARLY = """<script>(function(){try{var t=localStorage.getItem('layer-ds-theme');if(t==='dark'||t==='light')document.documentElement.setAttribute('data-theme',t);}catch(e){}})();</script>"""

def shell(pid, title, content, wrapped=False):
    body = f'''<header class="site-header">{brand()}<div class="site-header__actions">{toggle()}</div></header>
<div class="site">
  <aside class="sidebar" aria-label="문서 목차"><nav>{nav_html(pid)}</nav></aside>
  <header class="topbar"><details><summary>{brand()}<span class="topbar-row">{toggle()}<span class="menu-label">메뉴</span></span></summary><nav>{nav_html(pid)}</nav></details></header>
  <main class="main"><div class="content">
{content}
{pager(pid)}
  </div></main>
</div>
<div class="site-toast" id="toast" role="status" aria-live="polite"></div>
<button type="button" class="btn btn--floating btn--icon-only to-top" id="to-top" aria-label="페이지 맨 위로" title="맨 위로">{icon("Icon/Assets/Chevron-Up")}</button>
{SCRIPT}'''
    head = f'''<title>{title}</title>
{EARLY}
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="icon" href="img/favicon.svg" type="image/svg+xml">
<link rel="icon" href="img/favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="img/apple-touch-icon.png">
{HEAD_LINKS}'''
    if wrapped:
        return head + '\n' + body + '\n'
    return f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{head}
</head>
<body>
{body}
</body>
</html>
'''

def page_head(eyebrow, h1, lead, status=None, node=None, extra=''):
    meta = []
    if status: meta.append(chip(*status))
    if node: meta.append(figma_link(node))
    meta.append(f'<span>{UPDATED} 기준</span>')
    if extra: meta.append(extra)
    return f'''<header class="page-head">
  <span class="eyebrow">{eyebrow}</span>
  <h1>{h1}</h1>
  <p class="lead">{lead}</p>
  <div class="meta">{"".join(meta)}</div>
</header>'''

# ── data ──────────────────────────────────────────────────
PALETTE = [
    ('Primary', [('Gray', 'gray', [('0', 'FFFFFF'), ('100', 'F2F4F8'), ('200', 'EDF0F4'), ('300', 'DFE3EA'), ('400', 'CED2DA'), ('500', 'A9AFBB'), ('600', '8B909C'), ('700', '666B75'), ('800', '454952'), ('900', '212329')], '900')]),
    ('Secondary', [('Blue', 'blue', [('50', 'F1F6FF'), ('100', 'E9F0FF'), ('200', 'E2EBFE'), ('300', 'C4D7FD'), ('400', 'A7C4FC'), ('500', '89B0FB'), ('600', '6C9CFA'), ('700', '415E96'), ('800', '2B3E64'), ('900', '172031')], '600'),
                   ('Purple', 'purple', [('50', 'FBFAFF'), ('100', 'F6F5FE'), ('200', 'E8E6FD'), ('300', 'D1CDFC'), ('400', 'BAB3FA'), ('500', 'A39AF9'), ('600', '8C81F7'), ('700', '544D94'), ('800', '383463'), ('900', '1C1A31')], '600')]),
    ('Status / Accent', [('Green', 'green', [('100', 'E2FCF0'), ('200', 'C6F1DD'), ('300', 'A6E9C8'), ('400', '6FDAA6'), ('500', '28C07B'), ('900', '034C0C')], '500'),
                         ('Red', 'red', [('100', 'FFE5E5'), ('200', 'FFC7C7'), ('300', 'FFA7A7'), ('400', 'FB5C5C'), ('500', 'F03E3E')], '500'),
                         ('Orange', 'orange', [('100', 'FFF0CF'), ('200', 'FDD495'), ('300', 'FDB663'), ('400', 'FC9F30'), ('500', 'F58603')], '500')]),
]
OPACITY = ['4', '8', '12', '22', '32', '48', '56', '72', '86', '100']

TYPE = [  # name, size, lh, weight label, class
    ('Heading 28 Bold', 28, '150%', '700 Bold', 'heading-28-bold'),
    ('Heading 24 Bold', 24, '150%', '700 Bold', 'heading-24-bold'),
    ('Title 20 Bold', 20, '140%', '700 Bold', 'title-20-bold'),
    ('Title 18 Bold', 18, '140%', '700 Bold', 'title-18-bold'),
    ('Title 22 Bold', 22, '140%', '700 Bold', 'title-22-bold'),
    ('Title 16 Bold', 16, '140%', '700 Bold', 'title-16-bold'),
    ('Title 15 Bold', 15, '140%', '700 Bold', 'title-15-bold'),
    ('Title 14 Bold', 14, '140%', '700 Bold', 'title-14-bold'),
    ('Subtitle 18 SemiBold', 18, '140%', '600 SemiBold', 'subtitle-18-semibold'),
    ('Subtitle 16 SemiBold', 16, '140%', '600 SemiBold', 'subtitle-16-semibold'),
    ('Subtitle 14 SemiBold', 14, '140%', '600 SemiBold', 'subtitle-14-semibold'),
    ('Body 16 Medium', 16, '140%', '500 Medium', 'body-16-medium'),
    ('Body 15 Medium', 15, '140%', '500 Medium', 'body-15-medium'),
    ('Body 15 Medium Long', 15, '180%', '500 Medium', 'body-15-medium-long'),
    ('Body 14 Medium', 14, '140%', '500 Medium', 'body-14-medium'),
    ('Body 13 Medium', 13, '140%', '500 Medium', 'body-13-medium'),
    ('Body 12 SemiBold', 12, '140%', '600 SemiBold', 'body-12-semibold'),
    ('Body 12 Medium', 12, '140%', '500 Medium', 'body-12-medium'),
    ('Caption 11 SemiBold', 11, '140%', '600 SemiBold', 'caption-11-semibold'),
    ('Caption 11 Medium', 11, '140%', '500 Medium', 'caption-11-medium'),
    ('Caption 10 Bold', 10, '140%', '700 Bold', 'caption-10-bold'),
    ('Caption 10 Medium', 10, '140%', '500 Medium', 'caption-10-medium'),
]

# color.css (primitive palette, under review)
ROLES = [
    ('text/primary', 'Gray 900', 'gray-900', '제목, 본문, 입력한 글자, 선택된 탭'),
    ('text/secondary', 'Gray 700', 'gray-700', '아코디언 내용·제목 등 보조 글자'),
    ('text/tertiary', 'Gray 500', 'gray-500', '안내 문구(placeholder), 팝업 부제, 선택 안 된 탭'),
    ('text/disabled', 'Gray 400', 'gray-400', '비활성 버튼·칩·라벨·날짜 글자'),
    ('text/inverse', 'Gray 0', 'gray-0', '진한 바탕 위 글자(Primary 버튼, 토스트, 선택된 칩)'),
    ('text/accent', 'Blue 600', 'blue-600', 'Blue Ghost·Light Blue 버튼 글자, 오늘 날짜, 입력 중 글자 수'),
    ('text/error', 'Red 500', 'red-500', '입력 오류 안내, 위험 행동 글자(삭제 · 내보내기)'),
    ('bg/surface', 'Gray 0', 'gray-0', '화면, 카드, 팝업, 바텀시트 바탕'),
    ('bg/secondary', 'Gray 100', 'gray-100', '칩, Box 탭, 목록 카드, 아코디언, 비활성 바탕'),
    ('bg/inverse', 'Gray 900', 'gray-900', 'Primary·Floating 버튼'),
    ('bg/accent', 'Blue 600', 'blue-600', 'Blue 버튼, 선택된 칩·날짜, 체크된 체크박스·라디오'),
    ('bg/accent-secondary', 'Blue 100', 'blue-100', 'Light Blue 버튼, Guide 툴팁'),
    ('bg/selected', 'Blue 200', 'blue-200', '아코디언 Index 현재 항목'),
    ('bg/toast', 'Opacity 86', 'opacity-86', '토스트'),
    ('border/default', 'Gray 300', 'gray-300', '입력창, Outlined 버튼 테두리'),
    ('border/divider', 'Opacity 8', 'opacity-8', '탭 아래 구분선'),
    ('border/focus', 'Blue 600', 'blue-600', '입력창 포커스, 키보드 Focus 표시'),
    ('overlay/dim', 'Opacity 72', 'opacity-72', '모달 뒤 딤드(팝업 · 웹 모달 · 바텀시트) — 흐름을 멈추고 답을 받아야 할 때'),
    ('status/error', 'Red 500', 'red-500', '삭제 아이콘 바탕, 오류 아이콘'),
]
def role_css(n): return '--color-' + n.replace('/', '-')

def build_color_css():
    lines = ['/* Layer Design System — primitive color palette',
             '   Source: Figma "Foundation / Color" (node 1:3324). Status: under review.',
             '   Primitives first, then role tokens (text, bg, border, overlay, status) collected from the components. */', ':root {']
    for _, fams in PALETTE:
        for fam, slug, steps, _p in fams:
            for s, h in steps:
                lines.append(f'  --color-{slug}-{s}: #{h};')
    for o in OPACITY:
        lines.append(f'  --color-opacity-{o}: rgb(6 8 12 / {int(o) / 100:g});')
    lines.append('')
    lines.append('  /* Roles — pick these in components; Figma collection "Color Role", same names */')
    for n, _l, prim, use in ROLES:
        lines.append(f'  {role_css(n)}: var(--color-{prim});   /* {use} */')
    lines.append('}')
    (R / 'css/color.css').write_text('\n'.join(lines) + '\n')

# ── DS component builders (same markup as the Figma implementation) ──
USER_ICON = bare((A / 'avatar-user-icon.svg').read_text())
def avatar(kind='icon', size=32):
    sz = {42: ' avatar--42', 28: ' avatar--28'}.get(size, '')
    if kind == 'icon': return f'<span class="avatar{sz}" role="img" aria-label="프로필">{USER_ICON}</span>'
    return '<span class="avatar"><img src="img/avatar-sample.png" alt="프로필 사진" width="32" height="32"></span>'
def app_bar_home(title='회고'):
    return f'<header class="app-bar app-bar--home"><h3 class="app-bar__title text-heading-24-bold">{title}</h3><div class="app-bar__side app-bar__side--end">{avatar()}</div></header>'
def app_bar_sub(title='회고', inverse=False, text_button=False, disabled=False, label='완료'):
    tb = f'<button type="button" class="app-bar__text-button text-subtitle-16-semibold"{" disabled" if disabled else ""}>{label}</button>' if text_button else ''
    acts = tb if text_button else f'<button type="button" class="app-bar__button" aria-label="더보기">{icon("Icon/Assets/More")}</button><button type="button" class="app-bar__button" aria-label="메뉴">{icon("Icon/Assets/Drawer")}</button>'
    return (f'<header class="app-bar app-bar--sub{" app-bar--inverse" if inverse else ""}"><div class="app-bar__contents">'
            f'<div class="app-bar__side"><button type="button" class="app-bar__button" aria-label="뒤로">{icon("Icon/Assets/Arrow-left")}</button></div>'
            f'<h3 class="app-bar__title text-subtitle-18-semibold">{title}</h3><div class="app-bar__side app-bar__side--end">{acts}</div></div></header>')
NAV = [('Home', '회고', 'Icon/Nav/Home'), ('Action Item', '실행 목표', 'Icon/Nav/ActionItem'), ('Analysis', '분석', 'Icon/Nav/Analysis')]
def nav_item(label, iconname, state=None):
    cur = ' aria-current="page"' if state == 'current' else ''
    cls = {'hover': ' is-hover', 'pressed': ' is-pressed'}.get(state, '')
    return f'<a href="#" class="nav-item{cls}"{cur}><span class="nav-item__icon">{icon(iconname)}</span><span class="nav-item__label text-caption-11-medium">{label}</span></a>'
def nav_bar(on='Home', safe=True, interactive=False):
    items = ''.join(f'<li>{nav_item(l, ic, "current" if k == on else None)}</li>' for k, l, ic in NAV)
    sa = f'<span class="safe-area" aria-hidden="true">{bare(asset("safe-area-ios14"))}</span>' if safe else ''
    return f'<nav class="nav-bar{" js-nav" if interactive else " is-static"}" aria-label="주요 메뉴 예시"><ul class="nav-bar__items">{items}</ul>{sa}</nav>'

# ── pages ─────────────────────────────────────────────────
def p_index():
    rows = [
        ['<a href="logo.html">Logo</a>', 'Brand', chip('ok', '확정'), '심볼, 파비콘 3종, 가로형 2종, 응용 2종'],
        ['<a href="illustration.html">Illustration</a>', 'Brand', chip('ok', '확정'), 'Content 7 · Banner 2 · Retro 7 · Splash 4, 500 기준 투명 배경, 컴포넌트'],
        ['<a href="color.html">Color</a>', 'Foundation', chip('wait', '검토 중'), '원색 팔레트 확정. 용도별 색은 컴포넌트 분석 후 추가'],
        ['<a href="typography.html">Typography</a>', 'Foundation', chip('ok', '확정'), '텍스트 스타일 22개(Title 22 · Title 14 추가), 크기·굵기·행간 토큰'],
        ['<a href="elevation.html">Elevation</a>', 'Foundation', chip('ok', '확정'), '그림자 4단계와 용도 이름'],
        ['<a href="iconography.html">Iconography</a>', 'Foundation', chip('ok', '확정'), '아이콘 69개(Assets 26, Graphic 30, Emotion 10, Navigation 3)'],
        ['<a href="radius.html">Radius</a>', 'Foundation', chip('ok', '확정'), '4 · 6 · 8 · 10 · 12 · 16 · Full 일곱 단계와 용도 토큰'],
        ['<a href="state.html">State</a>', 'Foundation', chip('ok', '확정'), 'Hover 한 단계 · Pressed 두 단계 규칙, Selected · Disabled · Focus · 입력창 상태'],
        ['<a href="tokens.html">Tokens</a>', 'Foundation', chip('ok', '초안'), '토큰 규칙(이름 · 고르는 순서 · 추가 규칙)과 버전별 JSON 다운로드'],
        ['<a href="spacing.html">Spacing</a>', 'Foundation', chip('ok', '확정'), '4~24 여섯 단계 + 섹션 간격 32 · 40, 화면 좌우 여백 screen-x'],
        ['Layout', 'Foundation', chip('todo', '준비 중'), '화면 격자와 너비 기준 정의 예정'],
        ['<a href="app-bar.html">App Bar</a>', 'Component', chip('ok', '확정'), 'Home, Sub, 어두운 배경용'],
        ['<a href="navigation-bar.html">Navigation Bar</a>', 'Component', chip('ok', '확정'), '탭 3개, 기본·호버·눌림 상태'],
        ['<a href="avatar.html">Avatar</a>', 'Component', chip('ok', '확정'), '사용자 아이콘, 프로필 사진'],
        ['<a href="empty-state.html">Empty State</a>', 'Component', chip('ok', '확정'), '안내 문구 + 아이콘 선택, 테두리 None · Dashed'],
        ['<a href="badge.html">Badge</a>', 'Component', chip('ok', '확정'), '읽기 전용 라벨, Blue · White · Gray × 22 · 25'],
        ['<a href="chip-button.html">Chip Button</a>', 'Component', chip('ok', '확정'), 'Multi Choice, 아이콘 포함, Two Choice 카드, 4가지 상태'],
        ['<a href="fields.html">Fields</a>', 'Component', chip('ok', '확정'), 'Text Input, Text Area, Select Field, 7가지 상태'],
        ['<a href="tabs.html">Tabs</a>', 'Component', chip('ok', '확정'), 'Text 탭(왼쪽 정렬·같은 너비), Box 탭(Scrollable·같은 너비), 호버 상태'],
        ['<a href="date-picker.html">Date Time Picker</a>', 'Component', chip('ok', '확정'), '날짜·시간을 함께 고르는 바텀시트, Day 상태 6개, 12시간제'],
        ['<a href="controls.html">Controls</a>', 'Component', chip('ok', '확정'), '체크박스, 라디오(새로 추가), 라벨 왼쪽·오른쪽, 호버·눌림'],
        ['<a href="scroll-bar.html">Scroll Bar</a>', 'Component', chip('ok', '확정'), '기본·호버·눌림'],
        ['<a href="lists.html">Lists</a>', 'Component', chip('ok', '확정'), '체크박스 리스트, 아이콘 리스트(순서 변경·삭제)'],
        ['<a href="accordion.html">Accordion</a>', 'Component', chip('ok', '확정'), 'Index Title·Index·Index Item, Contents(접기·펼치기)'],
        ['<a href="toast.html">Toast</a>', 'Component', chip('ok', '확정'), 'Text·Info·Caution, 3초 뒤 사라짐, 위치 4가지'],
        ['<a href="tooltip.html">Tooltip</a>', 'Component', chip('ok', '확정'), 'Function(화살표 5방향 × Blue·Gray), Hover, Guide'],
        ['<a href="popup.html">Popup</a>', 'Component', chip('ok', '확정'), 'Basic·With Illustration × Single·Side by Side·Stacked, 제목·부제 선택'],
        ['<a href="bottom-sheet.html">Bottom Sheet</a>', 'Component', chip('ok', '확정'), 'Short(내용에 맞춤) 4종 × 버튼, Long(670) 4종, 일러스트 교체'],
        ['<a href="progress-bar.html">Progress Bar</a>', 'Component', chip('ok', '확정'), '2·3·4단계, 현재 단계 선택'],
        ['<a href="button.html">Button</a>', 'Component', chip('ok', '확정'), 'Filled 5 · Ghost 2 · Outlined 2 · Floating, 48/40px(Filled는 웹 36px까지), 버튼 그룹'],
    ]
    content = page_head('Layer Design System', '레이어 디자인시스템 문서',
        '레이어 앱 화면에 쓰는 색, 글꼴, 그림자, 아이콘, 컴포넌트를 한곳에 모은 문서입니다. 디자이너와 개발자, AI가 같은 이름으로 같은 값을 쓰도록 하는 것이 목적입니다.',
        extra='<a href="https://www.figma.com/community/file/1699490552460986431/layer-ds" target="_blank" rel="noopener">Figma 커뮤니티 파일</a>')
    content += f'''
<section class="section">
  <h2>만드는 방식</h2>
  <div class="principles">
    <div><h3>실제 화면에서 출발합니다</h3><p>값을 미리 정해두지 않습니다. Figma에서 만든 컴포넌트와 화면을 코드로 옮기면서, 반복해서 쓰인 값만 토큰으로 만듭니다.</p></div>
    <div><h3>결정은 기록으로 남깁니다</h3><p>분석하다 발견한 불일치는 담당자가 결정하고, 그 결과를 <a href="updates.html">업데이트</a>에 날짜와 함께 남깁니다.</p></div>
    <div><h3>Figma와 코드가 같은 이름을 씁니다</h3><p><code>Title 18 Bold</code>는 코드에서도 <code>.text-title-18-bold</code>입니다. 이름만 알면 어디서든 찾을 수 있습니다.</p></div>
  </div>
</section>
<section class="section">
  <h2>진행 상태</h2>
  {table(['영역', '구분', '상태', '내용'], rows)}
</section>
<section class="section">
  <h2>코드에서 쓰기</h2>
  <p>토큰과 컴포넌트는 CSS 파일로 제공합니다. 필요한 파일을 불러온 뒤 클래스 이름을 붙이면 됩니다.</p>
  {code("""<link rel="stylesheet" href="css/typography.css">
<link rel="stylesheet" href="css/color.css">
<link rel="stylesheet" href="css/elevation.css">
<link rel="stylesheet" href="css/icons.css">
<link rel="stylesheet" href="css/components.css">
<link rel="stylesheet" href="css/buttons.css">

<h2 class="text-title-18-bold">이번 주 회고</h2>
<div class="elevation-100">…</div>""")}
</section>
<section class="section">
  <h2>다음 계획</h2>
  <ol class="steps">
    <li><strong>입력창, 카드</strong> 기본 컴포넌트 2~3개를 더 분석합니다.</li>
    <li><strong>실제 화면</strong> 컴포넌트를 쓰는 화면 1~2개를 분석합니다.</li>
    <li><strong>토큰 정리</strong> 모인 값으로 Color(용도), Spacing, Radius 토큰을 만들고 Color 페이지를 새 기준으로 맞춥니다.</li>
  </ol>
</section>'''
    return content

def swatch(fam, slug, s, h, primary):
    light = int(h[0:2], 16) * 0.299 + int(h[2:4], 16) * 0.587 + int(h[4:6], 16) * 0.114 > 150
    tag = f'<span class="sw-tag" style="color:{"#212329" if light else "#fff"}">Primary</span>' if primary else ''
    return (f'<button type="button" class="sw" data-copy="#{h}" data-copy-msg="#{h} 복사했어요" aria-label="{fam} {s} #{h} 복사">'
            f'<span class="sw-chip" style="background:#{h}">{tag}</span><span class="sw-name">{fam} {s}</span><span class="sw-hex mono">#{h}</span></button>')

def p_color():
    content = page_head('Foundations', 'Color', 'Layer의 원색 팔레트입니다. 무채색 Gray를 기본으로, Blue를 브랜드 색으로, Green·Red·Orange를 상태 표시에 씁니다. 견본을 누르면 색상 값이 복사됩니다.',
                        status=('wait', '검토 중'), node='1-3324')
    content += '<div class="callouts">' + callout('wait', '검토 중', '2026-10-26', '아래 팔레트는 Figma Color 페이지의 값입니다. 텍스트, 배경, 테두리처럼 <strong>용도별 색 이름</strong>은 Button 등 컴포넌트를 분석해 근거가 모이면 추가합니다.') + '</div>'
    for group, fams in PALETTE:
        subs = ''
        for fam, slug, steps, prim in fams:
            cols = len(steps)
            sws = ''.join(swatch(fam, slug, s, h, s == prim) for s, h in steps)
            subs += f'<div class="sub"><h3>{fam}</h3><div class="swatches" style="--n:{cols}">{sws}</div></div>'
        content += f'<section class="section"><h2>{group}</h2>{subs}</section>'
    ops = ''.join(f'<button type="button" class="sw" data-copy="var(--color-opacity-{o})" data-copy-msg="Opacity {o} 토큰 복사했어요" aria-label="Opacity {o} 복사">'
                  f'<span class="sw-chip sw-chip--checker"><span style="background:rgb(6 8 12 / {int(o)/100:g})"></span></span><span class="sw-name">Opacity {o}</span><span class="sw-hex mono">#06080C · {o}%</span></button>' for o in OPACITY)
    content += f'''<section class="section"><h2>Opacity</h2><p>모두 같은 색(#06080C)에 투명도만 다릅니다. 그림자, 구분선, 딤 처리에 씁니다.</p><div class="swatches" style="--n:10">{ops}</div></section>'''
    uses = [
        ['Gray 400 → 600 → 900', '내비게이션 탭의 기본 → 호버 → 선택 아이콘', '<a href="navigation-bar.html">Navigation Bar</a>'],
        ['Gray 600 / 900', '내비게이션 라벨(기본 / 선택)', '<a href="navigation-bar.html">Navigation Bar</a>'],
        ['Gray 400', '프로필 기본 배경, Emotion 아이콘 비활성', '<a href="avatar.html">Avatar</a>, <a href="iconography.html">Iconography</a>'],
        ['Blue 600', '앱바 텍스트 버튼, 그래픽 아이콘 주색', '<a href="app-bar.html">App Bar</a>, <a href="iconography.html">Iconography</a>'],
        ['Blue 50 ~ 800', '그래픽 아이콘과 Emotion 아이콘 전체', '<a href="iconography.html">Iconography</a>'],
        ['Opacity 4 · 8 · 12 · 22', '그림자 4단계의 진하기', '<a href="elevation.html">Elevation</a>'],
        ['Opacity 4', '내비게이션 바 위쪽 구분선', '<a href="navigation-bar.html">Navigation Bar</a>'],
        ['Gray 900 → 800 → 700', 'Primary·Floating 버튼 배경(기본 → 호버 → 눌림), 버튼 기본 글자색', '<a href="button.html">Button</a>'],
        ['Gray 300 → 400 → 500', 'Secondary 버튼 배경, Outlined 테두리(Gray 300)', '<a href="button.html">Button</a>'],
        ['Gray 0 → 100 → 200', 'White·Ghost·Outlined 버튼 배경', '<a href="button.html">Button</a>'],
        ['Gray 100 / 400', '모든 버튼의 비활성 배경 / 글자', '<a href="button.html">Button</a>'],
        ['Blue 600 → 700 → 800', 'Blue 버튼 배경', '<a href="button.html">Button</a>'],
        ['Blue 100 → 200 → 300', 'Light Blue 버튼 배경, Outlined Blue 테두리(Blue 300)', '<a href="button.html">Button</a>'],
        ['Blue 0 → 50 → 100', 'Ghost·Outlined Blue 버튼 배경, 글자 Blue 600', '<a href="button.html">Button</a>'],
        ['Gray 100 → 200 / Blue 600', '칩 배경(기본 → 호버 / 선택), 글자 Gray 800', '<a href="chip-button.html">Chip Button</a>'],
        ['Blue 600 / Opacity 4', '진행 막대(지난 단계 / 남은 단계)', '<a href="progress-bar.html">Progress Bar</a>'],
        ['Gray 300 → Blue 600 / Gray 200', '입력창 테두리(기본 → 포커스·입력 중·오류 / 비활성)', '<a href="fields.html">Fields</a>'],
        ['Gray 900 / Gray 500 / Gray 300', '입력한 글자 / 안내 문구·글자 수 / 비활성 글자', '<a href="fields.html">Fields</a>'],
        ['Red 500', '입력 오류 안내 문구 · 메뉴 위험 행동', '<a href="fields.html">Fields</a> · <a href="popover.html">Menu</a>'],
        ['Gray 500 → 600 → 900', 'Text 탭 글자(선택 안 됨 → 호버 → 선택), 선택 밑줄 Gray 900', '<a href="tabs.html">Tabs</a>'],
        ['Gray 100 → 200 / Gray 800', 'Box 탭 배경(기본 → 호버 / 선택)', '<a href="tabs.html">Tabs</a>'],
        ['Blue 600 → 700 → 800 / Blue 400', '체크박스·라디오 선택(기본 → 호버 → 눌림 / 비활성)', '<a href="controls.html">Controls</a>'],
        ['Gray 400 → 500 → 600', '체크박스·라디오 테두리(기본 → 호버 → 눌림)', '<a href="controls.html">Controls</a>'],
        ['Opacity 22 → 32 → 48', '스크롤 바 막대(기본 → 호버 → 눌림)', '<a href="scroll-bar.html">Scroll Bar</a>'],
        ['Gray 100 → 200 → 300 / Blue 200', '아코디언·Index 항목 배경(기본 → 호버 → 눌림 / 선택)', '<a href="accordion.html">Accordion</a>'],
        ['Gray 800 / Gray 400 / Red 500', '숫자 동그라미 / 순서 변경 아이콘 / 삭제 아이콘', '<a href="lists.html">Lists</a>'],
        ['Opacity 86 / Blue 600 / Red 500', '토스트 배경 / Info 아이콘 / Caution 아이콘', '<a href="toast.html">Toast</a>'],
        ['Gray 100 → 200 / Blue 600 / Gray 400', '날짜(호버 → 눌림 / 선택·오늘 / 고를 수 없음)', '<a href="date-picker.html">Date Time Picker</a>'],
        ['Gray 0 / Gray 900 / Gray 500 / Opacity 72', '팝업 카드 / 제목 / 부제 / 딤드', '<a href="popup.html">Popup</a>'],
        ['Gray 0 / Gray 900 / Opacity 72', '바텀시트 / 제목 / 딤드', '<a href="bottom-sheet.html">Bottom Sheet</a>'],
        ['Blue 600 / Gray 900 / Blue 100', 'Function 툴팁(Blue·Gray), Hover 툴팁 / Guide 툴팁 배경', '<a href="tooltip.html">Tooltip</a>'],
    ]
    content += f'''<section class="section"><h2>지금까지 확인된 사용처</h2><p>분석한 페이지에서 실제로 쓰인 곳입니다. 용도별 색 이름은 이 표가 쌓이면서 정해집니다.</p>{table(['색', '사용처', '근거'], uses)}</section>'''
    content += f'''<section class="section"><h2>코드</h2><p><code>css/color.css</code>에 팔레트 전체(<code>--color-이름-단계</code>)와 아래 역할 토큰(<code>--color-역할</code>)이 들어 있습니다. 컴포넌트에서는 역할 토큰을 먼저 씁니다.</p>{code("""/* 역할 토큰 (권장) */
color: var(--color-text-primary);
background: var(--color-bg-secondary);
border-color: var(--color-border-default);

/* 역할이 없는 곳은 팔레트 단계 */
color: var(--color-gray-600);""")}</section>'''
    rrows = [[f'<span class="role-sw" style="background:var(--color-{prim})"></span><button type="button" class="token" data-copy="var({role_css(n)})">{n}</button>', f'<span class="mono small">{role_css(n)}</span>', lab, use] for n, lab, prim, use in ROLES]
    content += f'''<section class="section"><h2>역할 토큰</h2><p>컴포넌트를 만들 때는 팔레트 단계보다 이 역할 토큰을 먼저 고릅니다. 실제로 쓰이는 곳이 있는 것만 19개로 정리했습니다. Hover·Pressed는 <a href="state.html">State</a> 규칙(팔레트 한 칸·두 칸)을 따르므로 역할 토큰을 따로 두지 않습니다.</p>
{table(['토큰', '코드', '값', '쓰는 곳'], rrows)}</section>'''
    content += f'''<section class="section"><h2>Figma 변수</h2><p>Figma의 <strong>Color</strong> 변수 모음에 팔레트 55개가 코드와 같은 이름으로 들어 있고, <strong>Color Role</strong> 모음에 역할 토큰 19개가 팔레트를 가리키는 별칭으로 들어 있습니다. 팔레트 변수는 고르기 목록에서 숨기고 역할 토큰만 보이게 했습니다.</p>
{table(['Figma 변수', '코드 토큰', '예'], [['color/gray/0 ~ color/gray/900', '--color-gray-0 ~ 900', 'Gray 0 = #FFFFFF, 예전 스타일 이름은 Gray/000'], ['color/blue/50 ~ 900 · purple · green · red · orange', '--color-blue-600 등', '단계 번호가 그대로 이름'], ['color/opacity/4 ~ 100', '--color-opacity-72 등', '#06080C에 투명도가 값 안에 들어 있음(칠 불투명도는 100%)']])}
<p class="note">모든 변수에 코드 이름(var(--color-text-primary) 등)과 쓰는 곳 설명이 들어 있어 Dev Mode와 Figma MCP에서 그대로 읽힙니다. 글자 토큰은 글자 색에서, 바탕 토큰은 채우기에서, 테두리 토큰은 선 색에서만 고를 수 있습니다.</p></section>'''
    content += '<section class="section"><h2>결정 기록</h2><div class="callouts">' + callout('ok', '추가', '2026-10-27', '역할 토큰 19개를 만들고 컴포넌트의 기본 상태 색 414곳을 팔레트에서 역할 토큰으로 옮겼습니다. Hover·Pressed 상태는 팔레트 단계를 그대로 씁니다.') + callout('ok', '반영', '2026-10-27', 'Figma에 Color 변수 55개를 만들고, 컴포넌트와 문서 대지에서 Color 스타일로 연결된 색 1,851곳을 같은 이름의 변수로 옮겼습니다. 값은 원래 스타일과 모두 같은 것을 확인했습니다. 스타일 없이 숫자로만 들어 있던 팔레트 색 28곳(진행 바, 토스트, 스크롤 바 등)도 변수에 연결했습니다.') + callout('wait', '확인 필요', '2026-10-27', '변수로 옮기지 않은 것: 서비스 대표 화면과 AI 시안(문서가 아닌 화면), 외부 라이브러리 컴포넌트(상태 바, 홈 표시줄, 키보드, Fields 대지에 남은 외부 Text Input), Lists 대지의 숨은 레이어 2개(brand Navy 스타일, #191926), 아이콘 안의 검정. Profile 배경 #D0D3DB는 2026-10-28에 Gray 400으로 맞췄습니다.') + callout('ok', '반영', '2026-10-26', 'Orange 300 라벨이 "Orange / 00"으로 잘못 적혀 있던 것을 Figma와 코드 모두 "Orange / 300"으로 고쳤습니다.') + '</div></section>'
    return content

def p_typography():
    rows = []
    for name, size, lh, w, cls in TYPE:
        rows.append([f'<span class="text-{cls} type-sample">{name}</span>', f'{size}px', lh, w,
                     f'<button type="button" class="token" data-copy="text-{cls}">.text-{cls}</button>'])
    content = page_head('Foundations', 'Typography', '모든 글자는 Pretendard 한 가지 글꼴로 씁니다. 국문, 영문, 숫자를 모두 같은 글꼴로 쓰고, 아래 22개 스타일 밖의 크기나 굵기는 만들지 않습니다.',
                        status=('ok', '확정'), node='1-3589')
    content += f'''<section class="section">
  <h2>글꼴</h2>
  <div class="canvas type-hero"><span class="type-hero__big">가나다 Aa 123</span><span class="type-hero__meta">Pretendard · 500 Medium · 600 SemiBold · 700 Bold</span></div>
  {table(['항목', '값'], [['글꼴', 'Pretendard'], ['굵기', '500 Medium, 600 SemiBold, 700 Bold'], ['행간', '140% (Heading 28 · 24는 150%, 긴 글 Body 15 Long은 180%)'], ['웹', 'Heading 28은 웹(1440) 페이지 제목, 섹션 제목 · 웹 카드 제목은 Title 15 Bold, 소제목 · 접기 제목 · 이전/다음 · 템플릿 카드 제목은 Title 14 Bold, 모달 제목은 Title 22 Bold'], ['자간', '0'], ['글꼴 기능', '<code>case</code>, <code>ss02</code> 켜기']])}
</section>
<section class="section">
  <h2>텍스트 스타일</h2>
  <p>이름은 <strong>역할 · 크기 · 굵기</strong> 순서입니다. 클래스 이름을 누르면 복사됩니다.</p>
  {table(['스타일', '크기', '행간', '굵기', '클래스'], rows, num_cols=(1, 2))}
</section>
<section class="section">
  <h2>역할별 쓰임</h2>
  {table(['역할', '쓰는 곳'], [['Heading', '화면의 가장 큰 제목. 예: Home 앱바의 "회고"'], ['Title', '카드나 섹션의 제목'], ['Subtitle', '서브 화면 앱바 제목, 라벨, 중간 강조'], ['Body', '본문과 설명'], ['Caption', '내비게이션 라벨, 배지, 부가 정보']])}
</section>
<section class="section">
  <h2>코드</h2>
  {code("""<h1 class="text-heading-24-bold">회고</h1>
<p class="text-body-15-medium">이번 주에 잘한 일을 적어 보세요.</p>

/* 직접 조합할 때 */
font-size: var(--font-size-16);
font-weight: var(--font-weight-semibold);
line-height: var(--line-height-140);""")}
  <p class="note">문서 사이트의 큰 제목(56px)처럼 앱 화면에서 쓰지 않는 크기는 토큰에 넣지 않았습니다.</p>
</section>
<section class="section"><h2>결정 기록</h2><div class="callouts">
  {callout('ok', '반영', '2026-10-28', '텍스트 스타일 16개를 원본 라이브러리에서 이 파일의 로컬 스타일로 옮겼습니다. 이름과 값은 그대로이고, 각 스타일 설명에 코드 클래스(.text-body-15-medium 등)를 적었습니다. 이 과정에서 Figma의 Caption/10 Bold도 확정대로 10px이 되었습니다(번호 동그라미 등 6곳). 같은 이름으로 두 개 있던 Subtitle/14 SemiBold는 하나로 합쳤습니다.')}
  {callout('ok', '확정', '2026-10-26', 'Caption 10 Bold는 <strong>10px</strong>이 맞습니다. Figma 텍스트 스타일에는 11px로 설정돼 있지만, 이름과 표 기준으로 확정했습니다. 원본 라이브러리는 수정하지 않습니다.')}
  {callout('ok', '확정', '2026-10-26', 'Title 18 Bold의 행간은 <strong>140%</strong>입니다. Figma 스타일의 150%가 아니라 다른 Title과 같은 값으로 확정했습니다.')}
</div></section>'''
    return content

LEVELS = [('100', 'Card', 'card', '카드, 리스트 묶음', '0 4px 12px rgb(6 8 12 / 4%)'),
          ('200', 'Floating Button', 'floating-button', '떠 있는 버튼', '0 4px 8px / 12% + 0 1px 4px / 8%'),
          ('300', 'Layer', 'layer', '드롭다운, 팝오버 같은 겹침 화면', '0 4px 12px / 12% + 0 4px 8px / 8%'),
          ('400', 'Modal / Bottom Sheet', 'modal', '모달, 바텀시트', '0 4px 12px / 22% + 0 4px 8px / 8%')]
def p_elevation():
    cards = ''.join(f'<div class="lvl"><div class="lvl-card elevation-{n}"></div><div><p class="text-subtitle-16-semibold lvl-name">Shadow {n}</p><p class="text-body-14-medium lvl-use">{u}</p></div></div>' for n, u, *_ in LEVELS)
    rows = [[f'Shadow {n}', u, f'<button type="button" class="token" data-copy="var(--shadow-{s})">--shadow-{s}</button>', f'<button type="button" class="token" data-copy="elevation-{n}">.elevation-{n}</button>', f'<span class="mono small">{v}</span>'] for n, u, s, d, v in LEVELS]
    content = page_head('Foundations', 'Elevation', '그림자로 화면 위에 떠 있는 정도를 나타냅니다. 숫자가 클수록 더 위에 있는 요소입니다. 화면을 만들 때는 진하기보다 용도 이름(Card, Modal 등)으로 고르세요.',
                        status=('ok', '확정'), node='1-4091')
    content += f'''<section class="section"><h2>단계</h2><div class="canvas canvas--sunk lvl-stage">{cards}</div></section>
<section class="section"><h2>토큰</h2>{table(['단계', '용도', '용도 토큰', '클래스', '값'], rows)}
<p class="note">그림자 색은 모두 #06080C이고, 진하기 4·8·12·22%는 <a href="color.html">Color</a>의 Opacity 단계와 같습니다.</p></section>
<section class="section"><h2>코드</h2>{code("""/* 용도로 고르기 (권장) */
box-shadow: var(--shadow-card);

/* 클래스 */
<div class="elevation-400">바텀시트</div>""")}</section>
<section class="section"><h2>Figma 스타일</h2><p>Shadow/100 ~ 400은 이 파일의 로컬 그림자 스타일입니다(2026-10-28, 원본 라이브러리에서 같은 값으로 옮김). 각 스타일 설명에 용도 토큰 이름(--shadow-modal 등)을 적었습니다.</p></section>
<section class="section"><h2>열린 질문</h2><div class="callouts">
  {callout('wait', '확인 필요', '2026-10-26', 'Shadow 300·400은 "진한 그림자 + 아래 옅은 그림자(4px 위치, 8px 흐림, 8%)" 구조인데, Shadow 200만 아래 그림자가 1px 위치, 4px 흐림입니다. 그래서 200과 300이 화면에서 거의 구분되지 않습니다. 의도한 차이인지 정해야 합니다.')}
</div></section>'''
    return content

RADII = [
    (4, '--radius-4', 'Checkbox', '체크박스'),
    (6, '--radius-6', 'Chip · Box 탭 38', '작은 칩 버튼, Box 탭'),
    (8, '--radius-8', 'Chip 48 · Tooltip · 목록 카드', '칩 버튼 48, Function·Guide 툴팁, 아이콘 리스트 카드, 체크박스·라디오 누름 영역'),
    (10, '--radius-10', 'Button 40', '작은 버튼(40)'),
    (12, '--radius-12', 'Button 48 · Field · Card', '버튼 48, 입력창·선택창, Two Choice 카드, 토스트, 아코디언'),
    (16, '--radius-16', 'Popup · Bottom Sheet · 웹 카드', '팝업, 바텀시트(위 두 모서리만), 웹의 넓은 섹션 카드(--radius-card-lg)'),
    ('Full', '--radius-full', 'Pill · Circle', 'Floating 버튼, 아바타, 라디오, 날짜 칸, 진행 바, 스크롤 바, 순서 번호'),
]
def p_radius():
    def box(v):
        r = '999px' if v == 'Full' else f'{v}px'
        return f'<div class="rd-item"><div class="rd-box" style="border-radius:{r}"></div><p class="text-subtitle-16-semibold rd-name">Radius {v}</p><p class="text-body-14-medium rd-val">{"원·알약" if v == "Full" else r}</p></div>'
    stage = ''.join(box(v) for v, *_ in RADII)
    rows = [[f'Radius {v}', '999px' if v == 'Full' else f'{v}px', f'<button type="button" class="token" data-copy="var({t})">{t}</button>', u] for v, t, _, u in RADII]
    pairs = [['Button', '48 → <strong>12</strong>', '40 → <strong>10</strong>', '<a href="button.html">Button</a>'],
             ['Chip Button · Box 탭', '48 → <strong>8</strong>', '38 → <strong>6</strong> (Box 탭은 38만 있음)', '<a href="chip-button.html">Chip Button</a>, <a href="tabs.html">Tabs</a>'],
             ['Floating 버튼', '48 → <strong>Full</strong>', '40 → <strong>Full</strong>', '<a href="button.html">Button</a>']]
    content = page_head('Foundations', 'Radius', '모서리 둥글기는 일곱 단계만 씁니다. 지금까지 정리한 컴포넌트에서 쓰인 값을 모은 것이고, 면이 클수록 더 둥글게 합니다.',
                        status=('ok', '확정'))
    content += f'''<section class="section"><h2>단계</h2><div class="canvas canvas--sunk rd-stage">{stage}</div></section>
<section class="section"><h2>토큰</h2>{table(['단계', '값', '토큰', '쓰는 곳'], rows)}
<p class="note">용도 토큰도 함께 있습니다. --radius-button(12), --radius-button-sm(10), --radius-button-xs(8), --radius-chip(8), --radius-chip-sm(6), --radius-field(12), --radius-card(12), --radius-card-lg(16, 웹 섹션 카드), --radius-toast(12), --radius-tooltip(8), --radius-modal(16), --radius-pill(Full).</p></section>
<section class="section"><h2>고르는 기준</h2>
<p>작은 조각에서 큰 면으로 갈수록 둥글기가 커집니다. 체크박스(4) → 칩·툴팁(8) → 버튼·입력창·카드(12) → 화면 위에 뜨는 팝업·바텀시트(16) 순서입니다.</p>
<p>같은 컴포넌트가 크기만 다르면 높이에 맞춰 한 단계 줄입니다.</p>
{table(['컴포넌트', '큰 크기', '작은 크기', '페이지'], pairs)}
<p>칩과 Box 탭은 같은 높이의 버튼보다 덜 둥글게 씁니다. 48 높이에서 버튼은 12, 칩은 8입니다.</p>
<p>바텀시트는 화면 아래에 붙기 때문에 위 두 모서리만 16을 주고 아래는 0입니다.</p></section>
<section class="section"><h2>코드</h2>{code("""<link rel="stylesheet" href="css/radius.css">

/* 용도로 고르기 (권장) */
border-radius: var(--radius-button);

/* 단계로 고르기 */
border-radius: var(--radius-12);

/* 클래스 */
<div class="radius-16-top">바텀시트</div>""")}</section>
<section class="section"><h2>Figma 변수</h2><p>Figma의 <strong>Radius</strong> 변수 모음에 radius/4 · 6 · 8 · 10 · 12 · 16 · full 일곱 개가 있고, 코드 이름(var(--radius-12) 등)이 함께 들어 있습니다. 모서리 둥글기 칸에서만 고를 수 있게 범위를 정해 두었습니다. full은 999로, 높이의 절반보다 크게 줘서 원·알약 모양을 만듭니다.</p>
<p>용도 이름(radius/button · button-sm · button-xs · chip · chip-sm · field · card · toast · tooltip · list-card · checkbox · modal · pill)도 같은 모음에 단계를 가리키는 별칭으로 들어 있고, 해당 컴포넌트는 용도 이름에 연결되어 있습니다.</p>
<p>컴포넌트의 모서리 값은 모두 이 변수에 연결되어 있습니다(버튼, 칩, 탭, 입력창, 체크박스·라디오, 목록, 아코디언, 팝업, 바텀시트, 날짜 선택, 토스트, 툴팁, 진행 바, 스크롤 바, 태그).</p></section>
<section class="section"><h2>결정 기록</h2><div class="callouts">
  {callout('ok', '반영', '2026-10-27', '<a href="lists.html">아이콘 리스트</a>의 삭제 아이콘 바탕 3.6px를 Radius 4로 맞췄습니다.')}
  {callout('ok', '추가', '2026-10-27', 'Figma에 Radius 변수 7개를 만들고 컴포넌트 모서리 1,160곳에 연결했습니다.')}
  {callout('ok', '정리', '2026-11-02', '정리 전이던 Component 18(진행 중 · 미달성 · 완료 상태 드롭다운)은 쓰이는 곳이 없어 컴포넌트를 해제하고 디자인으로만 남겼습니다. 모서리 3 문제도 함께 대상에서 빠졌습니다.')}
</div></section>'''
    return content

def sw(hex_, label, ink=False, border=False):
    style = f'background:{hex_};' + ('color:#fff;' if ink else '') + ('box-shadow:inset 0 0 0 1px #dfe3ea;' if border else '')
    return f'<span class="st-sw" style="{style}">{label}</span>'
STEPS = [
    ('밝은 회색 채움', 'Accordion · Index 항목 · 아코디언 제목', [('#f2f4f8', 'Gray 100'), ('#edf0f4', 'Gray 200'), ('#dfe3ea', 'Gray 300')]),
    ('흰 · 투명 바탕', 'White · Ghost · Outlined 버튼, 날짜 칸', [('#ffffff', 'Gray 0', False, True), ('#f2f4f8', 'Gray 100'), ('#edf0f4', 'Gray 200')]),
    ('중간 회색 채움', 'Secondary 버튼', [('#dfe3ea', 'Gray 300'), ('#ced2da', 'Gray 400'), ('#a9afbb', 'Gray 500')]),
    ('연한 파랑 채움', 'Light Blue 버튼', [('#e9f0ff', 'Blue 100'), ('#e2ebfe', 'Blue 200'), ('#c4d7fd', 'Blue 300')]),
    ('투명 · 파랑 글자', 'Ghost Blue · Outlined Blue 버튼', [('#ffffff', '투명', False, True), ('#f1f6ff', 'Blue 50'), ('#e9f0ff', 'Blue 100')]),
    ('파랑 채움', 'Blue 버튼, 체크된 체크박스·라디오', [('#6c9cfa', 'Blue 600', True), ('#415e96', 'Blue 700', True), ('#2b3e64', 'Blue 800', True)]),
    ('가장 진한 채움', 'Primary · Floating 버튼 (더 진한 색이 없어 밝아집니다)', [('#212329', 'Gray 900', True), ('#454952', 'Gray 800', True), ('#666b75', 'Gray 700', True)]),
    ('테두리', '체크박스·라디오 테두리(체크 전)', [('#ced2da', 'Gray 400'), ('#a9afbb', 'Gray 500'), ('#8b909c', 'Gray 600', True)]),
    ('스크롤 막대', '<a href="scroll-bar.html">Scroll Bar</a>', [('rgb(6 8 12 / .22)', 'Opacity 22'), ('rgb(6 8 12 / .32)', 'Opacity 32', True), ('rgb(6 8 12 / .48)', 'Opacity 48', True)]),
]
def p_state():
    head = '<div class="st-row st-row--head"><span></span><span>Default</span><span>Hover</span><span>Pressed</span></div>'
    rows = ''.join(f'<div class="st-row"><span class="st-name"><strong>{n}</strong><small>{u}</small></span>' + ''.join(sw(*c) for c in cs) + '</div>' for n, u, cs in STEPS)
    kinds = [['Default', '아무 일도 없는 기본 모습', '—'],
             ['Hover', '마우스를 올렸을 때(웹). 팔레트 한 단계', ':hover · .is-hover'],
             ['Pressed', '누르는 동안. 팔레트 두 단계', ':active · .is-pressed'],
             ['Selected', '고른 상태가 유지될 때', 'aria-pressed · aria-selected · aria-current'],
             ['Focus', '키보드로 옮겨 왔을 때(코드 전용). 2px Blue 600', ':focus-visible'],
             ['Disabled', '지금은 쓸 수 없을 때', ':disabled · .is-disabled'],
             ['Error', '입력값이 잘못됐을 때(입력창)', '.is-error']]
    selected = [['<a href="chip-button.html">Chip Button</a>, <a href="date-picker.html">날짜 칸</a>', 'Blue 600 바탕 + 흰 글자', 'Pressed와 같은 모습이 그대로 남습니다'],
                ['<a href="tabs.html">Box 탭</a>', 'Gray 800 바탕 + 흰 글자', ''],
                ['<a href="tabs.html">Text 탭</a>', 'Gray 900 글자 + 2px 밑줄', '고르지 않은 탭은 Gray 500, Hover는 Gray 600'],
                ['<a href="controls.html">체크박스 · 라디오</a>', 'Blue 600 채움 + 흰 체크', ''],
                ['<a href="accordion.html">Accordion Index 항목</a>', 'Blue 200 바탕', '목록 안에서 현재 위치'],
                ['<a href="navigation-bar.html">Navigation Bar</a>', 'Gray 900 아이콘 · 글자', '고르지 않은 탭은 Gray 600']]
    disabled = [['버튼 (Filled · Ghost · Outlined · Floating)', 'Gray 100 바탕 + Gray 400 글자', '모든 버튼이 같은 모습. Floating은 그림자 유지'],
                ['Chip Button', 'Gray 100 바탕 + Gray 400 글자, 아이콘 40%', '버튼과 같음'],
                ['체크박스 · 라디오', 'Gray 100 채움 + Gray 200 테두리 · 체크된 것은 Blue 400', '라벨은 Gray 400'],
                ['날짜 칸', '바탕 없음 + Gray 400 글자', ''],
                ['입력창 · 선택창', 'Gray 200 테두리 + Gray 300 글자', '<a href="fields.html">Fields</a> 결정대로 유지']]
    fields = [['Default', 'Gray 300 테두리'], ['Focus · Typing', 'Blue 600 테두리, 커서 Blue 600'], ['Typed', '값이 있고 포커스가 없을 때, Default 테두리'],
              ['Error · OverTyping', 'Blue 600 테두리 유지 + 아래 Red 500 안내 문구'], ['Disabled', 'Gray 200 테두리 + Gray 300 글자']]
    content = page_head('Foundations', 'State', '상태는 사용자의 행동에 컴포넌트가 답하는 방식입니다. Hover는 팔레트를 한 단계, Pressed는 두 단계 옮기는 것이 기본 규칙입니다. 지금까지 정리한 컴포넌트의 상태 색을 모아 보면 모두 이 규칙을 따릅니다.',
                        status=('ok', '확정'))
    content += f'''<section class="section"><h2>상태 종류</h2>{table(['상태', '뜻', '코드'], kinds)}</section>
<section class="section"><h2>Hover · Pressed 규칙</h2><p>기본색에서 <a href="color.html">팔레트</a>를 한 칸(Hover), 두 칸(Pressed) 옮깁니다. 밝은 색은 진해지고, 가장 진한 Gray 900은 더 갈 곳이 없어 밝아집니다. 그림자나 크기는 바꾸지 않습니다.</p>
<div class="canvas canvas--sunk st-table">{head}{rows}</div>
<p class="note">Chip Button과 Box 탭은 누르면 바로 Selected 모습(Blue 600, Gray 800)이 됩니다. Text 탭과 Navigation Bar는 바탕 없이 글자색만 바뀝니다.</p></section>
<section class="section"><h2>Selected</h2><p>고른 상태는 컴포넌트마다 표현이 다르지만, 색이 들어간 바탕(Blue 600, Gray 800)이나 가장 진한 글자(Gray 900)로 나머지와 확실히 구분합니다.</p>{table(['컴포넌트', '모습', '참고'], selected)}</section>
<section class="section"><h2>Disabled</h2><p>쓸 수 없는 요소는 Gray 100 바탕과 Gray 400 글자로 흐리게 보입니다. 누를 수 없다는 것 외에 크기나 모양은 그대로입니다.</p>{table(['컴포넌트', '모습', '참고'], disabled)}</section>
<section class="section"><h2>입력창 상태</h2>{table(['상태', '모습'], fields)}<p class="note">오류여도 테두리는 Blue 600을 유지하고, 오류는 아래 안내 문구로 알립니다.</p></section>
<section class="section"><h2>Focus</h2><p>키보드로 옮겨 왔을 때만 보이는 표시입니다. Figma에는 없고 코드에서만 씁니다. 모든 컴포넌트가 <strong>2px Blue 600 테두리</strong>를 쓰고, 버튼·칩처럼 떨어진 요소는 바깥 2px, 탭·내비게이션처럼 붙어 있는 요소는 안쪽 2px에 그립니다.</p>
<div class="canvas st-focus"><button type="button" class="btn btn--primary btn--sm st-fv">바깥 2px</button><span class="st-fv-in">안쪽 2px</span></div></section>
<section class="section"><h2>코드</h2>{code("""/* 실제 동작은 브라우저 상태로 */
.btn--blue:hover  {{ --btn-bg: var(--color-blue-700); }}
.btn--blue:active {{ --btn-bg: var(--color-blue-800); }}
.btn:disabled     {{ --btn-bg: var(--color-gray-100); --btn-fg: var(--color-gray-400); }}
.btn:focus-visible {{ outline: 2px solid var(--color-blue-600); outline-offset: 2px; }}

/* 고른 상태는 ARIA 속성으로 */
<button class="chip-button" aria-pressed="true">팀과 함께</button>
<button role="tab" class="tab" aria-selected="true">유형</button>

/* 문서·시안용으로 상태를 고정할 때 */
<button class="btn btn--blue is-hover">버튼</button>""".replace('{{', '{').replace('}}', '}'))}</section>
<section class="section"><h2>결정 기록</h2><div class="callouts">
  {callout('ok', '정리', '2026-10-27', 'Hover는 팔레트 한 단계, Pressed는 두 단계로 정했습니다. 버튼, 칩, 탭, 체크박스, 아코디언, 날짜 칸이 모두 이 규칙을 따릅니다.')}
  {callout('ok', '확정', '2026-10-27', '입력창 · 선택창의 Disabled 글자는 다른 컴포넌트(Gray 400)보다 연한 Gray 300입니다. Fields에서 정한 대로 유지합니다.')}
  {callout('ok', '정리', '2026-10-27', 'Focus 표시는 코드 전용입니다. 2px Blue 600으로 통일합니다(사이트와 Navigation Bar에서 쓰던 색에 맞춤).')}
</div></section>'''
    return content

SPACES = [(4, '좁은 간격', 'Stacked 버튼 사이, 아이콘과 글자, 체크박스와 라벨'), (8, '나란히 놓인 것 사이', '칩·버튼 나란히, Side by Side 버튼, 컴포넌트 안 묶음'), (12, '조금 떨어진 것 사이', '탭 사이, 제목과 부제, 숫자 동그라미와 글자'),
          (16, '묶음 사이', '카드 안 아이콘과 글자, 입력창 안쪽 위아래'), (20, '화면 여백', '화면 좌우 여백, 카드·토스트 안쪽 여백, 탭·바텀시트 본문'), (24, '덩어리 사이', '바텀시트 본문 위아래, 날짜 선택 칸 사이'),
          (32, '섹션 간격 (작은)', '화면의 큰 덩어리 사이: 상단 박스 ↔ 진행중인 회고 목록(스페이스 상세)'), (40, '섹션 간격 (큰)', '화면의 큰 덩어리 사이: 질문 제목 ↔ 선택지(회고 만들기 단계)')]
LAY_LIST = '<div class="lay-diagram" style="position:relative;flex:none;width:720px;height:450px;background:var(--color-gray-100);border-radius:8px;overflow:hidden;border:1px solid var(--color-gray-200)"><div style="position:absolute;left:0.0px;top:0.0px;width:142.0px;height:450.0px;background:var(--color-bg-surface);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:600;color:#5c616c;text-align:center;line-height:1.3">LNB<br>284</div><div style="position:absolute;left:142.0px;top:0.0px;width:20.0px;height:450.0px;background:rgb(251 92 92 / .22);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:600;color:#e03131;text-align:center;line-height:1.3">40</div><div style="position:absolute;left:700.0px;top:0.0px;width:20.0px;height:450.0px;background:rgb(251 92 92 / .22);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:600;color:#e03131;text-align:center;line-height:1.3">40</div><div style="position:absolute;left:162.0px;top:14.0px;width:538.0px;height:34.0px;background:var(--color-gray-200);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:600;color:#5c616c;text-align:center;line-height:1.3">머리(제목 · 버튼)</div><div style="position:absolute;left:162.0px;top:58.0px;width:148.0px;height:380.0px;background:var(--color-bg-surface);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:600;color:#5c616c;text-align:center;line-height:1.3">카드 열<br>296</div><div style="position:absolute;left:310.0px;top:58.0px;width:20.0px;height:380.0px;background:rgb(251 92 92 / .22);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:600;color:#e03131;text-align:center;line-height:1.3">40</div><div style="position:absolute;left:330.0px;top:58.0px;width:148.0px;height:380.0px;background:var(--color-bg-surface);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:600;color:#5c616c;text-align:center;line-height:1.3">카드 열<br>296</div><div style="position:absolute;left:478.0px;top:58.0px;width:69.0px;height:380.0px;background:transparent;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:600;color:#8b909c;text-align:center;line-height:1.3">남는<br>너비</div><div style="position:absolute;left:547.0px;top:58.0px;width:153.0px;height:380.0px;background:var(--color-bg-surface);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:600;color:#5c616c;text-align:center;line-height:1.3">오른쪽 패널<br>306</div></div>'
LAY_WORK = '<div class="lay-diagram" style="position:relative;flex:none;width:720px;height:450px;background:var(--color-gray-100);border-radius:8px;overflow:hidden;border:1px solid var(--color-gray-200)"><div style="position:absolute;left:0.0px;top:0.0px;width:42.0px;height:450.0px;background:var(--color-bg-surface);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:600;color:#5c616c;text-align:center;line-height:1.3">LNB<br>84</div><div style="position:absolute;left:42.0px;top:0.0px;width:10.0px;height:450.0px;background:rgb(251 92 92 / .22);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:600;color:#e03131;text-align:center;line-height:1.3"></div><div style="position:absolute;left:52.0px;top:14.0px;width:148.0px;height:424.0px;background:var(--color-bg-surface);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:600;color:#5c616c;text-align:center;line-height:1.3">목록 열<br>296</div><div style="position:absolute;left:200.0px;top:0.0px;width:10.0px;height:450.0px;background:rgb(251 92 92 / .22);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:600;color:#e03131;text-align:center;line-height:1.3"></div><div style="position:absolute;left:210.0px;top:0.0px;width:510.0px;height:450.0px;background:var(--color-bg-surface);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:600;color:#5c616c;text-align:center;line-height:1.3"></div><div style="position:absolute;left:210.0px;top:0.0px;width:20.0px;height:450.0px;background:rgb(108 156 250 / .2);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:600;color:#415e96;text-align:center;line-height:1.3">40</div><div style="position:absolute;left:700.0px;top:0.0px;width:20.0px;height:450.0px;background:rgb(108 156 250 / .2);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:600;color:#415e96;text-align:center;line-height:1.3">40</div><div style="position:absolute;left:230.0px;top:12.0px;width:470.0px;height:426.0px;background:var(--color-gray-100);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:600;color:#5c616c;text-align:center;line-height:1.3">작업 패널 내용(남은 너비)</div></div>'
LAY_MOB = '<div class="lay-diagram" style="position:relative;flex:none;width:188px;height:406px;background:var(--color-bg-surface);border-radius:8px;overflow:hidden;border:1px solid var(--color-gray-200)"><div style="position:absolute;left:0.0px;top:0.0px;width:187.5px;height:22.0px;background:var(--color-gray-200);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:600;color:#5c616c;text-align:center;line-height:1.3">상태 바 44</div><div style="position:absolute;left:0.0px;top:22.0px;width:187.5px;height:29.0px;background:var(--color-gray-100);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:600;color:#5c616c;text-align:center;line-height:1.3">앱 바 58</div><div style="position:absolute;left:0.0px;top:51.0px;width:10.0px;height:311.0px;background:rgb(251 92 92 / .22);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:600;color:#5c616c;text-align:center;line-height:1.3"></div><div style="position:absolute;left:177.5px;top:51.0px;width:10.0px;height:311.0px;background:rgb(251 92 92 / .22);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:600;color:#5c616c;text-align:center;line-height:1.3"></div><div style="position:absolute;left:10.0px;top:51.0px;width:167.5px;height:311.0px;background:transparent;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:600;color:#5c616c;text-align:center;line-height:1.3">본문<br>335</div><div style="position:absolute;left:0.0px;top:362.0px;width:187.5px;height:44.0px;background:var(--color-gray-100);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:600;color:#5c616c;text-align:center;line-height:1.3">Navigation Bar 88</div></div>'
def p_layout():
    content = page_head('Foundations', 'Layout', '화면의 틀입니다. 새 화면은 템플릿 세 가지(Web/List · Web/Work · Mobile) 중 하나에서 시작하고, LNB · 앱 바 · 여백은 템플릿이 정한 값을 그대로 씁니다.', status=('ok', '확정'))
    tpl = table(['템플릿', '쓰는 화면', '구조'], [['<strong>Web/List</strong>', '목록 · 대시보드(스페이스, 모달 · 팝오버 뒤 배경)', '펼친 LNB 284 + 여백 40 · 카드 열 296 × n · 사이 40 · 오른쪽 패널 306'], ['<strong>Web/Work</strong>', '작성 · 분석(왼쪽 목록을 보며 오른쪽에서 작업)', '접은 LNB 84 + 여백 20 · 목록 열 296 · 사이 20 · 작업 패널(남은 너비, 안쪽 좌우 40)'], ['<strong>Mobile</strong>', '모든 모바일 화면', '375 × 812 · 상태 바 44 · 앱 바 58 · 본문 좌우 20 · Navigation Bar 88']])
    rules = table(['', '규칙'], [['Do', '새 화면은 템플릿 인스턴스를 놓고 슬롯에 내용을 채웁니다. AI로 화면을 만들 때도 같습니다.'], ['Do', '웹 여백은 템플릿 값만 씁니다. Web/List 40, Web/Work 20, 작업 패널 안쪽 40.'], ["Don't", '18 · 28 · 30 · 68처럼 템플릿에 없는 여백을 쓰지 않습니다. 정리 전 화면에 있던 값입니다.'], ['예외', '웹 홈 대시보드(빈 상태)는 본문을 가운데 정렬(최대 928)합니다.'], ['확장', '웹은 형태가 다양합니다. 두 Type에 맞지 않는 새 형태가 반복되면 템플릿 밖에서 짜지 않고 Template/Web에 Type을 추가해 값을 먼저 정합니다.']])
    content += ('<section class="section"><h2>템플릿</h2>' + tpl + '<p class="note">Figma <code>Template/Web</code> — Type=List(Content 슬롯) · Type=Work(List · Panel 슬롯), <code>Template/Mobile</code>(Background=Surface · Secondary, Content 슬롯 · Show App Bar · Show Navigation Bar). 앱 바 · 내비게이션 · LNB는 노출된 인스턴스라 템플릿 인스턴스에서 바로 제목 · 현재 탭을 바꿉니다. 흰 카드를 쌓는 모바일 목록 화면은 Background=Secondary(Gray 100). 템플릿에는 같은 이름의 그리드 스타일(<code>Layout/Web List</code> 등)이 걸려 있습니다.</p></section>'
        + '<section class="section"><h2>Web/List</h2><p>여백과 열 사이는 모두 40입니다. 화면이 넓어지면 카드 열과 오른쪽 패널의 너비는 그대로 두고, 둘 사이 간격이 늘어납니다.</p><div class="canvas" style="overflow-x:auto;display:flex;justify-content:center">' + LAY_LIST + '</div></section>'
        + '<section class="section"><h2>Web/Work</h2><p>LNB를 접고 목록을 좁게 붙여 작업 패널을 넓게 씁니다. 바깥 여백은 20(빨간 띠), 작업 패널은 화면 오른쪽 끝에 붙는 흰 시트이고 안쪽 좌우는 40(파란 띠)입니다.</p><div class="canvas" style="overflow-x:auto;display:flex;justify-content:center">' + LAY_WORK + '</div></section>'
        + '<section class="section"><h2>Mobile</h2><p>기준 기기는 375 × 812입니다. 본문 좌우 여백은 <a href="spacing.html">screen-x(20)</a>, 카드 · 목록 너비는 335입니다. 작성 흐름은 Navigation Bar 대신 Button Group을 둡니다.</p><div class="canvas canvas--center">' + LAY_MOB + '</div></section>'
        + '<section class="section"><h2>토큰</h2>' + table(['토큰', '값', 'Figma 변수', '쓰는 곳'], LAYOUT_ROWS) + '</section>'
        + '<section class="section"><h2>규칙</h2>' + rules + '</section>'
        + '<section class="section"><h2>코드</h2>' + code(LAYOUT_CODE) + '</section>')
    return content

LAYOUT_CODE = """<link rel="stylesheet" href="css/layout.css">

<!-- Web/List -->
<div class="layout-web-list">
  <nav class="lnb">…</nav>
  <main class="layout-web-list__body">
    <header>…</header>
    <div class="layout-web-list__row">
      <div class="layout-web-list__columns"><section>…</section><section>…</section></div>
      <aside class="layout-web-list__panel">…</aside>
    </div>
  </main>
</div>

<!-- Web/Work -->
<div class="layout-web-work">
  <nav class="lnb lnb--folded">…</nav>
  <section class="layout-web-work__list">…</section>
  <main class="layout-web-work__panel">…</main>
</div>"""

LAYOUT_ROWS = [['<button type="button" class="token" data-copy="var(--layout-mobile-width)">--layout-mobile-width</button>', '375px', '<code>layout/mobile-width</code>', '모바일 기준 화면 너비(375 × 812)'], ['<button type="button" class="token" data-copy="var(--layout-web-width)">--layout-web-width</button>', '1440px', '<code>layout/web-width</code>', '웹 기준 화면 너비(1440 × 900)'], ['<button type="button" class="token" data-copy="var(--layout-lnb)">--layout-lnb</button>', '284px', '<code>layout/lnb</code>', '펼친 LNB 너비 — Web/List'], ['<button type="button" class="token" data-copy="var(--layout-lnb-folded)">--layout-lnb-folded</button>', '84px', '<code>layout/lnb-folded</code>', '접은 LNB 너비 — Web/Work'], ['<button type="button" class="token" data-copy="var(--layout-card-column)">--layout-card-column</button>', '296px', '<code>layout/card-column</code>', '웹 카드 · 목록 열 너비'], ['<button type="button" class="token" data-copy="var(--layout-side-panel)">--layout-side-panel</button>', '306px', '<code>layout/side-panel</code>', 'Web/List 오른쪽 패널 너비(실행목표)'], ['<button type="button" class="token" data-copy="var(--layout-margin-list)">--layout-margin-list</button>', '40px (spacing/40)', '<code>layout/margin-list</code>', 'Web/List 본문 좌우 여백 · 열 사이'], ['<button type="button" class="token" data-copy="var(--layout-margin-work)">--layout-margin-work</button>', '20px (spacing/20)', '<code>layout/margin-work</code>', 'Web/Work 여백 · 목록과 작업 패널 사이'], ['<button type="button" class="token" data-copy="var(--layout-panel-padding)">--layout-panel-padding</button>', '40px (spacing/40)', '<code>layout/panel-padding</code>', 'Web/Work 작업 패널 안쪽 좌우']]

def p_spacing():
    bars = ''.join(f'<div class="spc-row"><span class="spc-bar" style="width:{v * 4}px"></span><span class="text-subtitle-16-semibold">Spacing {v}</span><span class="spc-val">{v}px · {k}</span></div>' for v, k, _ in SPACES)
    rows = [[f'Spacing {v}', f'{v}px', f'<button type="button" class="token" data-copy="var(--spacing-{v})">--spacing-{v}</button>', u] for v, _, u in SPACES]
    rows.append(['screen-x (역할)', '20px', '<button type="button" class="token" data-copy="var(--spacing-screen-x)">--spacing-screen-x</button>', '화면 좌우 여백. 버튼 묶음, 바텀시트, 탭, 목록 행처럼 화면 너비를 채우는 요소'])
    content = page_head('Foundations', 'Spacing', '간격은 4 · 8 · 12 · 16 · 20 · 24 여섯 단계와, 화면의 큰 덩어리 사이에만 쓰는 섹션 간격 32 · 40을 씁니다. 화면 좌우 여백은 20입니다.', status=('ok', '확정'))
    content += f'''<section class="section"><h2>단계</h2><div class="canvas spc-stage">{bars}</div></section>
<section class="section"><h2>토큰</h2>{table(['단계', '값', '토큰', '쓰는 곳'], rows)}</section>
<section class="section"><h2>고르는 기준</h2><p>가까운 관계일수록 좁게 둡니다. 한 덩어리 안(아이콘과 글자)은 4~8, 같은 종류가 나란히 놓이면 8, 묶음과 묶음 사이는 16~24입니다. 화면을 크게 나누는 덩어리 사이(질문 제목과 선택지, 상단 요약과 목록)에만 32 · 40을 씁니다.</p>
<p>버튼 위아래 13, 입력창 좌우 13처럼 단계에 없는 값은 높이(48 등)를 맞추려고 컴포넌트 안에서 생긴 값입니다. 화면을 만들 때 직접 쓰지 않습니다.</p></section>
<section class="section"><h2>코드</h2>{code("""<link rel="stylesheet" href="css/spacing.css">

padding: 0 var(--spacing-screen-x);   /* 화면 좌우 여백 */
gap: var(--spacing-8);""")}</section>
<section class="section"><h2>Figma 변수</h2><p>Figma의 <strong>Spacing</strong> 변수 모음에 spacing/4 ~ 24와 spacing/screen-x가 있습니다. 자동 배치의 간격과 안쪽 여백에서만 고를 수 있고, 컴포넌트에서 이 값을 쓰는 996곳이 연결되어 있습니다.</p></section>'''
    return content

ROW1 = ["Arrow-left", "Arrow-Right", "Close", "Chevron-Down", "Chevron-Up", "Chevron-Right", "Chevron-Left", "Drawer", "More", "Add", "Info", "More_hori", "Write", "Calendar", "Check", "Check_Filled", "Camera", "Camera_Filled"]
ROW2 = ["Expand", "Compress", "Unfold-Right", "Fold", "Unfold-Left", "Question", "Caution", "Caution_Filled", "Minus_Filled", "More_Filled", "Info_Filled"]
GRAPHIC = ["Team", "Person", "Planning", "Management", "Research", "Design", "Education", "Data", "Marketing", "Development", "Document", "List", "Recommend", "Regular", "Irregular"]
def p_iconography():
    assets = ''.join(f'<button type="button" class="ic" data-copy="{kebab(n)}.svg" data-copy-msg="{kebab(n)}.svg 복사했어요">{icon("Icon/Assets/" + n)}<span>{n.replace("_", " ")}</span></button>' for n in ROW1 + ROW2)
    pairs = ''.join(f'<div class="gp"><div class="gp-pair"><span class="gp-light">{gicon(f"Icon/Graphic/{n}|State=Color")}</span><span class="gp-dark">{gicon(f"Icon/Graphic/{n}|State=White")}</span></div><span>{n}</span></div>' for n in GRAPHIC)
    emo = ''.join(f'<div class="emo"><span>{gicon(f"Icon/Graphic/Emotion|Emotion={e}")}</span><span>{gicon(f"Icon/Graphic/Emotion|Emotion={e}_Disabled")}</span><small>{e}</small></div>' for e in ["Bad", "Soso", "Better", "Good", "Happy"])
    navs = ''.join(f'<div class="ic ic--static">{icon("Icon/Nav/" + n)}<span>{n}</span></div>' for n in ["Home", "ActionItem", "Analysis"])
    sizes = ''.join(f'<div class="size-demo"><span class="icon icon-{s}">{bare(mono(I["Icon/Assets/Calendar"]))}</span><code>.icon-{s}</code></div>' for s in ['24', '18', '16', '12'])
    content = page_head('Foundations', 'Iconography', '아이콘은 세 종류입니다. 화면 조작에 쓰는 단색 Assets, 메뉴 항목에 쓰는 여러 색의 Graphic, 하단 탭에 쓰는 Navigation입니다. 아이콘을 누르면 파일 이름이 복사됩니다.',
                        status=('ok', '확정'), node='1-3724')
    content += f'''<section class="section"><h2>크기</h2><p>Assets 아이콘은 24px로 그려져 있고, 24·18·16·12px로 줄여 씁니다. Graphic 아이콘은 28px이고, 좁은 줄에서는 24px로 줄여 씁니다.</p><div class="canvas size-row">{sizes}</div></section>
<section class="section"><h2>Assets <span class="count">29</span></h2><p>단색 아이콘은 <strong>글자색을 따라갑니다</strong>. 버튼 글자가 흰색이면 아이콘도 흰색이 됩니다.</p><div class="canvas"><div class="ic-grid">{assets}</div></div></section>
<section class="section"><h2>Graphic <span class="count">15 × 2</span></h2><p>메뉴와 분류에 쓰는 그림 아이콘입니다. 밝은 배경에는 Color, 어두운 배경에는 White를 씁니다. White는 연한 원(Gray 200, 40px) 안의 썸네일에도 씁니다(홈 스페이스 카드). 크기는 28이 기본이고, 카드 안 인원 수처럼 좁은 줄에서는 24로 줄여 씁니다. 색은 모두 <a href="color.html">Blue</a> 단계에서 나옵니다.</p><div class="canvas"><div class="gp-grid">{pairs}</div></div></section>
<section class="section"><h2>Emotion <span class="count">5 × 2</span></h2><p>회고의 기분을 다섯 단계로 표시합니다. 아래 줄은 선택되지 않은 상태입니다.</p><div class="canvas"><div class="emo-row">{emo}</div></div></section>
<section class="section"><h2>Navigation <span class="count">3</span></h2><p>하단 탭 전용입니다. 상태별 색은 <a href="navigation-bar.html">Navigation Bar</a>에서 정합니다.</p><div class="canvas"><div class="ic-grid">{navs}</div></div></section>
<section class="section"><h2>코드</h2>{code("""<!-- SVG를 넣고 크기 클래스를 붙입니다. 색은 color로 바꿉니다. -->
<span class="icon icon-18" style="color: var(--color-blue-600)">
  <svg viewBox="0 0 24 24">…</svg>
</span>""")}</section>
<section class="section"><h2>결정 기록</h2><div class="callouts">
  {callout('ok', '반영', '2026-10-26', '<strong>Calendar_Filled → Camera_Filled</strong> 실제 모양이 카메라라서 Figma 컴포넌트와 코드 파일 이름을 모두 바꿨습니다.')}
  {callout('ok', '확정', '2026-10-26', 'Emotion에서 Better(Blue 400)가 Good(Blue 500)보다 연한 것은 의도한 색입니다.')}
  {callout('wait', '확인 필요', '2026-10-26', 'Figma에서 Question, Camera, Camera_Filled만 순수 검정(#000)이고 나머지는 Gray 900입니다. 코드에서는 글자색을 따라가서 차이가 없지만, Figma에서는 미세하게 다릅니다.')}
</div></section>'''
    return content

def p_app_bar():
    spec = [['높이', '58px'], ['여백', '위 14 · 오른쪽 22 · 아래 8 · 왼쪽 20px'], ['아이콘', '24px, 간격 16px'], ['Home 제목', '<a href="typography.html">Heading 24 Bold</a>'], ['Sub 제목', '<a href="typography.html">Subtitle 18 SemiBold</a>, 가운데 정렬'], ['텍스트 버튼', 'Subtitle 16 SemiBold, Blue 600 · 누를 수 없을 때 Gray 400 (<a href="button.html">Button/Text Button</a> Type=Accent, State=Disabled)'], ['기준 너비', '375px']]
    content = page_head('Components', 'App Bar', '화면 맨 위에서 지금 어디에 있는지 알려주고, 뒤로 가기나 더보기 같은 동작을 둡니다. 탭 첫 화면에는 Home, 그 아래 화면에는 Sub를 씁니다.',
                        status=('ok', '확정'), node='1-3989')
    content += f'''<section class="section"><h2>Home</h2><p>탭의 첫 화면입니다. 왼쪽에 큰 제목, 오른쪽에 <a href="avatar.html">Avatar</a>를 둡니다.</p><div class="canvas canvas--center"><div class="phone-w">{app_bar_home()}</div></div></section>
<section class="section"><h2>Sub</h2><p>한 단계 들어간 화면입니다. 뒤로 가기, 가운데 제목, 오른쪽 동작으로 구성합니다. 동작 자리에는 아이콘 대신 텍스트 버튼을 둘 수 있습니다.</p>
<div class="canvas canvas--center"><div class="phone-w stack">{app_bar_sub()}{app_bar_sub("회고 작성", text_button=True)}{app_bar_sub("회고 작성", text_button=True, disabled=True, label="마치기")}</div></div><p class="canvas-caption">텍스트 버튼은 누를 수 없을 때 Disabled(Gray 400)로 둡니다. 예: 답을 쓰기 전의 "마치기". Figma에서는 Button/Text Button(Type=Accent)의 State로 바꿉니다.</p></section>
<section class="section"><h2>Inverse</h2><p>어두운 배경 위에서 씁니다. 글자와 아이콘이 모두 흰색이 됩니다.</p><div class="canvas canvas--center dark-canvas"><div class="phone-w">{app_bar_sub(inverse=True)}</div></div></section>
<section class="section"><h2>스펙</h2>{table(['항목', '값'], spec)}</section>
<section class="section"><h2>코드</h2>{code("""<header class="app-bar app-bar--sub">
  <div class="app-bar__contents">
    <div class="app-bar__side">
      <button class="app-bar__button" aria-label="뒤로">…</button>
    </div>
    <h1 class="app-bar__title text-subtitle-18-semibold">회고</h1>
    <div class="app-bar__side app-bar__side--end">…</div>
  </div>
</header>

<!-- 어두운 배경: app-bar--inverse 추가 -->""")}</section>
<section class="section"><h2>결정 기록</h2><div class="callouts">
  {callout('ok', '확정', '2026-10-26', 'Inverse에서 더보기 아이콘도 흰색으로 맞춥니다. Figma에서는 이 아이콘만 Gray 900이라 어두운 배경에 묻혀 보이지 않았습니다.')}
</div></section>'''
    return content

def p_nav():
    states = ''.join(f'<div class="state"><span class="state-label">{t}</span><div class="state-item">{nav_item("회고", "Icon/Nav/Home", s)}</div></div>' for t, s in [('Default', None), ('Hover', 'hover'), ('Pressed · 선택', 'pressed')])
    srow = [['Default', '<span class="dot" style="background:#CED2DA"></span>Gray 400', '<span class="dot" style="background:#8B909C"></span>Gray 600'],
            ['Hover', '<span class="dot" style="background:#8B909C"></span>Gray 600', '<span class="dot" style="background:#8B909C"></span>Gray 600'],
            ['Pressed · 선택', '<span class="dot" style="background:#212329"></span>Gray 900', '<span class="dot" style="background:#212329"></span>Gray 900']]
    spec = [['높이', '54px (+ iOS 홈 표시줄 영역 34px)'], ['여백', '위 6 · 좌우 4 · 아래 4px, 탭 간격 4px'], ['탭', '높이 44px, 아이콘 24px, 라벨 <a href="typography.html">Caption 11 Medium</a>'], ['위쪽 구분선', '1px, Opacity 4 (안쪽 선)'], ['배경', 'Gray 0']]
    bars = [('status-bar-ios18', 'iOS 18 상태 바 · 393 × 54'), ('safe-area-ios18', 'iOS 18 홈 표시줄 · 393 × 21'), ('status-bar-ios14', 'iOS 14 상태 바 · 375 × 44'), ('safe-area-ios14', 'iOS 14 홈 표시줄 · 375 × 34'), ('status-bar-android', 'Android 상태 바 · 360 × 40'), ('safe-area-android', 'Android 내비게이션 · 360 × 24')]
    osb = ''.join(f'<figure class="os"><div class="os-img{" os-img--android" if "status-bar-android" == n else ""}">{bare(asset(n))}</div><figcaption>{c}</figcaption></figure>' for n, c in bars)
    content = page_head('Components', 'Navigation Bar', '화면 맨 아래에서 회고, 실행 목표, 분석 세 탭을 오갑니다. 지금 있는 탭은 진한 색으로 표시합니다.',
                        status=('ok', '확정'), node='1-4016')
    content += f'''<section class="section"><h2>예시</h2><p>직접 눌러 보세요. 마우스를 올리면 호버, 누르면 선택 상태로 바뀝니다.</p><div class="canvas canvas--center"><div class="phone-w">{nav_bar('Home', safe=True, interactive=True)}</div></div></section>
<section class="section"><h2>선택된 탭</h2><div class="canvas canvas--center"><div class="phone-w stack stack--loose">{nav_bar('Home', safe=False)}{nav_bar('Action Item', safe=False)}{nav_bar('Analysis', safe=False)}</div></div></section>
<section class="section"><h2>탭 상태</h2><div class="canvas"><div class="states">{states}</div></div>{table(['상태', '아이콘', '라벨'], srow)}</section>
<section class="section"><h2>스펙</h2>{table(['항목', '값'], spec)}</section>
<section class="section"><h2>시스템 영역</h2><p>상태 바와 홈 표시줄은 iOS·Android가 그리는 영역입니다. 화면을 그릴 때 자리만 비워 두고, 우리 컴포넌트로 만들지 않습니다.</p><div class="canvas"><div class="os-grid">{osb}</div></div>{callout('ok', '확정', '2026-10-29', 'OS Bar 안의 시스템 부품(Time · Home Indicator 등)은 iOS·Android 키트에서 가져온 원격 인스턴스를 그대로 씁니다. 우리가 정하는 디자인이 아니고 개발에서 구현하지도 않으므로 로컬로 바꾸거나 토큰에 연결하지 않으며, 화면 점검의 원격 인스턴스 0개 기준에서 예외입니다. OS 모양이 바뀌면 키트만 바꿔 끼웁니다.')}</section>
<section class="section"><h2>코드</h2>{code("""<nav class="nav-bar" aria-label="주요 메뉴">
  <ul class="nav-bar__items">
    <li><a class="nav-item" href="/home" aria-current="page">
      <span class="nav-item__icon"><span class="icon icon-24">…</span></span>
      <span class="nav-item__label text-caption-11-medium">회고</span>
    </a></li>
    …
  </ul>
</nav>""")}<p class="note">선택된 탭은 <code>aria-current="page"</code>로 표시합니다. 화면 읽기 프로그램도 같은 정보를 읽습니다.</p></section>
<section class="section"><h2>열린 질문</h2><div class="callouts">
  {callout('wait', '확인 필요', '2026-10-26', '앱바와 내비게이션은 375px 기준인데 iOS 18 상태 바는 393px입니다. 화면을 그릴 기준 기기를 정하면 이후 화면 분석이 쉬워집니다.')}
</div></section>'''
    return content

def p_avatar():
    content = page_head('Components', 'Avatar', '사용자를 나타내는 작은 원입니다. 프로필 사진이 있으면 사진을, 없으면 사용자 아이콘을 보여줍니다.',
                        status=('ok', '확정'), node='1-3978')
    content += f'''<section class="section"><h2>종류</h2><div class="canvas"><div class="av-row"><div class="av">{avatar("icon")}<span>사용자 아이콘<small>사진이 없을 때</small></span></div><div class="av">{avatar("icon", 42)}<span>Size 42<small>설정 화면 프로필 행</small></span></div><div class="av">{avatar("icon", 28)}<span>Size 28<small>웹 LNB 아래 프로필</small></span></div><div class="av">{avatar("image")}<span>프로필 사진<small>사진이 있을 때</small></span></div></div></div><p class="canvas-caption">예시 사진은 Figma 원본의 견본 이미지입니다.</p></section>
<section class="section"><h2>스펙</h2>{table(['항목', '값'], [['크기', '32 × 32px(앱 바 Home) · 42 × 42px(설정 화면 프로필 행) · 28 × 28px(웹 LNB 아래 프로필 — 펼침 · 접힘 모두), 원형'], ['사진이 없을 때', 'Gray 400 배경 + 흰색 사용자 모양'], ['사진', '원 안을 꽉 채우도록 자름'], ['쓰는 곳', '<a href="app-bar.html">App Bar</a> Home 오른쪽 · 웹 <a href="popover.html">팀원 목록</a>'], ['Show Leader', '대표자 표시. 오른쪽 아래 왕관(Gray 900 동그라미 + 흰 왕관), 크기의 37.5%(32 → 12)']])}</section>
<section class="section"><h2>대표자 표시</h2><p>스페이스 대표자에게만 왕관을 붙입니다. Figma에서는 Profile의 Show Leader를 켭니다.</p><div class="canvas"><div class="av-row"><div class="av"><span class="avatar-leader">{avatar('icon')}<span class="avatar-leader__badge"><svg viewBox="0 0 12 12" aria-hidden="true"><circle cx="6" cy="6" r="6" fill="currentColor"/><path d="M3.2 4.3 4.6 5.6 6 3.6l1.4 2 1.4-1.3-.5 3.4H3.7z" fill="#fff"/></svg></span></span><span>Show Leader<small>대표자</small></span></div><div class="av">{avatar('icon')}<span>기본<small>팀원</small></span></div></div></div></section>
<section class="section"><h2>코드</h2>{code("""<!-- 사진이 있을 때 -->
<span class="avatar"><img src="profile.jpg" alt="김레이어 프로필"></span>

<!-- 사진이 없을 때 -->
<span class="avatar" role="img" aria-label="프로필">
  <svg viewBox="0 0 32 32">…</svg>
</span>""")}</section>'''
    return content

def p_empty():
    content = page_head('Components', 'Empty State', '보여 줄 내용이 아직 없을 때 빈 칸 대신 두는 안내입니다. 무엇이 없는지와 어떻게 채우는지를 1~2줄로 알려 줍니다.', status=('ok', '확정'), node='359-85139')
    goal = '<svg class="empty-state__icon" viewBox="0 0 56 56" fill="none" aria-hidden="true"><circle cx="28" cy="32" r="18" fill="#EDF0F4" stroke="#CED2DA" stroke-width="2"/><circle cx="28" cy="9" r="3" stroke="#CED2DA" stroke-width="2"/><path d="M28 24v8" stroke="#A9AFBB" stroke-width="2" stroke-linecap="round"/><circle cx="28" cy="38" r="1.5" fill="#A9AFBB"/></svg>'
    ex1 = '<div class="empty-state"><p>진행 중인 회고가 없어요</p></div>'
    ex3 = '<div class="empty-state empty-state--dashed"><p>아직 작성된 회고가 없어요<br>회고를 작성하면 분석 결과를 확인할 수 있어요</p></div>'
    ex2 = f'<div class="empty-state">{goal}<p>진행 중인 실행 목표가 없어요<br>회고를 작성하고 행동으로 연결해보세요</p></div>'
    spec = table(['항목', '값'], [['테두리', 'Border=None: 없음(흰 섹션 카드가 틀). Border=Dashed: 점선 1px(Opacity 12, 4/4) — 카드 안에 다른 내용과 함께 있어 빈 영역을 구분할 때'], ['박스', '모서리 12(<code>--radius-card</code>), 위아래 32 · 좌우 20, 부모 카드 너비를 채움'], ['문구', '<a href="typography.html">Body 15 Medium</a> Gray 500, 가운데 정렬, 1~2줄(무엇이 없는지 + 어떻게 채우는지)'], ['아이콘', '56px, 문구와 간격 12. Show Icon으로 켜고 끔'], ['Figma', '<code>Empty State</code> · 속성 Border(None · Dashed) · Message · Show Icon · Icon(Empty State/Icon/*)']])
    content += (f'<section class="section"><h2>예시</h2><div class="canvas"><div class="es-demo"><span class="state-label">Border = None · 흰 카드가 이미 틀일 때 (기본)</span>{ex1}{ex2}<span class="state-label">Border = Dashed · 카드 안에서 다른 내용과 함께 있을 때</span>{ex3}</div></div><p class="canvas-caption">웹 홈 대시보드의 빈 상태. 분석 카드는 위에 감정 항목이 함께 있어서 빈 영역을 점선으로 구분합니다.</p></section>'
                f'<section class="section"><h2>스펙</h2>{spec}</section>'
                f'<section class="section"><h2>코드</h2>{code(ex2.replace(goal, "<svg class=\"empty-state__icon\">…</svg>"))}</section>')
    return content

def goal_section():
    def gc(badge, mobile=False, items=True, empty=False, title='스프린트 1회차 이후 회고'):
        acts = f'<span class="goal-card__actions">{icon("Icon/Assets/Add", "icon")}{icon("Icon/Assets/More", "icon")}</span>'
        lst = '<ul class="goal-card__list"><li>긴 회의시간 줄이기</li><li>회의 후 내용 꼭 기록해두기</li><li>‘린 분석’ 북 스터디 진행</li></ul>' if items else ''
        goal = '<svg class="empty-state__icon" viewBox="0 0 56 56" fill="none" aria-hidden="true"><circle cx="28" cy="32" r="18" fill="#EDF0F4" stroke="#CED2DA" stroke-width="2"/><circle cx="28" cy="9" r="3" stroke="#CED2DA" stroke-width="2"/><path d="M28 24v8" stroke="#A9AFBB" stroke-width="2" stroke-linecap="round"/><circle cx="28" cy="38" r="1.5" fill="#A9AFBB"/></svg>'
        emp = f'<div class="empty-state">{goal}<p>실행목표가 없어요</p></div>' if empty else ''
        cls = 'goal-card goal-card--mobile' if mobile else 'goal-card'
        if badge:
            return f'<div class="{cls}"><div class="goal-card__head"><span class="badge badge--outlined badge--outlined-blue">실행 중</span>{acts}</div><div class="goal-card__body"><p class="goal-card__title">{title}</p>{lst}</div>{emp}</div>'
        return f'<div class="{cls}"><div class="goal-card__head"><p class="goal-card__title">{title}</p>{acts}</div>' + (f'<div class="goal-card__body">{lst}</div>' if items else '') + f'{emp}</div>'
    return (f'<section class="section"><h2>Card/Goal (Web)</h2><p>웹 회고 스페이스 오른쪽 실행목표 패널에 회고별로 쌓는 목표 묶음입니다. 상태가 있으면 Badge=On, 없으면 Off로 제목을 아이콘과 한 줄에 둡니다.</p>'
            f'<div class="canvas canvas--sunk canvas--center"><div class="cd-goal">{gc(True)}{gc(False)}</div></div>'
            + table(['항목', '값'], [['너비', '270 (패널 306, 안쪽 18)'], ['머리', '<a href="badge.html">Badge Outlined Blue</a>(실행 중) + Add · More 18, 왼쪽 4'], ['제목', '<a href="typography.html">Title 15 Bold</a> Gray 900'], ['목표 줄', '높이 36(위아래 12), 점 Gray 400 5px + Body 14 Medium Gray 900, 3줄까지. 목표가 없으면 Show Items를 끔'], ['묶음 사이', '간격 20 + 구분선 Gray 100 1px'], ['Figma', '<code>Card/Goal (Web)</code> · Badge=On · Off, Title, Item 1~3, Show Item 2 · 3, Show Items']]) + '</section>'
            + f'<section class="section"><h2>Card/Goal (Mobile)</h2><p>모바일 실행목표 화면에 회고별로 쌓는 흰 카드입니다. 구조와 속성은 웹과 같고, 카드 틀과 글자 크기만 다릅니다. 목표가 아직 없으면 빈 상태를, 접어 둔 회고는 제목만 보여 줍니다.</p>'
            f'<div class="canvas canvas--sunk canvas--center"><div class="cd-stack" style="width:335px">{gc(True, True)}{gc(True, True, items=False, empty=True, title="중간발표 이후 회고")}{gc(False, True, items=False, title="스프린트 2회차 이후 회고")}</div></div>'
            + table(['항목', '값'], [['틀', '335, 흰 바탕, 모서리 12, <a href="elevation.html">Shadow 100</a>, 안쪽 위 20 · 좌우 20 · 아래 16, 카드 사이 12'], ['머리', 'Badge Outlined Blue 22(실행 중, 웹과 같음) + Add · More 24(세로 점)'], ['제목', '<a href="typography.html">Title 18 Bold</a> Gray 900'], ['목표 줄', '높이 46(위아래 12), 점 Gray 400 6px + <a href="typography.html">Body 16 Medium</a> Gray 900, 3줄까지'], ['빈 상태', 'Show Items 끄고 Show Empty 켬 → <a href="empty-state.html">Empty State</a>(Border=None) "실행목표가 없어요"'], ['Figma', '<code>Card/Goal (Mobile)</code> · Badge=On · Off, Title, Item 1~3, Show Item 2 · 3, Show Items, Show Empty']]) + '</section>')

def answer_section():
    def bdg(t): return f'<span class="badge badge--gray badge--25">{t}</span>'
    txt = '가장 어려운 점은 일정관리를 하는 것이다. 나만의 일정을 관리한다면 상관없지만, 셀 내 모든 인원들의 일정을 고려하며 관리를 하는 것이 처음에는 많이 어려운 점 중 하나였다.'
    E = ['Bad', 'Soso', 'Better', 'Good', 'Happy']
    emo = lambda sel='Good': '<div class="emotion-scale">' + ''.join(bare(G[f'Icon/Graphic/Emotion|Emotion={e}' + ('' if e == sel else '_Disabled')]) for e in E) + '</div>'
    score = lambda v=80: '<div class="score-bar"><div class="score-bar__labels">' + ''.join(f'<span{" class=\"is-current\"" if n == v else ""}>{n}</span>' for n in range(0, 101, 20)) + '</div><div class="score-bar__track">' + ''.join(f'<span{" class=\"is-on\"" if i < v // 20 else ""}></span>' for i in range(5)) + '</div></div>'
    card = lambda body, web=False, name='김레이어': f'<div class="answer-card{" answer-card--web" if web else ""}">' + (bdg(name) if name else '') + body + '</div>'
    t = f'<p class="answer-card__text">{txt}</p>'
    qg = lambda q, inner: f'<div class="question-group" style="width:340px"><p class="question-group__title">{q}</p><div class="question-group__content">{inner}</div></div>'
    return (f'<section class="section"><h2>Card/Answer</h2><p>팀원의 답을 보여 주는 카드입니다. Platform으로 모바일 · 웹을, Type으로 답의 종류(글 · 만족도 · 점수)를 고릅니다. 내 답을 다시 볼 때는 이름표를 끕니다(Show Name).</p>'
            f'<div class="canvas canvas--sunk canvas--center"><div class="cd-stack" style="width:335px"><span class="state-label">Mobile · Text</span>{card(t)}<span class="state-label">Mobile · Emotion</span>{card(emo())}<span class="state-label">Mobile · Score</span>{card(score())}</div></div>'
            + table(['항목', '값'], [['Platform=Mobile', '너비 335, 위 16 · 좌우 16 · 아래 20, 흰 바탕, 모서리 12, <a href="elevation.html">Shadow 100</a>'], ['Platform=Web', '너비 308(열에 맞춤), 위 12 · 좌우 12 · 아래 18, 흰 바탕, 모서리 8, 그림자 없음 — 질문 묶음(회색) 위에 놓임'], ['이름표', '<a href="badge.html">Badge</a> Gray 25 · Show Name'], ['Type=Text', '<a href="typography.html">Body 15 Medium Long</a>(행간 180%) Gray 800'], ['Type=Emotion', 'Answer/Emotion Scale — 얼굴 36 다섯 개(사이 8), 고른 얼굴만 색, 나머지는 회색(_Disabled)'], ['Type=Score', 'Answer/Score Bar — 0~100 20 단위 5칸, 높이 16 · 모서리 8, 채운 칸 Blue 600 · 빈 칸 Gray 200, 고른 눈금 Caption 11 SemiBold 파랑'], ['Figma', '<code>Card/Answer</code> · Platform · Type · Answer · Show Name / <code>Answer/Emotion Scale</code> · Value / <code>Answer/Score Bar</code> · Value']]) + '</section>'
            + f'<section class="section"><h2>Card/Question Group (Web)</h2><p>웹에서 질문 하나와 그 답들을 묶는 회색 카드입니다. 회고 확인의 질문별 보기에서는 열마다 팀원 답을 쌓고, 제출 전 확인에서는 이름표 없이 내 답 하나를 넣습니다.</p>'
            f'<div class="canvas"><div style="display:flex;flex-wrap:wrap;gap:16px;justify-content:center;align-items:flex-start">{qg("진행상황에 대해 얼마나 만족하나요?", card(emo(), True) + card(emo("Better"), True, "박회고"))}{qg("1. 계속 유지하고 싶은 것은 무엇인가요?", card(t, True, ""))}</div></div>'
            + table(['항목', '값'], [['틀', 'Gray 100, 모서리 12, 안쪽 16, 사이 16, 너비는 열 · 본문에 맞춤'], ['질문', '<a href="typography.html">Title 15 Bold</a> Gray 900'], ['내용', 'Content <strong>슬롯</strong> — Card/Answer(Platform=Web), 사이 12'], ['Figma', '<code>Card/Question Group (Web)</code> · Question · Content(슬롯)']]) + '</section>')

def template_section():
    def bd(t, big=False): return f'<span class="badge badge--gray{" badge--25" if big else ""}">{t}</span>'
    more = icon('Icon/Assets/More', 'icon')
    art = lambda f, cls: f'<img class="{cls}" src="img/illustrations/retro-{f}.svg" alt="">'
    def dflt(t, b, f, mobile=False, btn=False):
        return (f'<div class="template-card{" template-card--mobile" if mobile else ""}"><div class="template-card__row"><div class="template-card__text"><p class="template-card__title">{t}</p>{bd(b, mobile)}</div>{art(f, "template-card__art")}</div>'
                + ('<button type="button" class="btn btn--outlined btn--sm" style="width:100%">선택하기</button>' if btn else '') + '</div>')
    def cust(mobile=False):
        return (f'<div class="template-card template-card--custom{" template-card--mobile" if mobile else ""}"><div class="template-card__top"><p class="template-card__title">커스텀 템플릿</p>{more}</div><div class="template-card__meta">{bd("KPT", mobile)}<span class="template-card__date">2024. 07. 12</span></div></div>')
    det = lambda small=False: (f'<div class="template-detail{" template-detail--240" if small else ""}"><div class="template-detail__head"><p class="template-detail__title">차근차근, 단계적인 회고</p>{bd("KPT", not small)}</div>{art("kpt", "template-detail__art")}<button type="button" class="btn btn--ghost{" btn--sm" if small else ""}" style="width:100%">{"회고 방식 알아보기" if small else "더 알아보기"}</button></div>')
    qs = ''.join(f'<li class="list-card"><span class="num-badge">{i + 1}</span><span class="list-card__text">{q}</span></li>' for i, q in enumerate(['어려움을 느꼈던 부분은 무엇인가요?', '잘했다고 생각하는 부분은 무엇인가요?', '계속 유지하고 싶은 것은 무엇인가요?']))
    summ = f'<div class="template-summary"><div class="template-summary__head"><div><p class="template-summary__title">차근차근, 단계적인 회고</p>{bd("KPT", True)}</div><button type="button" class="btn btn--outlined btn--sm">{icon("Icon/Assets/Write", "icon")}질문 수정</button></div><ol class="list list--cards">{qs}</ol></div>'
    row = lambda inner: f'<div style="display:flex;flex-wrap:wrap;gap:16px;justify-content:center;align-items:flex-start">{inner}</div>'
    return (f'<section class="section"><h2>Card/Template</h2><p>회고 템플릿 카드입니다. 기본 템플릿(Type=Default)은 그림이 있고, 내가 만든 템플릿(Type=Custom)은 만든 날짜가 있습니다. 템플릿을 고르는 단계에서는 Show Button으로 "선택하기"를 켭니다.</p>'
            f'<div class="canvas canvas--sunk">' + row(dflt('차근차근,<br>단계적인 회고', 'KPT', 'kpt') + dflt('감정 통찰을<br>위한 회고', 'MAD SAD GLAD', 'mad-sad-glad') + dflt('내가 직접<br>만드는 회고', '무제', 'untitled', btn=True) + cust()) + '</div>'
            f'<div class="canvas canvas--sunk" style="margin-top:12px">' + row(dflt('차근차근, 단계적인 회고', 'KPT', 'kpt', True) + cust(True)) + '</div>'
            + table(['항목', '값'], [['Platform=Web', '230, 흰 바탕, 테두리 Gray 100, 모서리 8, 안쪽 16 — 템플릿 리스트 모달 2열(사이 16)'], ['Platform=Mobile', '335, 흰 바탕, <a href="elevation.html">Shadow 100</a>, 모서리 12, 안쪽 20'], ['Type=Default', '제목 <a href="typography.html">Title 14 Bold</a>(Mobile 16) Gray 800 2줄 · <a href="badge.html">Badge</a> Gray 22(Mobile 25) · 오른쪽 아래 <a href="illustration.html">Retro 일러스트</a> 86(Mobile 100) · Show Button: <a href="button.html">Outlined 40</a> "선택하기"'], ['Type=Custom', '제목 + More / 배지 + 만든 날짜 Body 12 Medium Gray 500(Mobile 14)'], ['Figma', '<code>Card/Template</code> · Type · Platform · Title · Date · Show Button · Illustration']]) + '</section>'
            + f'<section class="section"><h2>Card/Template Detail</h2><p>회고를 만들 때 템플릿을 넘겨 보며 소개하는 정사각형 카드입니다. 크기는 335와, 옆 카드가 살짝 보이게 넘길 때 쓰는 240 두 가지입니다.</p>'
            f'<div class="canvas canvas--sunk">' + row(det() + det(True)) + '</div>'
            + table(['Size', '값'], [['335', '안쪽 24, 제목 Title 20 Bold, Badge 25, 그림 160, <a href="button.html">Ghost 48</a> "더 알아보기"'], ['240', '안쪽 20, 제목 Title 14 Bold, Badge 22, 그림 115, Ghost 40 "회고 방식 알아보기"'], ['Figma', '<code>Card/Template Detail</code> · Size · Title · Illustration']]) + '</section>'
            + f'<section class="section"><h2>Card/Template Summary</h2><p>고른 템플릿의 질문을 확인하는 요약 카드입니다(웹 회고 생성). 질문 줄은 <a href="lists.html">아이콘 리스트</a> Action=None · Marker=Number입니다.</p>'
            f'<div class="canvas">' + row(summ) + '</div>'
            + table(['항목', '값'], [['틀', '472, 흰 바탕, 테두리 Gray 300, 모서리 12, 안쪽 20, 사이 24'], ['머리', '제목 Title 20 Bold + Badge Gray 25, 오른쪽 <a href="button.html">Outlined 40</a> + Write 아이콘 "질문 수정"'], ['질문', 'Questions <strong>슬롯</strong> — List/Icon List None · Number, 사이 8'], ['Figma', '<code>Card/Template Summary</code> · Title · Questions(슬롯)']]) + '</section>')

def p_cards():
    def bdg(t, c): return f'<span class="badge {c}">{t}</span>'
    person = bare(G['Icon/Graphic/Person|State=Color'])
    space = lambda title, desc, badge=True: (f'<div class="space-card"><span class="space-card__thumb">{bare(G["Icon/Graphic/Development|State=Color"])}</span><div class="space-card__body"><div class="space-card__head"><div class="space-card__row"><strong class="space-card__title">{title}</strong>'
                                             + (bdg('진행 중 1', 'badge--blue') if badge else '') + '</div>' + (f'<p class="space-card__desc">{desc}</p>' if desc else '') + '</div><p class="space-card__meta">멤버 11명 · 회고 4개</p></div></div>')
    retro = lambda btn, closed=False, badge=('D-15', 'badge--white'): (f'<div class="retro-card{" retro-card--closed" if closed else ""}"><div class="retro-card__top"><div class="retro-card__body"><p class="retro-card__title">중간발표 이후 회고</p><p class="retro-card__desc">방향성 체크 및 팀 내 개선점 구축</p>'
                         + (f'<span class="retro-card__date">2024. 07. 12 ~ 2024. 07. 28</span></div><div class="retro-card__side">' if closed else f'<span class="retro-card__date">{icon("Icon/Assets/Calendar", "icon")}2024. 07. 30 오전 10:00</span></div><div class="retro-card__side">{bdg(*badge)}') + f'{icon("Icon/Assets/More", "icon")}</div></div>'
                         f'<div class="retro-card__bottom"><span class="retro-card__count">{person}<b>{"10" if closed else "1"}</b>/ 10</span><button type="button" class="btn {"btn--primary" if closed else "btn--blue"} btn--sm">{btn}</button></div></div>')
    answer = (f'<div class="answer-card">{bdg("김레이어", "badge--gray badge--25")}<p class="answer-card__text">가장 어려운 점은 일정관리를 하는 것이다. 나만의 일정을 관리한다면 상관없지만, 셀 내 모든 인원들의 일정을 고려하며 관리를 하는 것이 처음에는 많이 어려운 점 중 하나였다.</p></div>')
    def web(status, cls, deadline, count, closed=False, sel=False, desc=True):
        cc = 'retro-card-web__count--closed' if closed else ('retro-card-web__count--zero' if count.startswith('0') else 'retro-card-web__count--active')
        cur, tot = count.split(' / '); count = f'<b>{cur}</b> / {tot}'
        return (f'<div class="retro-card-web{" retro-card-web--selected" if sel else ""}"><div class="retro-card-web__head">{bdg(status, cls if cls == "badge--blue" else "badge--outlined " + cls)}{icon("Icon/Assets/More", "icon")}</div>'
                f'<p class="retro-card-web__title">중간발표 이후 회고</p>' + ('<p class="retro-card-web__desc">방향성 체크 및 팀 내 개선점 구축</p>' if desc else '')
                + f'<div class="retro-card-web__foot"><span>{deadline}</span><span class="retro-card-web__count {cc}">{person}{count}</span></div></div>')
    content = page_head('Components', 'Cards', '회고 서비스에서 반복되는 카드 다섯 가지입니다. 화면에서 카드를 직접 그리지 않고 Figma의 Card/ 컴포넌트를 씁니다.', status=('ok', '확정'), node='365-4431')
    content += (f'<section class="section"><h2>Card/Space</h2><p>모바일 홈의 회고 스페이스 카드입니다. 제목은 한 줄로 말줄임하고, 설명이 없으면 Show Description을 꺼서 높이 79가 됩니다.</p>'
                f'<div class="canvas canvas--sunk canvas--center"><div class="cd-stack">{space("떡잎마을방범대", "IT 연합동아리 디프만 15기의 프로젝트 방향성 체크 및 팀 내 개선점 구축")}{space("떡잎마을방범대대대대대대대대대대대대대", "", False)}</div></div>'
                + table(['항목', '값'], [['크기', '335 × 103 (설명 없으면 79), 안쪽 16, 아이콘과 글 사이 16'], ['아이콘', 'Gray 200 원 40 안에 그래픽 아이콘 28 (Icon으로 바꿈)'], ['글자', '제목 <a href="typography.html">Title 16 Bold</a> 한 줄 · 설명 Body 13 Medium Gray 600 한 줄 · 아래 Body 12 Medium Gray 600'], ['Figma', '<code>Card/Space</code> · Title · Description · Meta · Show Description · Show Badge · Icon']]) + '</section>'
                f'<section class="section"><h2>Card/Retro (Mobile)</h2><p>모바일 회고 카드입니다. 진행 중인 회고는 Status=Open(스페이스 화면), 마감된 회고는 Status=Closed(회고 관리)를 씁니다. 버튼 이름은 상황에 맞게(회고 작성 · 회고 확인 · 분석 확인) 바꿉니다.</p>'
                f'<div class="canvas canvas--center"><div class="cd-stack"><span class="state-label">Open · Progress = Before(작성 전) — D-day</span>{retro("회고 작성")}<span class="state-label">Open · Progress = Writing — 작성 중</span>{retro("회고 작성", badge=("작성 중", "badge--outlined badge--outlined-blue"))}<span class="state-label">Open · Progress = Submitted — 제출 완료</span>{retro("회고 확인", badge=("제출 완료", "badge--outlined badge--outlined-green"))}<span class="state-label">Status = Closed</span>{retro("분석 확인", True)}</div></div>'
                + table(['항목', '값'], [['크기', '335 × 160(설명 없으면 136, Show Description), 안쪽 20, 모서리 12'], ['Status', 'Open: 바탕 Blue 50 · D-day 배지 · 마감일(Calendar 16) · 버튼 40 Blue. Closed: 바탕 Gray 100 · D-day 없음 · 기간 "시작 ~ 마감"(아이콘 없음) · 인원 모두 Gray 500 · 버튼 40 Primary'], ['글자', '제목 Title 16 Bold · 설명 Body 14 Medium Gray 800 · 날짜 Body 14 Medium Gray 500'], ['오른쪽 위', '배지 한 자리 + More 24. 배지는 D-day <em>또는</em> 내 상태 하나만 — Progress=Before(작성 전): <a href="badge.html">Badge</a> White D-day · Writing: Badge Outlined Blue 작성 중 · Submitted: Badge Outlined Green 제출 완료. 마감(Closed)은 배지 없음'], ['버튼 문구', '작성 전 · 작성 중 "회고 작성" · 제출 완료 "회고 확인" · 마감 "분석 확인"'], ['아래', '인원 수 Body 16 Medium(Person 24): 제출 인원 Blue 600 + "/ 10" Gray 500, 모두 제출하면 둘 다 Gray 500. 오른쪽 <a href="button.html">Button 40 Blue</a>'], ['Figma', '<code>Card/Retro (Mobile)</code> · Status(Open · Closed) · Progress(Before · Writing · Submitted) · Title · Description · Show Description · Deadline · Period(Closed) · Show Deadline · Count(제출 인원) · Total("/ 10") · Show Button']]) + '</section>'
                + answer_section() + template_section() +
                f'<section class="section"><h2>Card/Retro (Web)</h2><p>웹 회고 스페이스에서 열마다 세로로 쌓는 회고 카드입니다. 왼쪽 위 배지 한 자리에 D-day 또는 진행 상태를 보여 주고, 마감 방식은 Deadline으로 고릅니다.</p>'
                f'<div class="canvas canvas--sunk"><div class="cd-grid">{web("D-4", "badge--blue", "마감 예정<i>|</i>2024.07.30 10:00", "0 / 10", sel=True)}{web("작성 전", "badge--outlined-gray", "모든 인원 제출 시 마감", "0 / 10", desc=False)}{web("작성 중", "badge--outlined-blue", "모든 인원 제출 시 마감", "1 / 10")}{web("제출 완료", "badge--outlined-green", "모든 인원 제출 시 마감", "8 / 10")}{web("분석 완료", "badge--outlined-dark", "마감일<i>|</i>2024.07.30 10:00", "10 / 10", True)}</div></div>'
                + table(['항목', '값'], [['크기', '296 × 138, 안쪽 18, 흰 바탕, 모서리 12, 카드 사이 12'], ['배지', '한 자리에 D-day <em>또는</em> 상태 하나만 — 작성 전 + 마감일 있음(Before · Set): Badge Blue D-day · 작성 전 + 마감일 없음: 작성 전(Gray) · 작성 중(Blue) · 제출 완료(Green) · 분석 완료(Dark)'], ['Status', 'Before 작성 전 · Writing 작성 중 · Submitted 제출 완료 · Analyzed 분석 완료'], ['Deadline', 'Set 마감 예정 날짜 · Unset 모든 인원 제출 시 마감 · Closed 마감일(마감된 회고 열)'], ['글자', '제목 <a href="typography.html">Title 15 Bold</a> · 설명 Body 12 Medium Gray 800 · 아래 Body 12 Medium Gray 500, 인원 수 Body 12 SemiBold — 제출 인원은 작성 중 · 제출 완료 Blue 600 · 마감 Gray 700 · 0명 Gray 500, "/ 10"은 Gray 500'], ['Selected', 'On: 지금 열어 둔(작성 중인) 회고 — 테두리 Blue 400 1px + <a href="elevation.html">Shadow 100</a>. 한 열에 하나만 (예시 첫 카드)'], ['설명', 'Show Description — 설명이 없으면 끔(예시 둘째 카드)'], ['Figma', '<code>Card/Retro (Web)</code> · Status × Deadline × Selected · Show Description · 배지 Label(D-day)']]) + '</section>'
                + goal_section()
                + f'<section class="section"><h2>코드</h2>{code("<link rel=\"stylesheet\" href=\"css/cards.css\">" + chr(10) + "<div class=\"space-card\">…</div>" + chr(10) + "<div class=\"retro-card\">…</div>" + chr(10) + "<div class=\"answer-card\">…</div>" + chr(10) + "<div class=\"retro-card-web\">…</div>")}</section>')
    return content

def p_dropdown():
    tmpl = bare(G['Icon/Graphic/Document|State=Color']); team = bare(G['Icon/Graphic/Team|State=Color'])
    chev = icon('Icon/Assets/Chevron-Down', 'dropdown__chevron')
    dd = lambda label, ic, st='': f'<button type="button" class="dropdown{st}">' + (f'<span class="dropdown__icon">{ic}</span>' if ic else '') + f'{label}{chev}</button>'
    content = page_head('Components', 'Dropdown', '웹 화면 위쪽에서 보기를 바꾸거나 걸러 볼 때 쓰는 버튼입니다. 누르면 목록이 열립니다.', status=('ok', '확정'), node='363-30483')
    content += (f'<section class="section"><h2>예시</h2><div class="canvas canvas--sunk canvas--center"><div class="bd-row"><button type="button" class="btn btn--blue btn--xs">{icon("Icon/Assets/Add", "icon")}회고 추가하기</button>{dd("KPT", tmpl)}{dd("11", team)}</div></div><p class="canvas-caption">웹 회고 스페이스 머리: 주요 행동 Button 36 Blue 옆에 대표 템플릿 · 팀원 드롭다운.</p>'
                f'<h3 class="tk-h3">State</h3><div class="canvas canvas--sunk bd-colors"><div class="bd-swatch"><span class="state-label">Default · 흰 바탕</span>{dd("KPT", tmpl)}</div><div class="bd-swatch"><span class="state-label">Hover · Gray 100</span>{dd("KPT", tmpl, " is-hover")}</div><div class="bd-swatch"><span class="state-label">Pressed · Gray 200</span>{dd("KPT", tmpl, " is-pressed")}</div></div></section>'
                + '<section class="section"><h2>스펙</h2>' + table(['항목', '값'], [['크기', '높이 36(웹 버튼 36과 같은 줄), 좌 12 · 우 16(Chevron 쪽 여백을 넓혀 시각 균형), 사이 6, 모서리 8(<code>--radius-button-xs</code>), 너비는 내용에 맞춤'], ['글자', '<a href="typography.html">Subtitle 14 SemiBold</a> Gray 600'], ['아이콘', '앞 그래픽 아이콘 20(Show Icon으로 켜고 끔) · 뒤 Chevron-Down 14'], ['Figma', '<code>Dropdown</code> · Label · Show Icon · Icon · State=Default · Hover · Pressed']]) + '</section>'
                + '<section class="section"><h2>쓰는 법</h2>' + table(['상황', '쓸 것'], [['웹 화면 위에서 보기 · 필터를 하나 고를 때', 'Dropdown'], ['여러 개를 골라 걸러 볼 때', '<a href="chip-button.html">Chip Button</a>'], ['입력 양식 안에서 값을 고를 때', '<a href="fields.html">Fields/Select Field</a>']]) + '</section>'
                f'<section class="section"><h2>코드</h2>{code("<button type=\"button\" class=\"dropdown\"><span class=\"dropdown__icon\">…</span>KPT<span class=\"dropdown__chevron\">…</span></button>")}</section>')
    return content

def p_popover():
    add = icon('Icon/Assets/Add', 'icon')
    crown = '<svg viewBox="0 0 12 12" aria-hidden="true"><circle cx="6" cy="6" r="6" fill="currentColor"/><path d="M3.2 4.3 4.6 5.6 6 3.6l1.4 2 1.4-1.3-.5 3.4H3.7z" fill="#fff"/></svg>'
    mem = lambda n, lead=False: '<li class="member-item">' + (f'<span class="avatar-leader">{avatar("icon")}<span class="avatar-leader__badge">{crown}</span></span>' if lead else avatar('icon')) + f'<span>{n}</span></li>'
    members = f'<li><button type="button" class="member-item member-item--add"><span class="member-item__add">{add}</span>팀원 추가</button></li>' + mem('홍길동', True) + ''.join(mem(n) for n in ['김레이어', '이회고'])
    pop = f'<div class="popover"><div class="popover__head"><p class="popover__title">인원<span class="popover__count">4</span></p><button type="button" class="text-button text-button--neutral">편집</button></div><ul class="member-list">{members}</ul></div>'
    menu = '<ul class="menu" role="menu"><li><button type="button" class="menu-item is-hover" role="menuitem">대표자 변경</button></li><li><button type="button" class="menu-item menu-item--danger" role="menuitem">팀원 삭제</button></li></ul>'
    content = page_head('Components', 'Popover · Menu', '버튼을 눌렀을 때 그 아래에 가볍게 뜨는 패널(Popover)과 행동 목록(Menu)입니다. 바깥을 누르면 바로 닫히고, 하던 일로 돌아갑니다.', status=('ok', '확정'), node='437-6315')
    content += (f'<section class="section"><h2>예시</h2><div class="canvas canvas--sunk" style="position:relative;overflow:hidden;min-height:340px"><div style="display:flex;gap:16px;align-items:flex-start;flex-wrap:wrap">{pop}{menu}</div></div><p class="canvas-caption">웹 08 멤버관리: 팀원 Dropdown → 인원 Popover → 팀원 더보기 Menu. 딤드 없이 그림자로만 띄웁니다.</p></section>'
        + '<section class="section"><h2>딤드 규칙</h2><p>Popover · Menu는 뒤에 딤드를 깔지 않고 그림자(<a href="elevation.html">Shadow 300</a>)로만 띄웁니다. 드롭다운이든 더보기든 같은 방식이라, 뒤 화면을 그대로 보면서 바로 닫을 수 있습니다. 딤드(<code>overlay/dim</code>, 72%)는 흐름을 멈추고 답을 받아야 하는 <a href="popup.html">Popup</a> · Modal (Web) · <a href="bottom-sheet.html">Bottom Sheet</a>에만 씁니다.</p></section>'
        + '<section class="section"><h2>Popover</h2>' + table(['항목', '값'], [['틀', '너비 280, 흰 바탕, 모서리 12(<code>--radius-card</code>), <a href="elevation.html">Shadow 300</a>, 안쪽 20 · 사이 20'], ['머리', '제목 <a href="typography.html">Title 16 Bold</a> + 개수 Gray 600(Show Count) + 오른쪽 <a href="button.html">Text Button</a> Neutral(Show Action, 예: 편집)'], ['내용', 'Content <strong>슬롯</strong> — 예: List/Member Item'], ['위치', '연 버튼 바로 아래, 오른쪽 끝을 맞춤'], ['Figma', '<code>Popover</code> · Title · Count · Show Count · Show Action · Content(슬롯)']]) + '</section>'
        + '<section class="section"><h2>List/Member Item</h2>' + table(['Type', '값'], [['Add', 'Blue 100 동그라미 32 + Add 16(Blue 600) + 팀원 추가(<a href="typography.html">Body 15 Medium</a> Blue 600)'], ['Member', '<a href="avatar.html">Profile 32</a> + 이름(Body 15 Medium Gray 900). 대표자는 Profile의 Show Leader(왕관)'], ['간격', '높이 32, 아이콘과 글자 사이 12, 줄 사이 12'], ['Figma', '<code>List/Member Item</code> · Type · Name']]) + '</section>'
        + '<section class="section"><h2>Menu</h2>' + table(['항목', '값'], [['틀', '너비 165(긴 글자면 넓어짐), 흰 바탕, 모서리 8, Shadow 300, 위아래 6, 줄 사이 4'], ['줄(Menu Item)', '높이 36, 좌우 20, <a href="typography.html">Subtitle 14 SemiBold</a>'], ['Type', 'Default Gray 800 · Danger <code>text/error</code>(Red 500) — 삭제처럼 되돌리기 어려운 행동, 맨 아래'], ['State', 'Hover Gray 100'], ['Figma', '<code>Menu</code>(Items 슬롯) · <code>Menu/Menu Item</code> · Label · Type · State']]) + '</section>'
        + f'<section class="section"><h2>코드</h2>{{code(POPOVER_CODE)}}</section>')
    return content.replace('{code(POPOVER_CODE)}', code(POPOVER_CODE))

POPOVER_CODE = """<link rel="stylesheet" href="css/popup.css">
<link rel="stylesheet" href="css/lists.css">

<div class="popover">
  <div class="popover__head">
    <p class="popover__title">인원<span class="popover__count">4</span></p>
    <button type="button" class="text-button text-button--neutral">편집</button>
  </div>
  <ul class="member-list">
    <li><button type="button" class="member-item member-item--add"><span class="member-item__add">…Add…</span>팀원 추가</button></li>
    <li class="member-item"><span class="avatar-leader"><span class="avatar">…</span><span class="avatar-leader__badge">…</span></span>홍길동</li>
  </ul>
</div>

<ul class="menu" role="menu">
  <li><button type="button" class="menu-item" role="menuitem">대표자 변경</button></li>
  <li><button type="button" class="menu-item menu-item--danger" role="menuitem">팀원 삭제</button></li>
</ul>"""

def p_analysis():
    E = lambda e: bare(G[f'Icon/Graphic/Emotion|Emotion={e}'])
    per = bare(G['Icon/Graphic/Person|State=Color'])
    leg = [('Happy', '매우 만족', 8), ('Good', '만족', 6), ('Better', '보통', 5), ('Soso', '불만족', 4), ('Bad', '매우 불만족', 3)]
    sat = ('<div class="satisfaction"><div class="satisfaction__chart" style="background:conic-gradient(var(--color-blue-800) 0 11.5%, var(--color-blue-700) 0 26.9%, var(--color-blue-400) 0 46.2%, var(--color-blue-500) 0 69.2%, var(--color-blue-600) 0 100%)"></div>'
           '<ul class="satisfaction__legend">' + ''.join(f'<li><span>{E(e)}{l}</span><b>{n}</b></li>' for e, l, n in leg) + '</ul></div>')
    goal = f'<div class="goal-rate"><span class="goal-rate__tip" style="left:78%">{per}78%</span><div class="goal-rate__track"><span class="is-on"></span><span class="is-on"></span><span class="is-on"></span><span style="background:linear-gradient(90deg,var(--color-bg-accent) 90%,var(--color-bg-surface) 0)"></span><span></span></div><div class="goal-rate__axis"><span>0</span><span>100</span></div></div>'
    panel = f'<div class="analysis-panel"><div class="analysis-panel__half"><p class="analysis-panel__title">진행상황에 대해 대부분 <em>만족해요</em></p><div class="analysis-panel__body">{sat}</div></div><div class="analysis-panel__half"><p class="analysis-panel__title">목표달성률은 평균 <em>78%</em>에요</p><div class="analysis-panel__body">{goal}</div></div></div>'
    ic = {'good': icon('Icon/Assets/Check_Filled', 'icon'), 'bad': icon('Icon/Assets/Minus_Filled', 'icon'), 'improve': icon('Icon/Assets/More_Filled', 'icon')}
    item = lambda t, k, n, m=False: f'<li class="keyword-item keyword-item--{t}{" keyword-item--mobile" if m else ""}">{ic[t]}<span class="keyword-item__text">{k}</span>' + (f'<span class="keyword-item__count">{n}</span>' if n else '') + '</li>'
    data = [('잘 하고 있어요', 'good', [('회의 내용 문서화', '4명'), ('꾸준한 글 작성', '3명'), ('적극적인 피드백', '4명')]), ('이런 점은 부족해요', 'bad', [('잦은 회의 늘어짐', '5명'), ('회의 시간 준수', '2명'), ('꾸준한 글 작성', '2명')]), ('개선이 필요해요', 'improve', [('설득력 갖추기', '6명'), ('꾸준한 자기개발', '4명'), ('적극적인 피드백', '2명')])]
    kp = '<div class="keyword-panel">' + ''.join(f'<div class="keyword-group"><p class="keyword-group__title">{t}</p><ul class="keyword-list">' + ''.join(item(ty, k, n) for k, n in rows) + '</ul></div>' for t, ty, rows in data) + '</div>'
    mob = ('<div style="width:295px;display:flex;flex-direction:column;gap:16px"><p class="highlight-title">이회고님은<span class="badge badge--outlined badge--outlined-blue">커뮤니케이션 부족</span>외<br>3가지를 문제점으로 생각해요</p><ul class="keyword-list">'
           + ''.join(item('bad', k, '', True) for k in ['커뮤니케이션 부족', '파트별 주차 계획', '진행과정 이해 부족']) + '</ul></div>')
    title = lambda l, d: f'<p class="analysis-title"><b>{l}</b><span>{d}</span></p>'
    content = page_head('Components', 'Analysis', '회고 결과를 보여 주는 분석 블록입니다. 섹션 머리 아래에 진행상황 패널(만족도 · 목표달성률)과 키워드 묶음을 놓습니다. 차트 모양은 예시이고, 실제 비율은 데이터로 그립니다.', status=('ok', '확정'), node='471-6698')
    content += (f'<section class="section"><h2>웹 분석 화면</h2><p>웹 04 회고 완료 분석의 팀 탭 구성입니다.</p><div class="canvas" style="overflow-x:auto"><div style="min-width:760px;display:flex;flex-direction:column;gap:32px"><div class="analysis-section">{title("진행상황", "우리팀의 진행상황에 대해 이렇게 생각해요!")}{panel}</div><div class="analysis-section">{title("회고", "우리팀은 이렇게 회고 하고 있어요!")}{kp}</div></div></div></section>'
        + '<section class="section"><h2>구성</h2>' + table(['컴포넌트', '값'], [['<code>Analysis/Section Title</code>', 'Label(Title 14 Bold) + 세로선(Gray 300) + Description(Body 14 Medium), Gray 800, 사이 7. 아래 9 띄우고 패널'], ['<code>Analysis/Progress Panel</code>', 'Gray 100 · 모서리 12 · 안쪽 24/24/28, 세로선으로 반 나눔. 제목 Subtitle 16 SemiBold + 강조 단어 Blue 600'], ['<code>Analysis/Satisfaction</code>', '도넛 138(구멍 69) + 범례 5줄(Emotion 18 · Body 12 Medium · 인원 Gray 500). 조각 색: 매우 만족 Blue 600 · 만족 500 · 보통 400 · 불만족 700 · 매우 불만족 800'], ['<code>Analysis/Goal Rate</code>', '5칸 막대 높이 30 · 칸 사이 3 · 양끝 둥긂, 채운 부분 Blue 600 · 빈 칸 흰색, 위 흰 말풍선(Person 18 + %), 아래 0 · 100. 실제 비율만큼 채움'], ['<code>Analysis/Keyword Group</code>', '제목 Subtitle 16 SemiBold + Items 슬롯(사이 8), 판 안 3열'], ['<code>Analysis/Keyword Item</code>', 'Type=Good(Check Gray 800) · Bad(Minus Red 500) · Improve(More Blue 600) × Platform=Web(흰 바탕 · 아이콘 16 · Subtitle 14) · Mobile(Gray 100 · 아이콘 24 · Subtitle 16). Show Count'], ['<code>Analysis/Highlight Title</code>', '모바일 개인 분석의 강조 문장. Name("이회고님은") + <a href="badge.html">Badge Outlined Blue 22</a>(키워드) + Particle("를" · "외") / 둘째 줄 Sentence. Subtitle 16 SemiBold Gray 900, 아래 Keyword Item(Mobile) 목록']]) + '</section>'
        + f'<section class="section"><h2>모바일 개인 분석</h2><p>강조 문장(<code>Analysis/Highlight Title</code>) 아래에 키워드 줄(Mobile)을 쌓습니다. 키워드 칩은 <a href="badge.html">Badge Outlined Blue</a>입니다.</p><div class="canvas canvas--center">{mob}</div></section>'
        + '<section class="section"><h2>규칙</h2>' + table(['', '규칙'], [['Do', '분석 블록은 Analysis 컴포넌트로 조합합니다. 차트 색과 순서는 위 표를 따릅니다.'], ['Do', '도넛 · 막대의 실제 비율은 데이터로 그립니다. Figma 모양은 자리 예시입니다.'], ["Don't", '답을 입력받는 0~100 점수에는 Goal Rate 대신 <a href="cards.html">Answer/Score Bar</a>를 씁니다.']]) + '</section>'
        + '<section class="section"><h2>코드</h2>' + code('<link rel="stylesheet" href="css/analysis.css">\n\n<div class="analysis-panel">\n  <div class="analysis-panel__half">…<div class="satisfaction">…</div></div>\n  <div class="analysis-panel__half">…<div class="goal-rate">…</div></div>\n</div>\n<div class="keyword-panel"><div class="keyword-group">…<ul class="keyword-list"><li class="keyword-item keyword-item--good">…</li></ul></div></div>') + '</section>')
    return content

def p_writing():
    chevL = icon('Icon/Assets/Chevron-Left', 'icon'); chevR = icon('Icon/Assets/Chevron-Right', 'icon')
    rows = [('*', '진행상황에 대해 얼마나 만족하나요?', 'answered'), ('*', '목표했던 부분에 얼마나 달성하셨나요?', 'current'), ('1.', '계속 유지하고 싶은 것은 무엇인가요?', ''), ('2.', '어려움을 느꼈던 부분은 무엇인가요?', ''), ('3.', '새롭게 시도해 볼 내용은 무엇인가요?', '')]
    items = ''.join(f'<li><button type="button" class="question-index__item{" is-answered" if s == "answered" else ""}"{" aria-current=\"true\"" if s == "current" else ""}><span class="question-index__marker">{m}</span><span class="question-index__q">{q}</span></button></li>' for m, q, s in rows)
    index = f'<div class="question-index"><div class="question-index__head"><p class="question-index__title">질문 전체보기</p><span class="question-index__progress">작성 완료 1/5</span></div><ul class="question-index__list">{items}</ul></div>'
    pager = f'<div class="question-pager"><button type="button" class="pager-btn">{chevL}이전</button><button type="button" class="pager-btn pager-btn--next">다음{chevR}</button></div>'
    pager_d = f'<div class="question-pager"><button type="button" class="pager-btn" disabled>{chevL}이전</button><button type="button" class="pager-btn pager-btn--next">다음{chevR}</button></div>'
    content = page_head('Components', 'Writing Panel', '웹에서 회고를 쓰는 패널에 들어가는 요소입니다. 지금 질문을 알리는 태그, 질문 사이를 오가는 버튼, 전체 질문과 작성 상태를 보여 주는 목록이 있습니다.', status=('ok', '확정'), node='394-6689')
    content += (f'<section class="section"><h2>Question Tag</h2><p>지금 질문의 종류와 번호를 알려 주는 읽기 전용 태그입니다. 누를 수 없습니다. 상태나 개수는 <a href="badge.html">Badge</a>를 씁니다.</p><div class="canvas canvas--center"><span class="question-tag">사전질문 1</span><span class="question-tag" style="margin-left:8px">질문 2</span></div>'
                + table(['항목', '값'], [['크기', '위아래 8 · 좌우 12, 모서리 12, 너비는 글자에 맞춤(높이 38)'], ['색 · 글자', 'Gray 100 바탕, <a href="typography.html">Subtitle 16 SemiBold</a> Gray 900'], ['Figma', '<code>Question Tag</code> · Label']]) + '</section>'
                f'<section class="section"><h2>Button/Pager</h2><p>이전 · 다음 질문으로 옮겨 가는 작은 버튼입니다. 첫 질문의 이전, 마지막 질문의 다음은 Disabled로 둡니다.</p><div class="canvas canvas--center"><div style="display:flex;gap:24px;flex-wrap:wrap">{pager_d}{pager}</div></div>'
                + table(['항목', '값'], [['크기', '높이 32, 화살표 쪽 8 · 반대쪽 12, 사이 6, 모서리 8(<code>--radius-button-xs</code>)'], ['색 · 글자', 'Gray 100 바탕 → Hover Gray 200, <a href="typography.html">Title 14 Bold</a> Gray 800 · Disabled Gray 400, 화살표 16'], ['Figma', '<code>Button/Pager</code> · Direction=Prev · Next, State=Default · Hover · Disabled']]) + '</section>'
                f'<section class="section"><h2>Question Index</h2><p>패널 오른쪽에서 전체 질문과 작성 상태를 보여 줍니다. 줄을 누르면 그 질문으로 이동합니다.</p><div class="canvas canvas--sunk canvas--center">{index}</div>'
                + table(['상태', '모습', '뜻'], [['Unanswered', '흰 바탕, 글자 Gray 600', '아직 답하지 않은 질문'], ['Current', 'Blue 50 바탕', '지금 보고 있는 질문'], ['Answered', '흰 바탕, 글자 Gray 900', '답을 쓴 질문']])
                + table(['항목', '값'], [['크기', '너비 294, 테두리 Opacity 8, 모서리 12. 머리 위 16 · 좌우 20 · 아래 8'], ['머리', '제목 Subtitle 16 SemiBold + "작성 완료 n/m" Body 12 Medium Gray 600'], ['줄', '278 × 52, 위아래 16 · 좌우 8, 모서리 8. 앞 표시(사전질문 * · 번호 1.) Body 15 Medium, 질문 Body 14 Medium 한 줄'], ['Figma', '<code>Question Index (Web)</code> · Title · Progress, 줄은 <code>Question Index Item</code> · State · Marker · Question']]) + '</section>'
                f'<section class="section"><h2>코드</h2>{code("<link rel=\"stylesheet\" href=\"css/writing.css\">" + chr(10) + "<span class=\"question-tag\">사전질문 1</span>" + chr(10) + "<div class=\"question-pager\"><button class=\"pager-btn\" disabled>…이전</button><button class=\"pager-btn pager-btn--next\">다음…</button></div>" + chr(10) + "<button class=\"question-index__item is-answered\">… / aria-current=\"true\" …</button>")}</section>')
    return content

def p_badge():
    def b(t, c='blue'): return '<span class="badge ' + ' '.join('badge--' + x for x in c.split()) + f'">{t}</span>'
    card = ('<div class="bd-card"><span class="bd-card__thumb"></span><div class="bd-card__body"><div class="bd-card__row">'
            '<strong class="text-title-16-bold bd-card__title">떡잎마을방범대대대대대대대대대대대</strong>' + b('진행 중 1') + '</div>'
            '<span class="text-body-13-medium bd-card__desc">IT 연합동아리 디프만 15기의 프로젝트 방향성 체크</span>'
            '<span class="text-body-12-medium bd-card__desc">멤버 11명 · 회고 4개</span></div></div>')
    content = page_head('Components', 'Badge', '상태나 개수를 짧게 알려 주는 읽기 전용 라벨입니다. 누를 수 없고, 카드 제목 옆처럼 정보 바로 옆에 붙여 씁니다.',
                        status=('ok', '확정'), node='332-4239')
    spec = table(['항목', '값'], [['크기', '22: 높이 22 · 좌우 6 / 25: 위아래 4 · 좌우 8, 너비는 글자에 맞춤'], ['모서리', 'Radius 4 (<code>--radius-4</code>)'], ['글자', 'Body 12 SemiBold'], ['Blue', '바탕 Blue 100 · 글자 Blue 600 (흰·회색 바탕 위)'], ['White', '바탕 Gray 0 · 글자 Blue 600 (연파랑 회고 카드 위의 D-day)'], ['Gray', '바탕 Gray 100 · 글자 Gray 800 (답변 카드의 작성자 이름)'], ['Outlined', '높이 22 · 좌우 6, 테두리 1px, 글자 <a href="typography.html">Caption 11 SemiBold</a>. Gray(작성 전) 바탕 Gray 200 · 테두리 Gray 400 · 글자 Gray 700 / Blue(작성 중) Blue 200 · 300 · 700 / Green(제출 완료) Green 100 · 200 · 900 / Dark(분석 완료) Opacity 12 · Gray 500 · Gray 900'], ['Figma', '<code>Badge</code> · 속성 Label(텍스트), Color=Blue · White · Gray · Green · Dark, Size=22 · 25, Style=Filled · Outlined']])
    use = table(['상황', '쓸 것'], [['진행 상태 · 개수 · D-day를 보여 줄 때', 'Badge'], ['눌러서 고르거나 걸러야 할 때', '<a href="chip-button.html">Chip Button</a>'], ['상태를 바꾸는 드롭다운(진행 중 · 미달성 · 완료)', '없음 — 옛 Component 18은 쓰이지 않아 컴포넌트를 해제하고 디자인으로만 남김. 실행목표 상태 표시는 Badge(실행 중)']])
    snippet = code('<span class="badge badge--blue">진행 중 1</span>\n<span class="badge badge--white">D-15</span>\n<span class="badge badge--gray badge--25">김레이어</span>\n<span class="badge badge--outlined badge--outlined-green">제출 완료</span>')
    content += (f'<section class="section"><h2>예시</h2><div class="canvas canvas--center"><div class="bd-row">{b("진행 중 1")}{b("D-15")}{b("진행 중 3")}</div></div>'
                f'<div class="canvas canvas--sunk canvas--center">{card}</div><p class="canvas-caption">홈 스페이스 카드: 제목이 길면 제목이 말줄임되고 Badge는 줄지 않습니다.</p>'
                f'<h3 class="tk-h3">Color</h3><div class="canvas bd-colors"><div class="bd-swatch"><span class="state-label">Blue · 흰·회색 바탕 위</span><div class="bd-on bd-on--white">{b("진행 중 1")}</div></div>'
                f'<div class="bd-swatch"><span class="state-label">White · 색 있는 카드 위</span><div class="bd-on bd-on--blue">{b("D-15", "white")}</div></div>'
                f'<div class="bd-swatch"><span class="state-label">Gray · 이름 등 중립 정보</span><div class="bd-on bd-on--white">{b("김레이어", "gray")}</div></div></div>'
                f'<h3 class="tk-h3">Size</h3><div class="canvas bd-colors"><div class="bd-swatch"><span class="state-label">22 · 제목 옆 상태, D-day</span><div class="bd-on bd-on--white">{b("진행 중 1")}</div></div>'
                f'<div class="bd-swatch"><span class="state-label">25 · 카드 머리의 이름표</span><div class="bd-on bd-on--white">{b("김레이어", "gray 25")}</div></div></div>'
                f'<h3 class="tk-h3">Style = Outlined</h3><p>웹 회고 카드의 진행 상태 태그입니다. 크기는 22 하나입니다.</p><div class="canvas bd-colors"><div class="bd-swatch"><span class="state-label">Gray · 작성 전</span><div class="bd-on bd-on--white">{b("작성 전", "outlined outlined-gray")}</div></div><div class="bd-swatch"><span class="state-label">Blue · 작성 중</span><div class="bd-on bd-on--white">{b("작성 중", "outlined outlined-blue")}</div></div><div class="bd-swatch"><span class="state-label">Green · 제출 완료</span><div class="bd-on bd-on--white">{b("제출 완료", "outlined outlined-green")}</div></div><div class="bd-swatch"><span class="state-label">Dark · 분석 완료</span><div class="bd-on bd-on--white">{b("분석 완료", "outlined outlined-dark")}</div></div></div></section>'
                f'<section class="section"><h2>스펙</h2>{spec}</section>'
                f'<section class="section"><h2>쓰는 법</h2>{use}<p>한두 단어로 씁니다. 문장은 넣지 않습니다. 바탕과 같은 계열 색이 겹치지 않게 Blue · White · Gray 중에 고르고, 제목 옆이면 22, 카드 머리에 단독으로 놓으면 25를 씁니다. 다른 상태 색은 대표 화면을 정리하며 필요할 때 추가합니다.</p></section>'
                f'<section class="section"><h2>코드</h2>{snippet}</section>')
    return content

def bt(cls, label='버튼', state=None, sm=False, icon_html='', block=False):
    st = {'hover': ' is-hover', 'pressed': ' is-pressed'}.get(state, '')
    dis = ' disabled' if state == 'disabled' else ''
    return f'<button type="button" class="btn {cls}{" btn--xs" if sm == "xs" else (" btn--sm" if sm else "")}{" btn--block" if block else ""}{st}"{dis}>{icon_html}{label}</button>'

BTN_KINDS = [  # label, class, default, hover, pressed, text
    ('Primary', 'btn--primary', 'Gray 900', 'Gray 800', 'Gray 700', 'Gray 0'),
    ('Secondary', 'btn--secondary', 'Gray 300', 'Gray 400', 'Gray 500', 'Gray 900'),
    ('Blue', 'btn--blue', 'Blue 600', 'Blue 700', 'Blue 800', 'Gray 0'),
    ('Light Blue', 'btn--light-blue', 'Blue 100', 'Blue 200', 'Blue 300', 'Blue 600'),
    ('White', 'btn--white', 'Gray 0', 'Gray 100', 'Gray 200', 'Gray 900'),
    ('Ghost', 'btn--ghost', 'Gray 0', 'Gray 100', 'Gray 200', 'Gray 900'),
    ('Ghost Blue', 'btn--ghost-blue', 'Gray 0', 'Blue 50', 'Blue 100', 'Blue 600'),
    ('Outlined', 'btn--outlined', 'Gray 0 + 테두리 Gray 300', 'Gray 100', 'Gray 200', 'Gray 900'),
    ('Outlined Blue', 'btn--outlined-blue', 'Gray 0 + 테두리 Blue 300', 'Blue 50', 'Blue 100', 'Blue 600'),
    ('Floating', 'btn--floating', 'Gray 900 + Shadow 200', 'Gray 800', 'Gray 700', 'Gray 0'),
]

def p_button():
    write = icon('Icon/Assets/Write', 'icon')
    def grid(kinds, sm=False):
        head = '<div class="bt-h"></div>' + ''.join(f'<div class="bt-h">{s}</div>' for s in ['Default', 'Hover', 'Pressed', 'Disabled'])
        rows = ''
        for name, cls in kinds:
            ic = write if cls == 'btn--floating' else ''
            rows += f'<div class="bt-name">{name}</div>' + ''.join(f'<div class="bt-cell">{bt(cls, state=s, sm=sm, icon_html=ic)}</div>' for s in [None, 'hover', 'pressed', 'disabled'])
        return f'<div class="bt-grid">{head}{rows}</div>'
    filled = [('Primary', 'btn--primary'), ('Secondary', 'btn--secondary'), ('Blue', 'btn--blue'), ('Light Blue', 'btn--light-blue'), ('White', 'btn--white')]
    other = [('Ghost', 'btn--ghost'), ('Ghost Blue', 'btn--ghost-blue'), ('Outlined', 'btn--outlined'), ('Outlined Blue', 'btn--outlined-blue'), ('Floating', 'btn--floating')]
    live = ''.join(bt(c) for c in ['btn--primary', 'btn--secondary', 'btn--blue', 'btn--light-blue', 'btn--white', 'btn--ghost', 'btn--outlined', 'btn--outlined-blue']) + bt('btn--floating', '회고 쓰기', icon_html=write)
    rules = [[n, f'<code>.{c}</code>', d, h, pr, t] for n, c, d, h, pr, t in BTN_KINDS]
    size = [['높이', '48px', '40px', '36px'], ['좌우 여백', '20px', '16px', '12px'], ['아이콘 · 글자 간격', '10px', '8px', '4px'], ['모서리', '12px', '10px', '8px (--radius-button-xs)'],
            ['글자', '<a href="typography.html">Subtitle 16 SemiBold</a>', '<a href="typography.html">Subtitle 14 SemiBold</a>', '<a href="typography.html">Subtitle 14 SemiBold</a>'], ['아이콘', '18px', '16px', '18px'],
            ['Floating', '좌우 18px · 간격 4px · 글자 14px · 완전히 둥근 모서리', '좌우 16px · 간격 4px · 글자 14px · 완전히 둥근 모서리', '없음'], ['클래스', '<code>.btn</code>', '<code>.btn.btn--sm</code>', '<code>.btn.btn--xs</code>']]
    sa = f'<span class="safe-area" aria-hidden="true">{bare(asset("safe-area-ios14"))}</span>'
    def group(kind, inner): return f'<div class="btn-group btn-group--{kind}"><div class="btn-group__buttons">{inner}</div>{sa}</div>'
    groups = (f'<figure class="bt-g"><figcaption>Single · 버튼 1개</figcaption>{group("one", bt("btn--primary", "완료"))}</figure>'
              f'<figure class="bt-g"><figcaption>Stacked · Primary + Ghost · 간격 4px</figcaption>{group("vertical", bt("btn--primary", "저장하기") + bt("btn--ghost", "나중에 할게요"))}</figure>'
              f'<figure class="bt-g"><figcaption>Side by Side · Secondary + Primary · 간격 8px</figcaption>{group("horizontal", bt("btn--secondary", "취소") + bt("btn--primary", "확인"))}</figure>')
    contrast = [['Primary, Blue 눌림, Floating', '흰 글자', '16:1 이상', chip('ok', '통과')],
                ['Secondary·White·Ghost·Outlined', 'Gray 900 글자', '12:1 이상', chip('ok', '통과')],
                ['Blue', '흰 글자 / Blue 600', '2.7:1', chip('wait', '미달 유지')],
                ['Ghost Blue · Outlined Blue', 'Blue 600 / 흰 배경', '2.7:1', chip('wait', '미달 유지')],
                ['Light Blue', 'Blue 600 / Blue 100', '2.4:1', chip('wait', '미달 유지')]]
    content = page_head('Components', 'Button',
        '버튼은 사용자가 원하는 동작을 실행하게 하는 요소입니다. 한 화면에서 가장 중요한 동작 하나에는 Filled Primary를 쓰고, 함께 놓이는 보조 동작은 Secondary·Ghost·Outlined로 위계를 나눕니다. 크기는 48px(기본)과 40px 두 가지입니다.',
        status=('ok', '확정'), node='1-1123')
    content += f'''<section class="section"><h2>예시</h2><p>마우스를 올리거나 눌러 보세요. 호버는 한 단계, 눌림은 두 단계 진해집니다.</p><div class="canvas"><div class="bt-live">{live}</div></div></section>
<section class="section"><h2>언제 쓰나요</h2>{table(['종류', '쓰는 곳'], [
    ['Filled Primary', '화면에서 가장 중요한 동작 하나. 저장, 완료, 다음'],
    ['Filled Secondary · White', 'Primary와 나란히 놓이는 보조 동작. 취소, 이전'],
    ['Filled Blue · Light Blue', '브랜드 색으로 강조해야 하는 동작'],
    ['Ghost', '덜 중요한 동작. 나중에 하기, 건너뛰기'],
    ['Outlined', '목록이나 카드 안에서 영역을 구분해야 하는 보조 동작'],
    ['Floating', '스크롤해도 화면 위에 떠 있어야 하는 동작. 회고 쓰기'],
])}</section>
<section class="section"><h2>Filled · 48px</h2><div class="canvas">{grid(filled)}</div></section>
<section class="section"><h2>Filled · 40px</h2><div class="canvas">{grid(filled, sm=True)}</div></section>
<section class="section"><h2>Filled · 36px <span class="count">웹</span></h2><div class="canvas">{grid(filled, sm="xs")}</div><p class="canvas-caption">웹 화면 머리 · 카드 안의 작은 행동에 씁니다(회고 추가하기, 제출하기, 수정). Figma Size=36은 Filled에만 있습니다.</p></section>
<section class="section"><h2>Ghost · Outlined · Floating · 48px</h2><div class="canvas">{grid(other)}</div></section>
<section class="section"><h2>Ghost · Outlined · Floating · 40px</h2><div class="canvas">{grid(other, sm=True)}</div></section>
<section class="section"><h2>상태 규칙</h2><p>모든 버튼은 같은 규칙을 따릅니다. 호버는 팔레트에서 <strong>한 단계</strong>, 눌림은 <strong>두 단계</strong> 진한 색입니다. 비활성은 종류와 상관없이 <strong>Gray 100 배경, Gray 400 글자</strong> 하나로 통일합니다. 테두리는 없애고, Floating만 그림자를 유지합니다.</p>{table(['종류', '클래스', '기본', '호버', '눌림', '글자'], rules)}</section>
<section class="section"><h2>크기</h2>{table(['항목', '48 (기본)', '40', '36 (웹)'], size)}<p class="note">40px는 모바일 카드 안, 목록 옆처럼 공간이 좁은 곳에 씁니다. 화면 아래 주요 버튼은 48px를 씁니다. 웹(1440)은 36px를 주로 쓰고, 작성 패널 아래 "임시저장 · 작성 완료"처럼 한 영역을 마무리하는 행동에는 40px를, 웹 모달 아래 버튼(이전 · 다음)에는 48px를 씁니다. 모달 안에서 너비를 채우는 추가 버튼도 40px(Light Blue)입니다.</p></section>
<section class="section"><h2>아이콘만 있는 버튼</h2><p>Show Label을 끄고 Show Icon을 켜면 아이콘만 남습니다. 무엇을 하는 버튼인지 주변 맥락으로 분명할 때만 쓰고, 코드에는 <code>aria-label</code>을 꼭 넣습니다.</p><div class="canvas"><div style="max-width:472px"><button type="button" class="btn btn--sm btn--light-blue btn--icon-only" style="width:100%" aria-label="질문 추가">{icon('Icon/Assets/Add', 'icon')}<span class="btn__label">질문 추가</span></button></div></div>{table(['항목', '값'], [['예', '질문 리스트 모달의 질문 추가: Size 40 · Light Blue · Add 아이콘 16 · 너비 채움'], ['Figma', 'Show Label 끔 + Show Icon 켬 + Icon 바꿈'], ['코드', '<code>.btn--icon-only</code> + <code>aria-label</code>']])}</section>
<section class="section"><h2>Text Button</h2><p>배경 없는 글자 버튼입니다. 앱 바 오른쪽(완료 · 마치기)은 Accent, 목록 머리의 삭제 · 편집처럼 가벼운 보조 행동은 Neutral을 씁니다.</p><div class="canvas"><div class="states"><div class="state"><span class="state-label">Accent</span><button type="button" class="text-button">완료</button></div><div class="state"><span class="state-label">Accent · Disabled</span><button type="button" class="text-button" disabled>마치기</button></div><div class="state"><span class="state-label">Neutral</span><button type="button" class="text-button text-button--neutral">삭제</button></div><div class="state"><span class="state-label">Neutral · Disabled</span><button type="button" class="text-button text-button--neutral" disabled>삭제</button></div></div></div>{table(['Type', '값', '쓰는 곳'], [['Accent', '<a href="typography.html">Subtitle 16 SemiBold</a> Blue 600', '<a href="app-bar.html">App Bar</a> 오른쪽 완료 · 마치기'], ['Neutral', '<a href="typography.html">Body 14 Medium</a> Gray 500', '목록 머리 삭제 · 편집(웹 질문 리스트 모달)'], ['Disabled', 'Gray 400', '아직 누를 수 없을 때']])}<p class="note">Figma <code>Button/Text Button</code> · Label · Type(Accent · Neutral) · State(Default · Disabled). 코드 <code>.text-button</code> · <code>.text-button--neutral</code>.</p></section>
<section class="section"><h2>버튼 그룹</h2><p>화면 맨 아래에 놓이는 버튼 묶음입니다. 너비 375px, 여백 위 8 · 좌우 20 · 아래 16px이며 아래에 홈 표시줄 영역이 붙습니다.</p><div class="canvas canvas--sunk"><div class="bt-groups">{groups}</div></div></section>
<section class="section"><h2>명도 대비</h2><p>글자와 배경의 대비는 4.5:1 이상을 권장합니다(WCAG AA). 파란 글자 계열은 기준에 못 미치지만 브랜드 색을 유지하기로 했습니다.</p>{table(['버튼', '조합', '대비', '판정'], contrast)}</section>
<section class="section"><h2>코드</h2>{code("""<link rel="stylesheet" href="css/buttons.css">

<!-- 48px (기본) -->
<button class="btn btn--primary">저장하기</button>

<!-- 40px -->
<button class="btn btn--secondary btn--sm">취소</button>

<!-- 36px (웹) -->
<button class="btn btn--blue btn--xs">회고 추가하기</button>

<!-- 아이콘 + 글자 -->
<button class="btn btn--floating"><span class="icon">…</span>회고 쓰기</button>

<!-- 비활성 -->
<button class="btn btn--primary" disabled>저장하기</button>

<!-- 화면 아래 버튼 그룹 (Side by Side) -->
<!-- Single: btn-group--one · Stacked: btn-group--vertical -->
<div class="btn-group btn-group--horizontal">
  <div class="btn-group__buttons">
    <button class="btn btn--secondary">취소</button>
    <button class="btn btn--primary">확인</button>
  </div>
</div>""")}</section>
<section class="section"><h2>결정 기록</h2><div class="callouts">
  {callout('ok', '반영', '2026-10-27', '호버는 한 단계, 눌림은 두 단계 진하게 통일했습니다. Primary·Floating은 Gray 800 → 700, Blue는 Blue 700 → 800로 바꿨습니다(전에는 검은 막을 겹쳐 표현).')}
  {callout('ok', '반영', '2026-10-27', 'Ghost·Outlined·Floating의 비활성을 Filled와 같은 모양으로 통일했습니다. Outlined 비활성은 테두리를 없앴습니다.')}
  {callout('ok', '반영', '2026-10-27', 'Secondary·White·Outlined의 글자색을 Gray 800에서 Gray 900으로 맞췄습니다.')}
  {callout('ok', '반영', '2026-10-27', 'Ghost·Outlined·Floating의 속성 이름 오타 "Show lcon"(소문자 L)을 "Show Icon"으로 고쳤습니다.')}
  {callout('ok', '추가', '2026-10-27', '높이 40px 크기를 추가했습니다. Figma에는 Size 속성(48/40)으로 들어갑니다.')}
  {callout('ok', '반영', '2026-10-27', '버튼 그룹 속성을 Popup과 같은 기준으로 Button = Single · Side by Side · Stacked로 바꿨습니다. 이름만 바꿨고 배치는 그대로입니다(세로 배치 = Stacked, 가로 배치 = Side by Side).')}
  {callout('wait', '유지', '2026-10-27', '파란 글자 계열 버튼은 명도 대비 기준에 못 미치지만 현재 색을 유지합니다.')}
</div></section>'''
    return content

def cb(kind, label, state=None, icon_name=None, live=False):
    cls = {'multi': 'chip-button', 'icon': 'chip-button chip-button--icon', 'card': 'chip-button chip-button--card'}[kind]
    st = {'hover': ' is-hover', 'selected': ' is-selected'}.get(state, '')
    ic = ''
    if icon_name:
        ic = (f'<span class="icon-graphic"><span class="icon-off">{bare(G[f"Icon/Graphic/{icon_name}|State=Color"])}</span>'
              f'<span class="icon-on">{bare(G[f"Icon/Graphic/{icon_name}|State=White"])}</span></span>')
    dis = ' disabled' if state == 'disabled' else ''
    stat = '' if live else ' cb-static'
    return f'<button type="button" class="{cls}{st}{stat}" aria-pressed="{"true" if state == "selected" else "false"}"{dis}>{ic}<span>{label}</span></button>'

def p_chip():
    def states(kind, label, icon_name=None):
        cells = ''.join(f'<div class="state"><span class="state-label">{t}</span><div>{cb(kind, label, s, icon_name)}</div></div>'
                        for t, s in [('Default', None), ('Hover', 'hover'), ('Pressed · Selected', 'selected'), ('Disabled', 'disabled')])
        return f'<div class="states cb-states{" cb-states--card" if kind == "card" else ""}">{cells}</div>'
    multi = ''.join(cb('multi', t, live=True) for t in ['아침', '점심', '저녁', '주말'])
    withicon = ''.join(cb('icon', t, icon_name='Planning', live=True) for t in ['계획', '실행', '회고'])
    multi38 = ''.join(f'<button type="button" class="chip-button chip-button--38" aria-pressed="false">{t}</button>' for t in ['12:00', '1:00', '2:00', '3:00'])
    two = f'<div class="chip-pair">{cb("card", "혼자 해요", icon_name="Team", live=True)}{cb("card", "함께 해요", icon_name="Team", live=True)}</div>'
    spec = [['Multi Choice', '높이 48 · 좌우 20px · 모서리 8px', '<a href="typography.html">Body 16 Medium</a>'],
            ['Multi Choice · Size 38', '높이 38 · 안쪽 9/16px · 모서리 6px', '<a href="typography.html">Subtitle 14 SemiBold</a>'],
            ['Multi Choice with Icon', '높이 48 · 왼쪽 14 · 오른쪽 20px · 아이콘 28px · 간격 8px · 모서리 8px', '<a href="typography.html">Body 16 Medium</a>'],
            ['Two Choice', '너비 화면에 맞춤(두 개 사이 8px) · 높이 163px · 아이콘 40px · 간격 16px · 모서리 12px', '<a href="typography.html">Body 16 Medium</a>, 가운데 정렬']]
    colors = [['Default', 'Gray 100', 'Gray 800', '컬러 아이콘'], ['Hover', 'Gray 200', 'Gray 800', '컬러 아이콘'],
              ['Pressed · Selected', 'Blue 600', 'Gray 0', '흰색 아이콘'], ['Disabled', 'Gray 100', 'Gray 400', '컬러 아이콘 40%']]
    content = page_head('Components', 'Chip Button',
        '칩 버튼은 여러 보기 중에서 답을 고르게 하는 요소입니다. 하나만 고를 때는 아이콘이 큰 Two Choice를, 여러 개를 고를 때는 Multi Choice를 쓰며 선택된 칩은 Blue 600으로 표시합니다.',
        status=('ok', '확정'), node='1-1304')
    content += f'''<section class="section"><h2>예시</h2><p>눌러서 선택해 보세요. 다시 누르면 선택이 풀립니다.</p>
<div class="canvas"><div class="stack stack--loose"><div class="chip-group cb-demo">{multi}</div><div class="chip-group cb-demo">{multi38}</div><div class="chip-group cb-demo">{withicon}</div><div class="cb-two">{two}</div></div></div></section>
<section class="section"><h2>종류</h2>{table(['종류', '쓰는 곳'], [['Multi Choice', '여러 개를 고를 수 있는 짧은 보기. 시간대, 관심사'], ['Multi Choice with Icon', '보기를 아이콘으로 구분하면 더 빨리 읽히는 경우'], ['Two Choice', '둘 중 하나를 고르는 큰 질문. 온보딩의 유형 선택']])}</section>
<section class="section"><h2>상태</h2><div class="canvas"><div class="stack stack--loose">{states('card', '유형타이틀', 'Team')}{states('icon', '타이틀', 'Planning')}{states('multi', '타이틀')}</div></div>{table(['상태', '배경', '글자', '아이콘'], colors)}<p class="note">선택은 칩이 가진 상태 중 하나라 눌림과 같은 색을 씁니다. 비활성은 <a href="button.html">Button</a>의 비활성 색과 같습니다.</p></section>
<section class="section"><h2>스펙</h2>{table(['종류', '크기', '글자'], spec)}</section>
<section class="section"><h2>코드</h2>{code("""<link rel="stylesheet" href="css/chips.css">

<!-- 선택 여부는 aria-pressed로 -->
<div class="chip-group">
  <button class="chip-button" aria-pressed="true">아침</button>
  <button class="chip-button" aria-pressed="false">점심</button>
</div>

<!-- Size 38 (시간 고르기 등 촘촘한 줄) -->
<button class="chip-button chip-button--38" aria-pressed="false">1:00</button>

<!-- 아이콘 포함 -->
<button class="chip-button chip-button--icon" aria-pressed="false">
  <span class="icon-graphic">
    <span class="icon-off">컬러 SVG</span><span class="icon-on">흰색 SVG</span>
  </span>
  <span>계획</span>
</button>

<!-- Two Choice: 화면 너비에 맞춰 두 칸 -->
<div class="chip-pair">
  <button class="chip-button chip-button--card" aria-pressed="false">…<span>혼자 해요</span></button>
  <button class="chip-button chip-button--card" aria-pressed="false">…<span>함께 해요</span></button>
</div>""")}</section>
<section class="section"><h2>결정 기록</h2><div class="callouts">
  {callout('ok', '추가', '2026-10-27', 'Multi Choice에 Size 속성을 만들고 높이 38, 모서리 6px 크기를 추가했습니다. 글자는 Subtitle 14 SemiBold입니다. Date Time Picker의 시간 칩이 이 크기를 씁니다.')}
  {callout('ok', '추가', '2026-10-27', '비활성 상태를 추가했습니다. 색은 버튼 비활성과 같은 Gray 100 배경, Gray 400 글자입니다. 아이콘은 컬러 아이콘을 40% 투명도로 씁니다.')}
  {callout('ok', '확정', '2026-10-27', '선택(Selected)은 눌림과 같은 상태로 둡니다.')}
  {callout('ok', '확정', '2026-10-27', '글자색은 Gray 800을 유지합니다. 버튼(Gray 900)과 다릅니다.')}
  {callout('ok', '확정', '2026-10-27', '모서리 8px는 버튼(12px)과 의도적으로 다르게 둡니다.')}
  {callout('ok', '반영', '2026-10-27', 'Two Choice는 너비가 화면에 맞춰 늘어나고, 글자가 길면 가운데 정렬로 줄바꿈됩니다. 전에는 163px로 고정이라 긴 글자가 넘쳤습니다.')}
  {callout('ok', '반영', '2026-10-27', 'Figma 이름 오타 "Multi Chioce"를 "Multi Choice"로 고쳤습니다.')}
</div></section>'''
    return content

def pb(size, done):
    segs = ''.join(f'<li class="progress-bar__step{" is-done" if i < done else ""}"></li>' for i in range(size))
    return f'<div class="progress-bar" role="progressbar" aria-valuemin="0" aria-valuemax="{size}" aria-valuenow="{done}" aria-label="{size}단계 중 {done}단계"><ol class="progress-bar__track">{segs}</ol></div>'

def p_progress():
    grid = ''
    for size in (4, 3, 2):
        rows = ''.join(f'<div class="pb-row"><span class="state-label">Current {c}</span>{pb(size, c)}</div>' for c in range(size + 1))
        grid += f'<div class="sub"><h3>{size}단계</h3><div class="pb-list">{rows}</div></div>'
    content = page_head('Components', 'Progress Bar',
        '여러 단계로 나뉜 과정에서 지금 몇 번째 단계인지 보여 줍니다. 지난 단계와 지금 단계는 Blue 600, 남은 단계는 옅은 회색으로 표시합니다.',
        status=('ok', '확정'), node='1-1304')
    content += f'''<section class="section"><h2>예시</h2><p>버튼을 눌러 단계를 옮겨 보세요.</p><div class="canvas canvas--center"><div class="pb-demo"><div id="pb-live">{pb(4, 1)}</div><div class="pb-ctrl"><button type="button" class="btn btn--secondary btn--sm" data-pb="-1">이전</button><button type="button" class="btn btn--primary btn--sm" data-pb="1">다음</button></div></div></div></section>
<section class="section"><h2>단계 수와 현재 단계</h2><p>Figma에서는 <code>Step Size</code>(4·3·2)와 <code>Current Step</code>(0부터 단계 수까지) 두 속성으로 고릅니다. 막대 색을 직접 바꾸지 않습니다.</p><div class="canvas"><div class="pb-grid">{grid}</div></div></section>
<section class="section"><h2>스펙</h2>{table(['항목', '값'], [['너비', '놓이는 곳의 너비를 채움'], ['여백', '없음 — 모바일 화면은 감싸는 프레임이 위 8 · 좌우 20 · 아래 20px, 웹은 Modal (Web) 안에서 좌우 24'], ['막대', '높이 4px, 끝이 둥근 모양, 사이 간격 4px, 너비는 똑같이 나눔'], ['지난·지금 단계', 'Blue 600'], ['남은 단계', 'Opacity 4']])}</section>
<section class="section"><h2>코드</h2>{code("""<div class="progress-bar" role="progressbar"
     aria-valuemin="0" aria-valuemax="4" aria-valuenow="1" aria-label="4단계 중 1단계">
  <ol class="progress-bar__track">
    <li class="progress-bar__step is-done"></li>
    <li class="progress-bar__step"></li>
    <li class="progress-bar__step"></li>
    <li class="progress-bar__step"></li>
  </ol>
</div>""")}<p class="note">단계 수는 <code>li</code> 개수로, 현재 단계는 <code>is-done</code>을 붙인 개수로 정합니다. <code>aria-valuenow</code>도 같이 바꿔 주세요.</p></section>
<section class="section"><h2>결정 기록</h2><div class="callouts">
  {callout('ok', '추가', '2026-10-27', 'Figma에 Current Step 속성을 추가했습니다. 전에는 사용 예시를 만들 때 막대 색을 하나씩 바꿔야 했고, 일부는 색 변수와 연결이 끊겨 있었습니다.')}
  {callout('wait', '유지', '2026-10-27', '남은 단계 색 Opacity 4는 흰 배경에서 거의 보이지 않지만(대비 약 1.1:1) 현재 색을 유지합니다.')}
  {callout('ok', '반영', '2026-10-27', 'Figma 이름 오타 "Progrees"를 "Progress"로, 예시 레이어 이름 "Component 5·6·7"을 용도 이름으로 고쳤습니다.')}
</div></section>'''
    return content

def fl_input(state='Default', label='회고 제목', value='', mx=10, help=None, area=False, live=False):
    cls = {'focus': ' is-focus', 'error': ' is-error', 'disabled': ' is-disabled'}.get(state, '')
    n = len(value)
    cnt = f'<span class="field__count">{f"<b>{n}</b>/{mx}" if n else f"0/{mx}"}</span>'
    dis = ' disabled' if state == 'disabled' else ''
    ph = '회고 설명을 적어 주세요' if area else '회고 제목을 적어 주세요'
    if area: ctl = f'<textarea class="field__input" rows="1" placeholder="{ph}" maxlength="{mx}" data-count{dis}>{value}</textarea>'
    else: ctl = f'<input class="field__input" type="text" placeholder="{ph}" maxlength="{mx}" value="{value}" data-count{dis}>'
    h = f'<p class="field__help">{help}</p>' if help else ''
    return f'<div class="field{" field--area" if area else ""}{cls}{"" if live else " fl-static"}"><label class="field__label">{label}</label><label class="field__box">{ctl}{cnt}</label>{h}</div>'

def fl_select(state='Default', text='회고 마감일을 선택해 주세요', live=False):
    cls = {'focus': ' is-focus', 'selected': ' is-selected', 'disabled': ' is-disabled'}.get(state, '')
    return f'<button type="button" class="select-field{cls}{"" if live else " fl-static"}"{" disabled" if state == "disabled" else ""}><span class="select-field__text">{text}</span>{icon("Icon/Assets/Calendar", "icon")}</button>'

def p_fields():
    st = [('Default', {}), ('Focus', {'state': 'focus'}), ('Typing', {'state': 'focus', 'value': '첫 회고'}), ('Typed', {'value': '첫 회고'}),
          ('Error', {'state': 'error', 'value': '첫 회고!', 'help': '*특수문자는 입력이 불가해요'}), ('OverTyping', {'state': 'error', 'value': '이번 주 회고 정리', 'mx': 10, 'help': '*최대 10자까지 입력이 가능해요'}),
          ('Disabled', {'state': 'disabled'})]
    def grid(area):
        cells = ''
        for name, kw in st:
            kw = dict(kw)
            if area and name == 'OverTyping': kw.update(value='이번 주에 잘한 점과 아쉬운 점 정리', mx=20, help='*최대 20자까지 입력이 가능해요')
            if area and 'mx' not in kw: kw['mx'] = 20
            cells += f'<div class="state fl-cell"><span class="state-label">{name}</span>{fl_input(area=area, label="회고 설명" if area else "회고 제목", **kw)}</div>'
        return f'<div class="fl-grid">{cells}</div>'
    sel = ''.join(f'<div class="state fl-cell"><span class="state-label">{n}</span>{fl_select(s, t)}</div>' for n, s, t in
                  [('Default', None, '회고 마감일을 선택해 주세요'), ('Focus · Pressed', 'focus', '회고 마감일을 선택해 주세요'), ('Selected', 'selected', '2026년 11월 3일 (화)'), ('Disabled', 'disabled', '회고 마감일을 선택해 주세요')])
    colors = [['Default', 'Gray 300', '안내 문구 Gray 500', '0/N · Gray 500'], ['Focus · Typing', 'Blue 600', 'Gray 900, 커서 Blue 600', '입력한 수 Blue 600'],
              ['Typed', 'Gray 300', 'Gray 900', '입력한 수 Blue 600'], ['Error · OverTyping', 'Blue 600', 'Gray 900 + 안내 문구 Red 500', '입력한 수 Blue 600'],
              ['Disabled', 'Gray 200', 'Gray 300', 'Gray 300']]
    spec = [['높이', 'Text Input·Select Field 53px, Text Area 74px부터 내용에 맞춰 늘어남'], ['여백', '위아래 16 · 좌우 14px, 모서리 12px, 테두리 1px'],
            ['라벨', '<a href="typography.html">Subtitle 14 SemiBold</a>, 입력창과 간격 8px'], ['입력 글자', '<a href="typography.html">Body 15 Medium</a>'],
            ['글자 수', '<a href="typography.html">Body 12 Medium</a>, Text Input은 오른쪽 옆, Text Area는 오른쪽 아래'], ['안내 문구', '<a href="typography.html">Body 14 Medium</a>, 입력창 아래 8px'],
            ['Select Field 아이콘', 'Calendar 20px · 기본 Gray 700, 포커스·선택 Gray 800, 비활성 Gray 300']]
    content = page_head('Components', 'Fields',
        '필드는 사용자가 글자를 입력하거나 정해진 값을 고르는 요소입니다. 한 줄로 짧게 받는 회고 제목은 Text Input, 여러 줄로 받는 회고 설명은 Text Area, 회고 마감일처럼 목록이나 달력에서 고르는 값은 Select Field를 씁니다.',
        status=('ok', '확정'), node='1-2301')
    content += f'''<section class="section"><h2>예시</h2><p>직접 입력해 보세요. 글자 수가 함께 올라갑니다.</p><div class="canvas"><div class="fl-demo">{fl_input(live=True)}{fl_input(label="회고 설명", mx=100, area=True, live=True)}<div class="field"><span class="field__label">회고 마감일</span>{fl_select(live=True)}</div></div></div></section>
<section class="section"><h2>Text Input</h2><div class="canvas">{grid(False)}</div></section>
<section class="section"><h2>Text Area</h2><p>입력한 내용에 맞춰 높이가 늘어납니다. 글자 수는 오른쪽 아래에 표시합니다.</p><div class="canvas">{grid(True)}</div></section>
<section class="section"><h2>Select Field</h2><p>누르면 달력이나 목록을 열어 값을 고릅니다. 고른 뒤에는 입력한 글자와 같은 Gray 900으로 표시합니다.</p><div class="canvas"><div class="fl-grid">{sel}</div></div></section>
<section class="section"><h2>전체 화면 작성 영역</h2><p>질문 제목 아래가 통째로 입력칸이 되는 회고 작성 화면은 테두리 없는 영역에 <a href="typography.html">Body 15 Medium Long</a>으로 씁니다. 이때 안내 문구는 <strong>Gray 400</strong>입니다. 넓은 영역에 Gray 500 안내 문구가 깔리면 이미 쓴 글처럼 보이기 때문입니다. 테두리가 있는 입력창의 안내 문구는 그대로 Gray 500입니다.</p></section>
<section class="section"><h2>상태</h2>{table(['상태', '테두리', '글자', '글자 수'], colors)}<p class="note">Error는 쓸 수 없는 글자(특수문자)를 넣었을 때, OverTyping은 최대 글자 수를 넘겼을 때입니다. 두 경우 모두 테두리는 포커스와 같은 Blue 600을 유지하고, 안내 문구만 빨간색으로 보여 줍니다.</p></section>
<section class="section"><h2>스펙</h2>{table(['항목', '값'], spec)}</section>
<section class="section"><h2>코드</h2>{code("""<link rel="stylesheet" href="css/fields.css">

<!-- Text Input -->
<div class="field">
  <label class="field__label" for="title">회고 제목</label>
  <label class="field__box">
    <input id="title" class="field__input" placeholder="회고 제목을 적어 주세요" maxlength="10">
    <span class="field__count"><b>4</b>/10</span>
  </label>
</div>

<!-- 오류: is-error + 안내 문구 -->
<div class="field is-error">
  …
  <p class="field__help">*특수문자는 입력이 불가해요</p>
</div>

<!-- Text Area -->
<div class="field field--area">…<textarea class="field__input" rows="1"></textarea>…</div>

<!-- Select Field (값을 고른 뒤 is-selected) -->
<button class="select-field is-selected">
  <span class="select-field__text">2026년 11월 3일 (화)</span>
  <span class="icon">…</span>
</button>""")}</section>
<section class="section"><h2>결정 기록</h2><div class="callouts">
  {callout('ok', '반영', '2026-10-27', 'Text Area의 Error와 OverTyping이 서로 바뀌어 있던 것을 Text Input 기준으로 맞췄습니다. Error는 특수문자, OverTyping은 글자 수 초과(N/N)입니다.')}
  {callout('ok', '반영', '2026-10-27', 'Text Input OverTyping 예시가 최대 10자인데 "최대 20자"였던 것을 "최대 10자", 10/10으로 고쳤습니다.')}
  {callout('ok', '반영', '2026-10-27', '입력한 글자색을 Gray 900으로 통일했습니다. Text Area는 Blue 900, Select Field는 Gray 800이었습니다.')}
  {callout('ok', '반영', '2026-10-27', 'Text Area의 커서를 "|" 글자 대신 막대로 그리고, 포커스·입력 중일 때만 보이게 했습니다. 기본 문구도 "Text|"에서 "Text"로 바꿨습니다.')}
  {callout('ok', '반영', '2026-10-27', 'Text Area 포커스·입력 중·오류 상태에 빠져 있던 흰 배경을 넣었습니다. 속성 이름 "Show label"을 "Show Label"로 맞추고, 안내 문구 하나에 텍스트 스타일을 연결했습니다.')}
  {callout('ok', '확정', '2026-10-27', '오류 상태 테두리는 약속대로 Blue 600을 유지합니다.')}
  {callout('wait', '유지', '2026-10-27', '비활성(Gray 300 글자, 대비 약 1.3:1)과 안내 문구(Gray 500, 대비 약 2.2:1) 색은 현재 값을 유지합니다.')}
</div></section>'''
    return content

def tb(label, sel=False, cls='tab', hover=False):
    return f'<button type="button" role="tab" class="{cls}{" is-hover" if hover else ""}" aria-selected="{"true" if sel else "false"}">{label}</button>'

def p_tabs():
    def text_tabs(labels, outlined=False, fixed=False, live=True, web=False, sel=0):
        items = ''.join(tb(l, i == sel) for i, l in enumerate(labels))
        return f'<div role="tablist" class="tabs{" tabs--sm" if web is True else ""}{" tabs--fixed" if fixed else ""}{" tabs--outlined" if outlined else ""}{" js-tablist" if live else " tb-static"}">{items}</div>'
    def box_tabs(labels, fixed=False, live=True):
        items = ''.join(tb(l, i == 0, 'box-tab') for i, l in enumerate(labels))
        return f'<div role="tablist" class="box-tabs{" box-tabs--fixed" if fixed else " box-tabs--scroll"}{" js-tablist" if live else " tb-static"}">{items}</div>'
    items = [['Text 탭(왼쪽 정렬)', tb('회고', True), tb('회고'), tb('회고', hover=True)],
             ['Text 탭(같은 너비)', f'<div class="tabs--fixed tb-one">{tb("회고", True)}</div>', f'<div class="tabs--fixed tb-one">{tb("회고")}</div>', f'<div class="tabs--fixed tb-one">{tb("회고", hover=True)}</div>'],
             ['Box 탭', tb('전체', True, 'box-tab'), tb('전체', False, 'box-tab'), tb('전체', False, 'box-tab', True)]]
    rows = ''.join(f'<div class="tb-name">{n}</div>' + ''.join(f'<div class="tb-cell tb-static">{c}</div>' for c in cs) for n, *cs in items)
    spec = [['Text 탭 Size 18', '높이 40 · 여백 0 · 탭 간격 8 · 탭 안 좌우 4px (모바일은 감싸는 프레임이 위 12 · 좌우 20)', '<a href="typography.html">Subtitle 18 SemiBold</a>', '밑줄 2px, 글자 너비만큼'],
            ['Text 탭(같은 너비)', '높이 44 · 좌우 20 · 칸을 똑같이 나눔 · 글자 위 7px', '<a href="typography.html">Title 18 Bold</a>', '밑줄 2px, 칸 너비 전체'],
            ['Text 탭 Size 14', '높이 40 · 여백 0 · 탭 간격 4 · 탭 안 좌우 4px · 글자 아래 10px', '<a href="typography.html">Subtitle 14 SemiBold</a>', '밑줄 2px, 글자 너비만큼'],
            ['Text 탭(밑줄 없음)', '높이 25(글자만큼) · 탭 간격 8 · 각 탭 Underline=Off', '<a href="typography.html">Subtitle 18 SemiBold</a>', '글자색만 Gray 900'],
            ['Box 탭', '탭 높이 38 · 안쪽 9/16px · 모서리 8px · 간격 8 · 묶음 여백 위 20 · 좌우 20 · 아래 16', '<a href="typography.html">Subtitle 14 SemiBold</a>', '선택 시 Gray 800 배경'],
            ['구분선(Outlined)', '아래 1px, Opacity 8', '', '']]
    colors = [['Text 탭', 'Gray 500', 'Gray 600', 'Gray 900 + 밑줄 Gray 900'], ['Box 탭', 'Gray 100 배경, Gray 800 글자', 'Gray 200 배경', 'Gray 800 배경, 흰 글자']]
    content = page_head('Components', 'Tabs',
        '탭은 같은 화면 안의 내용을 몇 갈래로 나눠 보여 주는 요소입니다. 밑줄로 선택을 표시하는 Text 탭은 화면의 주요 구분에, 칸 모양의 Box 탭은 목록을 거르는 보조 구분에 씁니다. 탭이 많아 화면을 넘치면 Scrollable로 옆으로 밀어서 봅니다.',
        status=('ok', '확정'), node='1-1374')
    content += f'''<section class="section"><h2>예시</h2><p>탭을 눌러 보세요. Box 탭은 옆으로 밀면 가려진 탭이 나오고, 더 볼 탭이 있는 쪽 가장자리만 흐려집니다.</p>
<div class="canvas"><div class="tb-demo">{text_tabs(['회고', '실행 목표', '분석'], outlined=True)}{text_tabs(['진행 중', '완료'], outlined=True, fixed=True)}{box_tabs(['전체', '이번 주', '지난주', '이번 달', '좋았던 점', '아쉬운 점', '다음 할 일'])}</div></div></section>
<section class="section"><h2>Text 탭</h2><p>왼쪽 정렬은 탭 이름 길이만큼 차지하고 2~4개까지 씁니다. 같은 너비는 칸을 똑같이 나누고 2~3개까지 씁니다. 아래 구분선은 필요할 때만 넣습니다(Outlined).</p>
<div class="canvas"><div class="tb-demo">{text_tabs(['회고', '실행 목표', '분석', '설정'])}{text_tabs(['회고', '실행 목표', '분석'], outlined=True)}{text_tabs(['진행 중', '완료', '보관'], fixed=True)}{text_tabs(['진행 중', '완료'], outlined=True, fixed=True)}</div></div></section>
<section class="section"><h2>크기 <span class="count">Size 18 · 14</span></h2><p>Text 탭은 모바일과 웹이 같은 컴포넌트입니다. 화면의 주요 구분에는 <strong>Size 18</strong>(탭 간격 8)을, 웹 패널 · 왼쪽 메뉴(LNB) 안에는 <strong>Size 14</strong>(탭 간격 4)를 씁니다. 높이는 40이고 여백이 없습니다. 모바일 화면에서는 감싸는 프레임이 위 12 · 좌우 20 여백을 줍니다.</p>
<div class="canvas"><div class="tb-demo">{text_tabs(['진행 중', '지난'], web=True)}{text_tabs(['전체', '개인', '팀'], web=True)}{text_tabs(['질문', '개별', '분석'], outlined=True, sel=2)}</div></div><p class="canvas-caption">Size 14: 실행목표 패널(진행 중 · 지난), LNB(전체 · 개인 · 팀). Size 18 + 구분선: 웹 회고 상세 패널 위(질문 · 개별 · 분석). Figma <code>Tabs/Text Tabs</code> · Size=18 · 14, 칸 수는 Show Tab 3 · 4, 구분선은 Show Divider, 이름과 선택은 각 탭(Text Tab Item)에서 바꿉니다.</p></section>
<section class="section"><h2>Segmented Control</h2><p>같은 내용을 보는 기준을 바꾸는 2~3칸 전환입니다. 예: 분석 결과의 개인 · 팀. 내용 영역 자체를 나누면 Text 탭을, 목록을 거르면 Box 탭을 씁니다.</p>
<div class="canvas canvas--center"><div class="bd-row"><div class="segmented" role="group"><button type="button" class="segmented__item" aria-pressed="false">개인</button><button type="button" class="segmented__item" aria-pressed="true">팀</button></div><div class="segmented" role="group"><button type="button" class="segmented__item" aria-pressed="true">전체</button><button type="button" class="segmented__item" aria-pressed="false">개인</button><button type="button" class="segmented__item" aria-pressed="false">팀</button></div></div></div>
{table(['항목', '값'], [['틀', 'Gray 100, 안쪽 4, 모서리 8'], ['칸', '위아래 6 · 좌우 12, 모서리 6, <a href="typography.html">Body 12 SemiBold</a> Gray 700 · Hover Gray 200 바탕'], ['선택', 'Gray 700 바탕 + 글자 Gray 100'], ['Figma', '<code>Segmented Control</code> · Item=2 · 3, 칸은 <code>Segmented Control/Item</code> · State · Label'], ['코드', '<code>.segmented &gt; .segmented__item[aria-pressed]</code>']])}</section>
<section class="section"><h2>밑줄 없는 Text 탭</h2><p>선택을 글자색만으로 표시하는 2개짜리 탭입니다. 높이는 글자만큼이고, Date Time Picker의 오전/오후처럼 작은 영역 안에서 씁니다.</p>
<div class="canvas"><div class="tb-demo"><div role="tablist" class="tabs tabs--plain js-tablist"><button type="button" role="tab" class="tab" aria-selected="true">오전</button><button type="button" role="tab" class="tab" aria-selected="false">오후</button></div></div></div></section>
<section class="section"><h2>Box 탭</h2><p>탭이 많으면 Scrollable, 2~3개면 같은 너비로 씁니다.</p>
<div class="canvas"><div class="tb-demo">{box_tabs(['전체', '이번 주', '지난주', '이번 달', '좋았던 점', '아쉬운 점'])}{box_tabs(['전체', '진행 중', '완료'], fixed=True)}{box_tabs(['혼자', '함께'], fixed=True)}</div></div></section>
<section class="section"><h2>상태</h2><div class="canvas"><div class="tb-grid"><div></div><div class="state-label">Selected</div><div class="state-label">Unselected</div><div class="state-label">Hover</div>{rows}</div></div>{table(['종류', '선택 안 됨', '호버', '선택'], colors)}<p class="note">호버는 선택 안 된 탭에만 적용합니다. 선택된 탭은 마우스를 올려도 그대로입니다.</p></section>
<section class="section"><h2>스펙</h2>{table(['종류', '크기', '글자', '선택 표시'], spec)}</section>
<section class="section"><h2>코드</h2>{code("""<link rel="stylesheet" href="css/tabs.css">

<!-- Text 탭 (같은 너비 + 구분선) -->
<div role="tablist" class="tabs tabs--fixed tabs--outlined">
  <button role="tab" class="tab" aria-selected="true">진행 중</button>
  <button role="tab" class="tab" aria-selected="false">완료</button>
</div>

<!-- Box 탭 (Scrollable) -->
<div role="tablist" class="box-tabs box-tabs--scroll">
  <button role="tab" class="box-tab" aria-selected="true">전체</button>
  <button role="tab" class="box-tab" aria-selected="false">이번 주</button>
  …
</div>

<script>
  // 더 볼 탭이 있는 쪽 가장자리만 흐리게
  document.querySelectorAll('.box-tabs--scroll').forEach(function (el) {
    function fog() {
      var max = el.scrollWidth - el.clientWidth;
      el.style.setProperty('--fog-l', el.scrollLeft > 1 ? '40px' : '0px');
      el.style.setProperty('--fog-r', el.scrollLeft < max - 1 ? '40px' : '0px');
    }
    el.addEventListener('scroll', fog, { passive: true }); fog();
  });
</script>""")}</section>
<section class="section"><h2>결정 기록</h2><div class="callouts">
  {callout('ok', '확정', '2026-10-27', '왼쪽 정렬 탭(Subtitle 18 SemiBold)과 같은 너비 탭(Title 18 Bold)의 글자 스타일 차이는 의도한 것입니다.')}
  {callout('ok', '반영', '2026-10-27', '같은 너비 탭은 선택되면 글자가 2px 올라갔는데, 선택 여부와 상관없이 같은 높이(위 7px)로 맞췄습니다. Figma 이름도 Sheet에서 Fixed로 바꿨습니다.')}
  {callout('ok', '반영', '2026-10-27', '같은 너비 탭의 글자를 행간 140%의 Title 18 Bold 스타일에 연결했습니다(외부 라이브러리 스타일은 150%). Popup 제목과 같은 스타일입니다.')}
  {callout('ok', '추가', '2026-10-27', '밑줄 없는 버전(Underline = Off)을 추가했습니다. Date Time Picker의 오전/오후가 이 버전을 씁니다.')}
  {callout('ok', '추가', '2026-10-27', '호버 상태를 추가했습니다. Text 탭은 글자 Gray 600, Box 탭은 배경 Gray 200입니다.')}
  {callout('ok', '반영', '2026-10-27', 'Box 탭 선택 색은 Gray 800으로 정했습니다. 선택 안 된 글자는 "Text/Disabled" 변수 대신 원본 Color 스타일 Gray 500에 연결했습니다.')}
  {callout('ok', '반영', '2026-10-27', 'Scrollable은 375px 안에서 잘리고, 더 볼 탭이 있는 쪽 가장자리를 흐리게 처리했습니다. 숨어 있던 "Component 10" 레이어는 지웠습니다.')}
</div></section>'''
    return content

def ctl(kind, checked=False, disabled=False, label=None, inter=None, live=True, name=None):
    cls = {'hover': ' is-hover', 'pressed': ' is-pressed'}.get(inter, '')
    attrs = (' checked' if checked else '') + (' disabled' if disabled else '') + (f' name="{name}"' if name else '')
    inp = f'<input class="control__input{cls}" type="{kind}"{attrs}>'
    st = '' if live else ' ct-static'
    if not label: return f'<label class="control control--bare{st}" aria-label="{kind}">{inp}</label>'
    txt, pos = label
    t = f'<span class="control__label">{txt}</span>'
    return f'<label class="control{st}">{t + inp if pos == "left" else inp + t}</label>'

def p_controls():
    qs = ['이번 주에 가장 잘한 일은?', '아쉬웠던 점은 무엇인가요?', '다음 주에 바꿔 볼 한 가지는?']
    left = ''.join(f'<li>{ctl("checkbox", i == 0, label=(q, "left"))}</li>' for i, q in enumerate(qs))
    right = ''.join(f'<li>{ctl("radio", i == 1, label=(t, "right"), name="ct-demo")}</li>' for i, t in enumerate(['혼자 회고', '팀 회고', '나중에 정할게요']))
    def grid(kind):
        head = '<div></div>' + ''.join(f'<div class="state-label">{h}</div>' for h in ['Checked', 'Unchecked', 'Disabled'])
        rows = ''
        for tname, lab in [('Default', None), ('Label Left', ('Label', 'left')), ('Label Right', ('Label', 'right'))]:
            for inter in [None, 'hover', 'pressed']:
                rows += f'<div class="ct-name">{tname}{" · " + inter.capitalize() if inter else ""}</div>'
                rows += f'<div>{ctl(kind, True, label=lab, inter=inter, live=False)}</div><div>{ctl(kind, False, label=lab, inter=inter, live=False)}</div>'
                rows += (f'<div class="ct-dis">{ctl(kind, True, True, label=lab, live=False)}{ctl(kind, False, True, label=lab, live=False)}</div>' if not inter else '<div></div>')
        return f'<div class="ct-grid">{head}{rows}</div>'
    colors = [['선택', 'Blue 600 배경 + 흰 체크(체크박스) / 흰 점 8px(라디오)', 'Blue 700', 'Blue 800'],
              ['선택 안 됨', '흰 배경 + Gray 400 테두리', 'Gray 500 테두리', 'Gray 600 테두리'],
              ['비활성', '선택: Blue 400 / 선택 안 됨: Gray 100 배경 + Gray 200 테두리', '-', '-']]
    spec = [['크기', '24px 칸 안에 20px 모양 · 체크박스 모서리 4px · 라디오 원형'], ['라벨형', '안쪽 여백 4px · 라벨과 간격 8px · 모서리 8px · 흰 배경 · 너비는 글자에 맞춤'],
            ['라벨 글자', '<a href="typography.html">Body 15 Medium</a> Gray 900 · 선택 안 된 비활성만 Gray 400'], ['누르는 영역', '라벨까지 포함한 전체']]
    content = page_head('Components', 'Controls',
        '체크박스와 라디오는 목록에서 항목을 고르는 요소입니다. 여러 개를 고를 수 있으면 체크박스, 하나만 고를 때는 라디오를 씁니다. 회고 질문 선택 리스트처럼 항목 오른쪽 끝에 둘 때는 Label Left를, 일반 목록에서는 Label Right를 씁니다.',
        status=('ok', '확정'), node='1-2462')
    content += f'''<section class="section"><h2>예시</h2><p>라벨을 눌러도 선택됩니다.</p><div class="canvas"><div class="ct-demo"><div><span class="state-label">회고 질문 고르기 · 체크박스 Label Left</span><ul class="ct-list ct-list--end">{left}</ul></div><div><span class="state-label">회고 방식 · 라디오 Label Right</span><ul class="ct-list">{right}</ul></div></div></div></section>
<section class="section"><h2>Checkbox</h2><div class="canvas">{grid("checkbox")}</div></section>
<section class="section"><h2>Radio</h2><p>체크박스와 같은 크기, 색, 속성으로 만들었습니다. 네모 대신 원, 체크 대신 흰 점을 씁니다.</p><div class="canvas">{grid("radio")}</div></section>
<section class="section"><h2>상태</h2>{table(['상태', '기본', '호버', '눌림'], colors)}<p class="note">호버는 한 단계, 눌림은 두 단계 진해지는 버튼 규칙을 따릅니다.</p></section>
<section class="section"><h2>스펙</h2>{table(['항목', '값'], spec)}</section>
<section class="section"><h2>코드</h2>{code("""<link rel="stylesheet" href="css/controls.css">

<!-- Label Left (라벨이 왼쪽, 박스가 오른쪽) -->
<label class="control">
  <span class="control__label">이번 주에 가장 잘한 일은?</span>
  <input class="control__input" type="checkbox" checked>
</label>

<!-- Label Right (박스가 왼쪽) -->
<label class="control">
  <input class="control__input" type="radio" name="mode">
  <span class="control__label">팀 회고</span>
</label>""")}<p class="note">라벨 위치는 마크업 순서로 정합니다. 실제 입력 요소를 써서 키보드(스페이스, 화살표)와 화면 읽기 프로그램에서도 동작합니다.</p></section>
<section class="section"><h2>결정 기록</h2><div class="callouts">
  {callout('ok', '추가', '2026-10-27', '라디오를 체크박스 형식(Type · State · Disable · Interaction)에 맞춰 새로 만들었습니다.')}
  {callout('ok', '추가', '2026-10-27', '박스가 왼쪽에 오는 Label Right를 추가했습니다. 기존 With Label은 Label Left로 이름을 바꿨습니다.')}
  {callout('ok', '추가', '2026-10-27', '호버·눌림 상태를 추가했습니다. 선택은 Blue 700 → 800, 선택 안 됨은 테두리 Gray 500 → 600입니다.')}
  {callout('ok', '반영', '2026-10-27', '라벨형의 선택 안 된 박스를 Default와 같은 Gray 400 테두리, 흰 배경으로 맞췄습니다. 라벨 너비는 글자 길이에 맞춰 늘어납니다.')}
  {callout('ok', '확정', '2026-10-27', '선택된 비활성의 라벨이 Gray 900으로 남는 것은 의도한 것입니다.')}
  {callout('ok', '반영', '2026-10-27', '쓰지 않던 Disabled(on/off) 속성과, 다른 데서 복사된 설명 "TextButton : 기본 텍스트 버튼"을 지웠습니다.')}
</div></section>'''
    return content

def p_scrollbar():
    lines = ''.join(f'<p>회고 질문 {i}. 이번 주에 있었던 일을 돌아봅니다.</p>' for i in range(1, 21))
    content = page_head('Components', 'Scroll Bar',
        '스크롤 바는 화면이나 목록의 내용이 넘칠 때 지금 위치를 보여 주는 요소입니다. 평소에는 옅게 보이다가 마우스를 올리면 한 단계, 끌고 있으면 두 단계 진해집니다. 막대 길이는 내용 길이에 따라 정해집니다.',
        status=('ok', '확정'), node='214-9561')
    states = ''.join(f'<div class="state"><span class="state-label">{n}</span><div class="sb-spec"><span style="background:rgb(6 8 12 / {a})"></span></div></div>' for n, a in [('Default', 0.22), ('Hover', 0.32), ('Pressed', 0.48)])
    content += f'''<section class="section"><h2>예시</h2><p>목록에 마우스를 올리면 스크롤 바가 나타납니다. 막대에 올리면 한 단계, 끌면 두 단계 진해집니다.</p><div class="canvas"><div class="scroll-area sb-demo">{lines}</div></div><p class="canvas-caption">Chrome, Safari, Edge에서 디자인대로 보입니다. Firefox는 브라우저 기본 얇은 막대에 기본 색만 적용됩니다.</p></section>
<section class="section"><h2>상태</h2><div class="canvas"><div class="states">{states}</div></div>{table(['상태', '막대 색'], [['Default', 'Opacity 22'], ['Hover', 'Opacity 32'], ['Pressed', 'Opacity 48']])}</section>
<section class="section"><h2>스펙</h2>{table(['항목', '값'], [['막대', '너비 4px, 끝이 둥근 모양(99px)'], ['여백', '좌우 3px · 위아래 5px (전체 너비 10px)'], ['트랙', '보이지 않음'], ['나타나는 때', '목록에 마우스를 올렸거나 스크롤하는 동안. 그 밖에는 숨김'], ['막대 길이', '내용 길이에 따라 자동. Figma에서는 트랙의 1/3로 그려 둠']])}</section>
<section class="section"><h2>코드</h2>{code("""<link rel="stylesheet" href="css/controls.css">

<div class="scroll-area" style="max-height: 320px">
  …긴 목록…
</div>

<script>
  // 마우스를 올렸을 때와 스크롤하는 동안 스크롤 바 표시
  document.querySelectorAll('.scroll-area').forEach(function (el) {
    var t;
    el.addEventListener('mouseenter', function () { el.classList.add('is-hover'); });
    el.addEventListener('mouseleave', function () { el.classList.remove('is-hover'); });
    el.addEventListener('scroll', function () {
      el.classList.add('is-scrolling'); clearTimeout(t);
      t = setTimeout(function () { el.classList.remove('is-scrolling'); }, 800);
    }, { passive: true });
  });
</script>""")}</section>
<section class="section"><h2>결정 기록</h2><div class="callouts">
  {callout('ok', '반영', '2026-10-27', '성격이 달라 Controls 보드에서 분리해 별도 보드로 옮겼습니다.')}
  {callout('ok', '확정', '2026-10-27', '막대 길이는 Figma에서는 1/3로 고정해 그리지만, 실제로는 내용 길이에 따라 정해집니다.')}
</div></section>'''
    return content

def p_lists():
    drawer = icon('Icon/Assets/Drawer', 'icon'); close = icon('Icon/Assets/Close', 'icon')
    qs = ['이번 주에 가장 잘한 일은?', '아쉬웠던 점은 무엇인가요?', '다음 주에 바꿔 볼 한 가지는?', '팀에게 고마웠던 순간은?']
    checks = ''.join(f'<li><label class="list-check"><span class="list-check__text">{q}</span><input class="control__input" type="checkbox"{" checked" if i == 1 else ""}></label></li>' for i, q in enumerate(qs))
    cards = ''.join(f'<li class="list-card"><span class="num-badge">{i + 1}</span><span class="list-card__text">{q}</span><button type="button" class="list-card__action list-card__action--reorder" aria-label="순서 바꾸기">{drawer}</button></li>' for i, q in enumerate(qs[:3]))
    dels = ''.join(f'<li class="list-card"><span class="num-badge">{i + 1}</span><span class="list-card__text">{q}</span><button type="button" class="list-card__action list-card__action--delete" aria-label="질문 삭제">{close}</button></li>' for i, q in enumerate(qs[:2]))
    content = page_head('Components', 'Lists', '리스트는 같은 종류의 항목을 세로로 나열하는 요소입니다. 항목을 고를 때는 체크박스 리스트를, 순서를 바꾸거나 지울 때는 아이콘 리스트를, 설정처럼 다른 화면으로 넘어가는 목록에는 메뉴 아이템을 씁니다.', status=('ok', '확정'), node='1-2532')
    content += f'''<section class="section"><h2>체크박스 리스트</h2><p>회고에 넣을 질문을 고를 때 씁니다. 줄 어디를 눌러도 선택됩니다.</p><div class="canvas canvas--sunk ls-wrap"><ul class="list">{checks}</ul></div>
{table(['항목', '값'], [['높이', '58px, 좌우 여백 20px, 흰 배경'], ['글자', '<a href="typography.html">Body 15 Medium</a> Gray 900'], ['체크박스', '<a href="controls.html">Controls</a> 체크박스(Default) 인스턴스']])}</section>
<section class="section"><h2>메뉴 아이템</h2><p>설정 화면처럼 누르면 다른 화면으로 가거나 값을 보여 주는 한 줄 목록입니다. 흰 카드 안에 쌓고, 카드 위에 그룹 제목을 둘 수 있습니다.</p><div class="canvas canvas--sunk ls-wrap"><div class="menu-card"><p class="menu-card__title">버전</p><a class="menu-row" href="#">공지사항{icon('Icon/Assets/Chevron-Right', 'icon')}</a><div class="menu-row menu-row--value">현재 버전<span class="menu-row__value">1.0.0</span></div><button type="button" class="menu-row">로그아웃</button></div></div>
{table(['항목', '값'], [['한 줄', '335 × 48px, 좌 20 · 우 16px(Value는 20)'], ['글자', '<a href="typography.html">Body 16 Medium</a> Gray 900'], ['Right = Chevron', '다른 화면으로 이동. <a href="iconography.html">Chevron-Right</a> 16px Gray 800'], ['Right = Value', '정보만 보여 줌. <a href="typography.html">Body 14 Medium</a> Gray 600 (예: 현재 버전 1.0.0)'], ['Right = None', '누르면 바로 실행 (예: 로그아웃)'], ['카드', '흰 배경, 모서리 12, <a href="elevation.html">Shadow 100</a>, 위아래 12px, 카드 사이 8px'], ['그룹 제목', '<a href="typography.html">Subtitle 14 SemiBold</a> Gray 600, 좌우 20 · 위아래 8px'], ['Figma', '<code>List/Menu Item</code> · 속성 Label · Value(텍스트), Right']])}</section>
<section class="section"><h2>아이콘 리스트</h2><p>고른 질문의 순서를 바꾸거나(Reorder) 지울 때(Delete) 씁니다. 바꿀 수 없는 고정 질문(사전 질문)은 Action=None · Marker=Star로 둡니다. 카드 사이 간격은 15px입니다.</p><div class="canvas ls-cols"><div><span class="state-label">Action = Reorder</span><ol class="list list--cards">{cards}</ol></div><div><span class="state-label">Action = Delete</span><ol class="list list--cards">{dels}</ol></div><div><span class="state-label">Action = None · Marker = Star</span><ul class="list list--cards"><li class="list-card list-card--fixed"><span class="num-badge num-badge--star">★</span><span class="list-card__text">진행상황에 대해 얼마나 만족하나요?</span></li></ul></div></div>
{table(['항목', '값'], [['카드', '안쪽 여백 15/12px, 간격 15px, 모서리 8px, Gray 100 배경'], ['숫자 동그라미', '20px, 모서리 30, Gray 800 배경, 흰 글자 <a href="typography.html">Caption 10 Bold</a>'], ['글자', '<a href="typography.html">Body 14 Medium</a> Gray 900'], ['순서 변경', '<a href="iconography.html">Drawer</a> 아이콘 18px, Gray 400'], ['삭제', '18px 빨간 네모(Red 500, 모서리 <a href="radius.html">Radius 4</a>) + 흰 <a href="iconography.html">Close</a> 아이콘'], ['고정(None · Star)', '★ 동그라미 Gray 700 · 글자 Gray 700, 오른쪽 아이콘 없음'], ['Figma', '<code>List/Icon List</code> · Action(Reorder · Delete · None) · Marker(Number · Star) · Number(Marker=Number일 때만, Star는 ★ 고정) · Text']])}</section>
<section class="section"><h2>코드</h2>{code("""<link rel="stylesheet" href="css/lists.css">

<!-- 체크박스 리스트 -->
<ul class="list">
  <li><label class="list-check">
    <span class="list-check__text">이번 주에 가장 잘한 일은?</span>
    <input class="control__input" type="checkbox">
  </label></li>
</ul>

<!-- 아이콘 리스트 -->
<ol class="list list--cards">
  <li class="list-card">
    <span class="num-badge">1</span>
    <span class="list-card__text">이번 주에 가장 잘한 일은?</span>
    <button class="list-card__action list-card__action--reorder" aria-label="순서 바꾸기">…Drawer…</button>
  </li>
</ol>""")}</section>
<section class="section"><h2>결정 기록</h2><div class="callouts">
  {callout('ok', '반영', '2026-10-27', '체크박스 리스트 두 벌을 하나로 합쳤고, 직접 그린 네모 대신 Controls 체크박스 인스턴스를 씁니다. 세트 이름은 List/Checkbox List, 속성은 State(Unchecked·Checked)입니다.')}
  {callout('ok', '반영', '2026-10-27', '아이콘 리스트는 List/Icon List 하나로 합치고 속성 Action(Reorder·Delete)을 만들었습니다. 배경은 팔레트 밖 #F6F8FA에서 Gray 100으로 바꿨습니다.')}
  {callout('ok', '반영', '2026-10-27', '순서 변경 아이콘은 기존 Drawer 아이콘을, 삭제는 빨간 네모와 Close 아이콘을 조합해 씁니다.')}
  {callout('ok', '반영', '2026-10-27', '숫자 동그라미 모서리를 30으로 맞추고, 글자에 Caption 10 Bold 스타일을 연결했습니다.')}
</div></section>'''
    return content

def p_accordion():
    chev = lambda n: icon('Icon/Assets/Chevron-' + n, 'icon')
    items = ['이번 주에 가장 잘한 일은?', '아쉬웠던 점은 무엇인가요?', '계속 유지하고 싶은 것은?', '다음 주에 바꿔 볼 한 가지는?', '팀에게 하고 싶은 말은?']
    idx_items = ''.join(f'<li><button type="button" class="acc-index__item"{" aria-current=\"true\"" if i == 2 else ""}><span>{q}</span>{chev("Right")}</button></li>' for i, q in enumerate(items))
    accs = ''.join(f'<div class="acc{" is-open" if i == 0 else ""}"><button type="button" class="acc__head" aria-expanded="{"true" if i == 0 else "false"}"><span class="num-badge">{i + 1}</span><span class="acc__title">{q}</span><span class="icon icon-down">{bare(mono(I["Icon/Assets/Chevron-Down"]))}</span><span class="icon icon-up">{bare(mono(I["Icon/Assets/Chevron-Up"]))}</span></button><div class="acc__body">{a}</div></div>'
                   for i, (q, a) in enumerate([('이번 주에 가장 잘한 일은?', '매일 아침 15분씩 회고 노트를 썼어요.'), ('아쉬웠던 점은 무엇인가요?', '회의가 길어져 집중 시간이 부족했어요.'), ('다음 주에 바꿔 볼 한 가지는?', '회의는 30분 안에 끝내기로 했어요.')]))
    states = ''.join(f'<div class="state"><span class="state-label">{n}</span><button type="button" class="acc-title{c} ac-static">질문 목록{chev("Down")}</button></div>' for n, c in [('Default', ''), ('Hover', ' is-hover'), ('Pressed', ' is-pressed')])
    item_states = ''.join(f'<div class="state"><span class="state-label">{n}</span><button type="button" class="acc-index__item{c} ac-static" style="width:240px"><span>질문</span>{chev("Right")}</button></div>' for n, c in [('Default', ''), ('Hover', ' is-hover'), ('Pressed', ' is-pressed'), ('Selected', ' is-selected')])
    content = page_head('Components', 'Accordion', '아코디언은 내용을 접어 두었다가 필요할 때 펼쳐 보는 요소입니다. 질문 목록 사이를 이동할 때는 Index를, 질문마다 내용을 보여 줄 때는 Contents를 씁니다.', status=('ok', '확정'), node='1-2532')
    content += f'''<section class="section"><h2>Index</h2><p>화면 위쪽의 버튼(Index Title)을 누르면 질문 목록(Index)이 열리고, 지금 질문은 Blue 200으로 표시합니다.</p>
<div class="canvas ac-wrap"><div class="ac-index-demo"><button type="button" class="acc-title js-idx">질문 목록{chev("Down")}</button><div class="acc-index" hidden><div class="acc-index__header">질문 목록{chev("Up")}</div><ul class="acc-index__list">{idx_items}</ul></div></div></div>
<div class="canvas"><div class="states">{states}</div><div class="states" style="margin-top:20px">{item_states}</div></div>
{table(['부분', '값'], [['Index Title', '140×40, 모서리 12 · Gray 100 → 200 → 300 · 글자 <a href="typography.html">Subtitle 16 SemiBold</a> Gray 700 · 아이콘 Gray 600'], ['Index', '너비 335, 모서리 12, Gray 100 · 머리글 40px Gray 900'], ['Index Item', '높이 46 · 좌우 28px · 간격 16 · <a href="typography.html">Body 14 Medium</a> · 기본 → Gray 200 → Gray 300 / 선택 Blue 200']])}</section>
<section class="section"><h2>Contents</h2><p>질문을 누르면 답이 펼쳐집니다. 다시 누르면 접힙니다.</p><div class="canvas ac-wrap"><div class="ac-stack">{accs}</div></div>
{table(['항목', '값'], [['크기', '너비 335 · 안쪽 여백 14/20px · 모서리 8'], ['배경', 'Gray 100 → 호버 Gray 200 → 눌림 Gray 300'], ['제목', '숫자 동그라미(모서리 30, <a href="typography.html">Body 12 SemiBold</a>) + <a href="typography.html">Subtitle 16 SemiBold</a> Gray 900 + 화살표 Gray 700'], ['펼친 내용', 'Gray 400 구분선 아래 <a href="typography.html">Body 14 Medium</a> Gray 700, 간격 12px']])}</section>
<section class="section"><h2>Section (웹)</h2><p>웹 왼쪽 열에서 한 영역을 통째로 접고 펼칩니다. 회고 작성 패널이 열려 실행목표 패널 자리가 없을 때 실행목표를 여기에 접어 둡니다. 제목 줄을 누르면 펼쳐집니다.</p>
<div class="canvas canvas--sunk canvas--center"><div class="sa-demo"><div class="section-accordion"><button type="button" class="section-accordion__head" aria-expanded="false" onclick="this.parentNode.classList.toggle('is-open');this.setAttribute('aria-expanded',this.parentNode.classList.contains('is-open'))">실행목표{chev("Down")}</button><div class="section-accordion__body"><div role="tablist" class="tabs tabs--sm"><button type="button" role="tab" class="tab" aria-selected="true">진행 중</button><button type="button" role="tab" class="tab" aria-selected="false">지난</button></div><div class="goal-card"><div class="goal-card__head"><p class="goal-card__title">스프린트 1회차 이후 회고</p></div><div class="goal-card__body"><ul class="goal-card__list"><li>긴 회의시간 줄이기</li><li>회의 후 내용 꼭 기록해두기</li></ul></div></div></div></div></div></div>
{table(['항목', '값'], [['크기', '너비 296, 위아래 8 · 좌우 12, 모서리 8, 흰 바탕'], ['제목 줄', '<a href="typography.html">Title 14 Bold</a> Gray 900 + 화살표 16(접힘 아래 · 펼침 위)'], ['펼친 내용', '위 구분선 Gray 100 · 위 6, 사이 24: <a href="tabs.html">웹 Text 탭</a> + <a href="cards.html">Card/Goal (Web)</a> 목록'], ['Figma', '<code>Accordion/Section (Web)</code> · State=Collapsed · Expanded, Title']])}</section>
<section class="section"><h2>코드</h2>{code("""<link rel="stylesheet" href="css/lists.css">

<div class="acc is-open">
  <button class="acc__head" aria-expanded="true">
    <span class="num-badge">1</span>
    <span class="acc__title">이번 주에 가장 잘한 일은?</span>
    <span class="icon icon-down">…</span><span class="icon icon-up">…</span>
  </button>
  <div class="acc__body">매일 아침 15분씩 회고 노트를 썼어요.</div>
</div>

<!-- Index: 지금 항목은 aria-current="true" -->
<button class="acc-index__item" aria-current="true"><span>질문</span>…</button>""")}</section>
<section class="section"><h2>결정 기록</h2><div class="callouts">
  {callout('ok', '반영', '2026-10-27', 'Index의 한 줄을 Accordion/Index Item 컴포넌트로 분리하고 Default·Hover·Pressed·Selected 상태를 줬습니다. 줄 사이 간격은 16px로 통일했습니다.')}
  {callout('ok', '반영', '2026-10-27', '상태 이름을 Pressed·Selected로 통일했습니다(Press, Select, State2~4 정리).')}
  {callout('ok', '반영', '2026-10-27', 'Position 예시를 실제 컴포넌트 인스턴스로 다시 만들었습니다. 팔레트 밖 색과 "Tittle" 오타, 화면 밖 버튼을 정리했습니다.')}
</div></section>'''
    return content


def ficon(n): return icon('Icon/Assets/' + n, 'icon')
TIP_TXT = '툴팁 내 자세한 내용을 작성해주세요'
def toast_html(kind='text', msg='Text'):
    ic = {'text': '', 'info': ficon('Check_Filled'), 'caution': ficon('Caution_Filled')}[kind]
    mod = '' if kind == 'text' else f' toast--{kind}'
    return f'<div class="toast{mod}" role="status">{ic}{msg}</div>'

def p_toast():
    types = ''.join(f'<div class="state"><span class="state-label">Type = {n}</span><div style="width:335px">{toast_html(k)}</div></div>' for n, k in [('Text', 'text'), ('Info', 'info'), ('Caution', 'caution')])
    tpls = (f'<template id="tt-text">{toast_html("text", "회고를 저장했어요")}</template>'
            f'<template id="tt-info">{toast_html("info", "실행 목표를 추가했어요")}</template>'
            f'<template id="tt-caution">{toast_html("caution", "인터넷 연결을 확인해 주세요")}</template>')
    demo = (f'<div class="canvas canvas--sunk fb-demo"><div class="fb-phone"><div class="fb-host" id="toast-host"></div></div>'
            f'<div class="fb-btns"><button type="button" class="btn btn--secondary btn--sm" data-show-toast="toast-host" data-toast-tpl="tt-text">Text</button>'
            f'<button type="button" class="btn btn--secondary btn--sm" data-show-toast="toast-host" data-toast-tpl="tt-info">Info</button>'
            f'<button type="button" class="btn btn--secondary btn--sm" data-show-toast="toast-host" data-toast-tpl="tt-caution">Caution</button></div>{tpls}</div>')
    content = page_head('Components', 'Toast', '토스트는 사용자가 한 행동의 결과를 잠깐 알려 주고 사라지는 메시지입니다. 버튼 같은 다른 조치는 넣지 않고, 3초가 지나면 저절로 사라집니다.', status=('ok', '확정'), node='1-4875')
    content += f'''<section class="section"><h2>종류</h2><p>알림의 성격에 따라 아이콘을 붙입니다. 완료처럼 긍정적인 결과에는 Info, 실패나 주의가 필요한 결과에는 Caution을 씁니다.</p><div class="canvas canvas--sunk"><div class="states">{types}</div></div>
{table(['항목', '값'], [['크기', '너비 335 · 최소 높이 58 · 안쪽 여백 18/20px · 모서리 12'], ['배경', 'Opacity 86 (검정 86%)'], ['글자', '<a href="typography.html">Body 16 Medium</a> 흰색'], ['아이콘', '22px, 글자와 간격 8 · Info: Check_Filled Blue 600 · Caution: Caution_Filled Red 500'], ['시간', '3초 동안 보인 뒤 사라짐']])}</section>
<section class="section"><h2>예시</h2><p>버튼을 누르면 화면 아래에 토스트가 떴다가 3초 뒤 사라집니다.</p>{demo}</section>
<section class="section"><h2>위치</h2><p>화면 위쪽이나 아래쪽에 띄우고, 다른 UI와 콘텐츠보다 앞에 놓아 가려지지 않게 합니다.</p>
{table(['경우', '위치'], [['Top', '상태 표시줄 아래 20px'], ['Bottom', '홈 인디케이터 위 18px'], ['Bottom with CTA', '아래쪽 버튼 위 18px'], ['Bottom with Keyboard', '키보드 위 18px']])}</section>
<section class="section"><h2>코드</h2>{code("""<link rel="stylesheet" href="css/feedback.css">

<div class="toast">회고를 저장했어요</div>
<div class="toast toast--info"><span class="icon">…Check_Filled…</span>실행 목표를 추가했어요</div>
<div class="toast toast--caution"><span class="icon">…Caution_Filled…</span>인터넷 연결을 확인해 주세요</div>

<!-- 띄우기: .toast-host 안에 넣고 .is-shown을 붙였다가 3초 뒤 뗍니다 -->
<div class="toast-host"><div class="toast is-shown">…</div></div>""")}</section>
<section class="section"><h2>결정 기록</h2><div class="callouts">
  {callout('ok', '반영', '2026-10-27', 'Caution 아이콘을 Gray 900에서 Red 400으로 바꿨습니다. 어두운 배경에서 거의 보이지 않았습니다.')}
  {callout('ok', '반영', '2026-10-27', '속성 이름을 Type = Text·Info·Caution으로 정리하고, Text에 숨어 있던 아이콘을 지웠습니다.')}
  {callout('ok', '반영', '2026-10-27', '사라지는 시간을 3초로 정해 설명에 적었습니다. 사용 예시는 실제 Toast와 Button 컴포넌트로 바꿨습니다.')}
</div></section>'''
    return content

def p_tooltip():
    arrows = [('Bottom-Left', 'bottom-left'), ('Bottom-Center', 'bottom-center'), ('Bottom-Right', 'bottom-right'), ('Top-Left', 'top-left'), ('Top-Right', 'top-right')]
    fn = ''.join(f'<div class="state"><span class="state-label">{n} · {gn}</span><div class="tooltip tooltip--{c}{g}">{TIP_TXT}</div></div>' for n, c in arrows for gn, g in [('Blue', ''), ('Gray', ' tooltip--gray')])
    hover = (f'<div class="canvas fb-hover"><span class="tooltip-anchor"><button type="button" class="fb-target" aria-describedby="hv1">{ficon("Info")}</button>'
             f'<span class="tooltip tooltip--hover" role="tooltip" id="hv1">질문을 고르면 회고에 추가돼요</span></span><span class="fb-hint">아이콘에 마우스를 올려 보세요</span></div>')
    content = page_head('Components', 'Tooltip', '툴팁은 기능이나 해야 할 일을 짧게 설명하는 말풍선입니다. 무엇을 가리키는지, 언제 보이는지에 따라 Function, Hover, Guide 세 가지를 씁니다.', status=('ok', '확정'), node='1-4875')
    content += f'''<section class="section"><h2>Function Tooltip</h2><p>화면의 기능을 설명합니다. 화살표로 대상을 가리키며, 가리킨 영역을 누르거나 다른 화면으로 이동할 때까지 계속 보입니다. 바탕은 Blue와 Gray 두 가지입니다.</p><div class="canvas"><div class="states fb-grid">{fn}</div></div>
{table(['항목', '값'], [['크기', '안쪽 여백 10/14px · 모서리 8'], ['색', 'Color = Blue: Blue 600 · Color = Gray: Gray 900 · 글자 흰색'], ['글자', '<a href="typography.html">Body 12 SemiBold</a>'], ['화살표', '17×12 삼각형, 말풍선과 4px 겹침 · 왼쪽·오른쪽은 가장자리에서 16px, Center는 가운데'], ['사라지는 때', '가리킨 영역을 누르거나 다른 화면으로 이동할 때(시간이 지나도 사라지지 않음)']])}</section>
<section class="section"><h2>Hover Tooltip</h2><p>마우스를 올렸을 때만 보이는 짧은 설명입니다. 대상의 왼쪽 끝에 맞춰 8px 위에 띄우고, 마우스가 벗어나면 바로 사라집니다. 화살표 없이 Gray 900 바탕으로 표시합니다.</p>{hover}
{table(['항목', '값'], [['위치', '대상 위 8px, 왼쪽 끝 맞춤'], ['크기', '안쪽 여백 8/12px · 모서리 8'], ['색', 'Gray 900 바탕, 흰 글자 <a href="typography.html">Body 12 SemiBold</a>'], ['보이는 때', '마우스를 올렸을 때, 키보드로 포커스했을 때']])}</section>
<section class="section"><h2>Guide Tooltip</h2><p>화면에서 해야 할 일을 안내합니다. 화면에 고정되어 있고 저절로 사라지지 않습니다.</p><div class="canvas canvas--sunk"><div style="width:335px;max-width:100%"><div class="guide-tip"><p class="guide-tip__label">TIP</p><p class="guide-tip__text">회고 설명 또는 진행 목표에 대해 적어도 좋아요 :)</p></div></div></div>
{table(['항목', '값'], [['크기', '너비 335 · 안쪽 여백 14/18px · 모서리 8 · 줄 간격 4'], ['색', 'Blue 100 바탕, Blue 600 글자'], ['글자', '라벨 <a href="typography.html">Body 12 SemiBold</a> · 내용 <a href="typography.html">Body 12 Medium</a>']])}</section>
<section class="section"><h2>Info Banner</h2><p>화면이나 모달 위쪽에서 사용법을 한 줄로 알려 주는 회색 안내입니다. 강조해야 하는 팁은 Guide Tooltip(파랑)을 씁니다.</p><div class="canvas canvas--center"><div class="info-banner" style="width:472px;max-width:100%">{icon("Icon/Assets/Info_Filled", "icon")}카드를 클릭하면 자세한 내용을 확인할 수 있어요</div></div>{table(['항목', '값'], [['틀', 'Gray 200 바탕, 모서리 8, 위아래 8 · 좌우 12, 사이 8, 너비는 놓이는 곳을 채움'], ['글자', '<a href="iconography.html">Info_Filled</a> 아이콘 18 + <a href="typography.html">Body 12 Medium</a> Gray 600'], ['Figma', '<code>Info Banner</code> · Message · Icon(교체)'], ['코드', '<code>.info-banner</code>']])}</section>
<section class="section"><h2>코드</h2>{code("""<link rel="stylesheet" href="css/feedback.css">

<!-- Function: 화살표 위치 + 색. 가리킨 영역을 누르거나 화면을 이동하면 지웁니다 -->
<div class="tooltip tooltip--bottom-left">설명</div>
<div class="tooltip tooltip--top-right tooltip--gray">설명</div>

<!-- Hover: 대상을 .tooltip-anchor로 감쌉니다 -->
<span class="tooltip-anchor">
  <button aria-describedby="tip1">…</button>
  <span class="tooltip tooltip--hover" role="tooltip" id="tip1">설명</span>
</span>

<!-- Guide -->
<div class="guide-tip"><p class="guide-tip__label">TIP</p><p class="guide-tip__text">안내</p></div>""")}</section>
<section class="section"><h2>결정 기록</h2><div class="callouts">
  {callout('ok', '반영', '2026-10-27', 'Function Tooltip에 Color 속성을 만들어 Gray 900 버전을 추가했습니다. 따로 떨어져 있던 가운데 화살표 툴팁은 Arrow = Bottom-Center로 묶었습니다.')}
  {callout('ok', '반영', '2026-10-27', '화살표 없는 툴팁은 의도한 것으로 확정하고 Hover Tooltip이라는 별도 항목으로 정리했습니다. 위치를 Figma 예시로 남겼습니다.')}
  {callout('ok', '반영', '2026-10-27', 'Hover Tooltip은 대상의 왼쪽 끝에 맞춰 8px 위에 띄우도록 바꿨습니다(이전: 8px 아래).')}
  {callout('ok', '반영', '2026-10-27', 'Function Tooltip은 3초 뒤 사라지지 않고, 가리킨 영역을 누르거나 다른 화면으로 이동할 때까지 표시하도록 설명을 고쳤습니다.')}
  {callout('ok', '반영', '2026-10-27', '화살표 가로 위치를 가장자리에서 16px로 통일했습니다. 가운데 화살표는 말풍선 정가운데에 맞췄습니다.')}
  {callout('ok', '확정', '2026-10-27', 'Guide Tooltip은 현재 모양을 유지합니다.')}
</div></section>'''
    return content

def p_datepicker():
    I2 = lambda n: icon('Icon/Assets/' + n, 'icon')
    hours = ''.join(f'<button type="button" class="chip-button chip-button--38 dp-hour" aria-pressed="false">{h}</button>' for h in ['12:00'] + [f'{h}:00' for h in range(1, 12)])
    live = (f'<section class="dtp js-dtp" aria-label="날짜와 시간 선택"><div class="dtp__header"><button type="button" class="dtp__icon-btn" data-dtp-close aria-label="닫기">{I2("Close")}</button></div>'
            f'<div class="dtp__calendar"><div class="dtp__month"><button type="button" class="dtp__icon-btn" data-dtp-prev aria-label="이전 달">{I2("Chevron-Left")}</button><h3 class="dtp__month-title"></h3>'
            f'<button type="button" class="dtp__icon-btn" data-dtp-next aria-label="다음 달">{I2("Chevron-Right")}</button></div><div class="dtp__week">' + ''.join(f'<span>{d}</span>' for d in '일월화수목금토') + '</div><ul class="dtp__days"></ul></div>'
            f'<div class="dtp__time" hidden><div class="tabs tabs--plain" role="tablist"><button type="button" role="tab" class="tab" data-mer="am" aria-selected="true">오전</button><button type="button" role="tab" class="tab" data-mer="pm" aria-selected="false">오후</button></div>'
            f'<div class="dtp__hours">{hours}</div></div><div class="dtp__footer"><div class="dtp__cta"><button type="button" class="btn btn--primary btn--block" disabled>완료</button></div></div></section>')
    days = ''.join(f'<div class="state"><span class="state-label">{n}</span><button type="button" class="dtp__day{c} dp-static">20</button></div>' for n, c in [('Default', ''), ('Hover', ' is-hover'), ('Pressed', ' is-pressed'), ('Selected', ' is-selected'), ('Today', ' is-today'), ('Disabled', ' is-disabled')])
    code_src = DP_CODE
    content = page_head('Components', 'Date Time Picker', '날짜와 시간을 함께 고르는 바텀시트입니다. 달력에서 날짜를 고르면 시간 영역이 열리고, 날짜와 시간을 모두 골라야 완료 버튼이 활성화됩니다.', status=('ok', '확정'), node='1-1804')
    content += f"""<section class="section"><h2>예시</h2><p>오늘은 파란 글자로 표시되고, 지난 날짜는 고를 수 없습니다. 날짜를 누르면 오전·오후와 시간이 나타나고, 시간 줄은 옆으로 밀어서 봅니다.</p><div class="canvas canvas--sunk dp-wrap">{live}</div></section>
<section class="section"><h2>구성</h2>{table(['영역', '내용'], [['Header area', '높이 56 · 오른쪽에 닫기 버튼(24px)'], ['Contents area', '달력(월 이동 + 요일 + 날짜) · 오전/오후 · 시간 칩'], ['Button area', '<a href="button.html">Button</a> 48 Primary, 날짜와 시간을 모두 고르기 전에는 Disabled']])}<p>바텀시트에는 핸들바가 없고 높이를 줄이거나 늘릴 수 없습니다. 닫기 버튼이나 위쪽 딤드(Opacity 72)를 눌러 닫습니다.</p></section>
<section class="section"><h2>날짜</h2><div class="canvas"><div class="states">{days}</div></div>
{table(['상태', '값'], [['크기', '41 × 41 원, 날짜 사이 8px · 줄 사이 8px · 일요일부터 시작'], ['글자', '<a href="typography.html">Body 15 Medium</a> Gray 800 (요일은 Gray 600)'], ['Hover / Pressed', '배경 Gray 100 / Gray 200'], ['Selected', 'Blue 600 배경, 흰 글자'], ['Today', 'Blue 600 글자'], ['Disabled', 'Gray 400 글자 (지난 날짜 등 고를 수 없는 날)']])}</section>
<section class="section"><h2>시간</h2><p>오전/오후는 <a href="tabs.html">밑줄 없는 Text 탭</a>, 시간은 <a href="chip-button.html">Chip Button</a> Size 38을 씁니다. 12시간제로 오전·오후 모두 12:00, 1:00~11:00을 보여 줍니다. 시간 줄은 화면 너비 안에서 옆으로 스크롤되고, 더 볼 칩이 있는 쪽 가장자리가 흐려집니다.</p></section>
<section class="section"><h2>코드</h2>{code(code_src)}</section>
<section class="section"><h2>결정 기록</h2><div class="callouts">
  {callout('ok', '반영', '2026-10-29', 'Figma 컴포넌트 4가지 상태 모두에서 오늘 이전 날짜(1~6일)를 Disabled로 바꿨습니다. 지난 날짜는 마감일로 고를 수 없습니다.')}
  {callout('ok', '반영', '2026-10-27', '요일 배치를 실제 달력대로 고쳤습니다(2024년 7월 1일 = 월요일). 파란 날짜는 오늘 표시입니다.')}
  {callout('ok', '반영', '2026-10-27', 'Date Selected 상태는 시간을 아직 고르지 않았으므로 버튼을 Disabled로 바꿨습니다.')}
  {callout('ok', '반영', '2026-10-27', '시간은 12시간제로 바꿨습니다. 오후에 쓰던 13:00~24:00을 없애고 오전·오후 모두 12:00, 1:00~11:00입니다.')}
  {callout('ok', '반영', '2026-10-27', '901px로 넘치던 시간 줄을 375px 안에서 스크롤되게 하고 가장자리 흐림을 넣었습니다.')}
  {callout('ok', '반영', '2026-10-27', '시간 칩은 Chip Button Size 38, 오전/오후는 밑줄 없는 Text 탭 인스턴스로 바꿨습니다. 날짜는 새 Day 컴포넌트(Default·Hover·Pressed·Selected·Today·Disabled)를 씁니다.')}
  {callout('ok', '반영', '2026-10-27', '요일·날짜에 Body 15 Medium을 연결했습니다. 칸 크기가 바뀌지 않도록 글자 상자 높이는 그대로 두었습니다. 속성 이름은 State(Default · Date Selected · Time Selected (AM) · Time Selected (PM))로 정리했습니다.')}
  {callout('ok', '반영', '2026-10-27', 'Anatomy의 빈 시트를 실제 인스턴스로 채우고, 번호 동그라미를 28px Gray 900으로 통일했습니다. 숨은 레이어와 1px 틈도 정리했습니다.')}
</div></section>"""
    return content

DP_CODE = """<link rel="stylesheet" href="css/buttons.css">
<link rel="stylesheet" href="css/chips.css">
<link rel="stylesheet" href="css/tabs.css">
<link rel="stylesheet" href="css/date-picker.css">

<section class="dtp">
  <div class="dtp__header"><button class="dtp__icon-btn" aria-label="닫기">…</button></div>
  <div class="dtp__calendar">
    <div class="dtp__month">… <h3 class="dtp__month-title">2024년 7월</h3> …</div>
    <div class="dtp__week"><span>일</span>…<span>토</span></div>
    <ul class="dtp__days">
      <li></li>  <!-- 1일 앞 빈칸 -->
      <li><button class="dtp__day" aria-pressed="false">1</button></li>
      <li><button class="dtp__day" aria-current="date">7</button></li>   <!-- 오늘 -->
      <li><button class="dtp__day" aria-pressed="true">20</button></li>  <!-- 선택 -->
    </ul>
  </div>
  <div class="dtp__time">
    <div class="tabs tabs--plain" role="tablist">
      <button role="tab" class="tab" aria-selected="true">오전</button>
      <button role="tab" class="tab" aria-selected="false">오후</button>
    </div>
    <div class="dtp__hours">
      <button class="chip-button chip-button--38" aria-pressed="true">12:00</button> …
    </div>
  </div>
  <div class="dtp__footer"><div class="dtp__cta"><button class="btn btn--primary btn--block" disabled>완료</button></div></div>
</section>"""

def pp(illust=False, buttons='single', title='Title', sub='Sub title', b1='버튼', b2='버튼'):
    acts = {'single': f'<div class="popup__actions"><button type="button" class="btn btn--primary">{b1}</button></div>',
            'side': f'<div class="popup__actions"><button type="button" class="btn btn--secondary">{b2}</button><button type="button" class="btn btn--primary">{b1}</button></div>',
            'stack': f'<div class="popup__actions popup__actions--stack"><button type="button" class="btn btn--primary">{b1}</button><button type="button" class="btn btn--ghost">{b2}</button></div>'}[buttons]
    t = (f'<p class="popup__title">{title}</p>' if title else '') + (f'<p class="popup__sub">{sub}</p>' if sub else '')
    return f'<div class="popup" role="dialog" aria-modal="true"><div class="popup__text">{t}</div>' + ('<div class="popup__illust"><img class="illust illust--120" src="img/illustrations/content-recommend.svg" alt=""></div>' if illust else '') + acts + '</div>'

def p_popup():
    grid = ''.join(f'<div class="state"><span class="state-label">{tn} · {n}</span><div class="pp-cell pp-static">{pp(il, b)}</div></div>'
                   for tn, il in (('Basic', False), ('With Illustration', True)) for n, b in [('Single', 'single'), ('Side by Side', 'side'), ('Stacked', 'stack')])
    demo_btns = ''.join(f'<button type="button" class="btn btn--secondary btn--sm" data-popup="{k}">{n}</button>' for k, n in [('single', 'Single'), ('side', 'Side by Side'), ('stack', 'Stacked'), ('illust', 'With Illustration')])
    tpls = (f'<template id="pp-single">{pp(False, "single", "회고를 저장했어요", "작성한 내용은 회고 목록에서 다시 볼 수 있어요.", "확인")}</template>'
            f'<template id="pp-side">{pp(False, "side", "작성을 그만둘까요?", "지금 나가면 작성한 내용이 사라져요.", "계속 쓰기", "나가기")}</template>'
            f'<template id="pp-stack">{pp(False, "stack", "알림을 켤까요?", "회고할 시간이 되면 알려 드릴게요.", "알림 켜기", "다음에")}</template>'
            f'<template id="pp-illust">{pp(True, "single", "이런 회고는 어때요?", "지금 팀에 맞는 회고 방식을 추천해 드려요.", "추천 보기")}</template>')
    content = page_head('Components', 'Popup', '팝업은 화면 가운데에 떠서 중요한 정보를 알리거나 선택을 요청하는 모달입니다. 화면 전체를 딤드(Opacity 72)로 덮고, 한 번에 하나만 띄웁니다.', status=('ok', '확정'), node='1-4692')
    content += f"""<section class="section"><h2>예시</h2><p>버튼을 누르면 팝업이 뜹니다. 팝업 안의 버튼이나 바깥 딤드를 누르면 닫힙니다.</p>
<div class="canvas canvas--sunk"><div class="cb-demo pp-demo">{demo_btns}</div></div>{tpls}<div class="popup-dim" id="popup-dim" hidden></div></section>
<section class="section"><h2>종류</h2><p>Type(Basic · With Illustration)과 Button(Single · Side by Side · Stacked)을 조합해 씁니다.</p><div class="canvas canvas--sunk"><div class="states pp-grid">{grid}</div></div>
{table(['Button', '구성', '쓰는 곳'], [['Single', 'Primary 1개, 너비 채움', '확인만 받으면 되는 알림'], ['Side by Side', 'Secondary + Primary, 가로로 반씩 · 간격 8', '취소/확인처럼 무게가 비슷한 두 선택'], ['Stacked', 'Primary 위, <a href="button.html">Ghost</a> 아래 · 간격 4', '권하는 행동 하나와 가벼운 대안(다음에, 취소)']])}</section>
<section class="section"><h2>구성</h2>{table(['영역', '값'], [['카드', '너비 315 · 안쪽 여백 위 30 · 좌우 20 · 아래 20 · 모서리 16 · 흰 배경 · 그림자 <a href="elevation.html">Shadow 400</a>'], ['Title (선택)', '<a href="typography.html">Title 18 Bold</a>(140%) Gray 900, 가운데 정렬, 최대 2줄'], ['Sub Title (선택)', '<a href="typography.html">Body 16 Medium</a> Gray 500, 최대 2줄 · 제목과 간격 12'], ['Illustration (선택)', '<a href="illustration.html">Illustration</a> 120 × 120, 글자와 버튼 사이 · 간격 20. 기본은 Content/Recommend이고 Illustration 속성으로 바꿉니다'], ['Button area', '<a href="button.html">Button</a> 48 · 글자 영역과 간격 28(아래 여백 8 + 간격 20)'], ['딤드', 'Opacity 72, 팝업은 화면 정가운데']])}</section>
<section class="section"><h2>Modal (웹)</h2><p>웹(1440)에서 여러 단계로 입력을 받는 큰 모달입니다. 위에 닫기와 단계 막대, 가운데 질문과 입력, 아래 이전 · 다음 버튼(48)이 있습니다. 확인 · 선택만 받으면 위의 Popup을 씁니다.</p>
<div class="canvas canvas--sunk canvas--center"><div class="modal" style="height:auto"><div class="modal__body"><div class="modal__head"><button type="button" class="modal__close" aria-label="닫기">{icon("Icon/Assets/Close", "icon")}</button></div><div class="progress-bar"><ol class="progress-bar__track"><li class="progress-bar__step is-done"></li><li class="progress-bar__step is-done"></li><li class="progress-bar__step"></li></ol></div><p class="modal__title">회고의<br>이름은 무엇인가요?</p><div style="height:120px;border-radius:8px;background:var(--color-blue-50,#f1f6ff);display:grid;place-items:center;color:var(--color-blue-600,#6c9cfa);font-size:14px">Content 슬롯</div></div><div class="modal__foot"><button type="button" class="btn btn--secondary">이전</button><button type="button" class="btn btn--primary" disabled>다음</button></div></div></div>
{table(['영역', '값'], [['틀', '520 × 652, 모서리 20(<code>--radius-modal-lg</code>), 흰 바탕, <a href="elevation.html">Shadow 400</a>, 뒤 딤드 Opacity 72'], ['위', '뒤로 가기 24(Show Back, 한 단계 뒤 모달) + 제목 <a href="typography.html">Title 22 Bold</a>(Show Title) + 닫기 24(오른쪽) · <a href="progress-bar.html">Progress Bar</a>(Show Progress), 사이 20'], ['가운데', 'Content <strong>슬롯</strong> — 화면마다 질문 · 입력을 직접 넣습니다(예: 회고 이름 — 제목 Heading 24 + Text Input + Text Area + Guide Tooltip)'], ['아래', '<a href="button.html">Button 48</a> 두 개(이전 Secondary · 다음 Primary), 간격 10, 여백 위 8 · 좌우 24 · 아래 24. 이전은 Show Prev, 버튼 영역 전체는 Show Footer로 숨김'], ['두 가지 쓰임', '단계형 입력(회고 이름 설정): 제목 없음 · 단계 막대 · 버튼. 목록형(템플릿 리스트): 제목 · 버튼 없음 · 바탕 Gray 100'], ['Figma', '<code>Modal (Web)</code> · Title · Show Title · Content(슬롯) · Show Progress · Show Prev · Show Footer · Show Back']])}</section>
<section class="section"><h2>코드</h2>{code(PP_CODE)}</section>
<section class="section"><h2>결정 기록</h2><div class="callouts">
  {callout('ok', '반영', '2026-10-27', 'Button 속성값을 Single · Side by Side · Stacked로 바꿨습니다. 전에는 Two Button - Vertical이 가로 배치, Horizontal이 세로 배치로 이름과 반대였습니다.')}
  {callout('ok', '반영', '2026-10-27', 'Stacked의 두 번째 버튼을 White에서 Ghost 버튼으로 바꿨습니다. 흰 팝업 위에서 버튼 모양이 보이지 않던 문제입니다.')}
  {callout('ok', '반영', '2026-10-27', '속성 이름을 Type으로 정리하고(숨은 문자 삭제), 중복된 Illustration 켜고 끄기 속성 2개를 없앴습니다. 그림은 With Illustration 유형에만 있습니다.')}
  {callout('ok', '추가', '2026-10-27', 'Title · Sub Title 텍스트 속성과 Show Title · Show Sub Title 켜고 끄기 속성을 추가했습니다.')}
  {callout('ok', '반영', '2026-10-27', '제목은 행간 140%의 Title 18 Bold 스타일에 연결했습니다(외부 라이브러리 스타일은 150%였음). 팝업 높이가 2px 줄었습니다.')}
  {callout('ok', '반영', '2026-10-27', '분리돼 있던 버튼을 Button 인스턴스로 바꾸고, 숨은 중복 버튼 줄과 빈 레이어를 지웠습니다. Stacked 버튼 묶음 너비를 채우기로 맞췄습니다.')}
  {callout('ok', '확정', '2026-10-27', 'Sub Title 색은 Gray 500을 유지합니다.')}
  {callout('ok', '반영', '2026-10-27', '회색 그림 자리를 Illustration 인스턴스(기본 Content/Recommend)로 바꾸고, Illustration 속성으로 다른 일러스트를 고를 수 있게 했습니다.')}
</div></section>"""
    return content

HI_SVG = bare(asset('safe-area-ios14'))
def bs_header(title='Title'):
    t = f'<p class="bsheet__header-title">{title}</p>' if title else ''
    return f'<div class="bsheet__header">{t}<button type="button" class="bsheet__close" aria-label="닫기">{icon("Icon/Assets/Close", "icon")}</button></div>'
def bs_footer(buttons=None):
    if not buttons: return f'<div class="bsheet__footer"><div class="bsheet__safe">{HI_SVG}</div></div>'
    cls = 'btn-group--horizontal' if len(buttons) == 2 else 'btn-group--one'
    return f'<div class="bsheet__footer"><div class="btn-group {cls}"><div class="btn-group__buttons">{"".join(buttons)}</div></div><div class="bsheet__safe">{HI_SVG}</div></div>'
def bs_btn(v, t='버튼'): return f'<button type="button" class="btn btn--{v} btn--block">{t}</button>'
def bs_tabs(a='A', b='B', extra=''):
    return f'<div class="bsheet__tabs"><div role="tablist" class="tabs tabs--fixed">{tb(a, True)}{tb(b)}</div>{extra}</div>'
def bs_short(content, buttons=None, title='Title', heading='Title<br>(최대 2줄)', label='유형타이틀', il='retro-kpt', icons=('Team', 'Team'), labels=None):
    body = {'default': '<div class="bs-slot"></div>',
            'chip': f'<div class="chip-pair">' + ''.join(cb("card", l, icon_name=ic_, live=True) for l, ic_ in zip(labels or (label, label), icons)) + '</div>',
            'illust': f'<div class="bsheet__illust"><img class="illust" src="img/illustrations/{il}.svg" alt=""></div>',
            'area': '<div class="field field--area"><label class="field__box"><textarea class="field__input" rows="3" placeholder="Text" maxlength="20" data-count></textarea><span class="field__count">0/20</span></label></div>'}[content]
    h = '' if content == 'area' else f'<h2 class="bsheet__title">{heading}</h2>'
    return f'<section class="bsheet" role="dialog" aria-modal="true" aria-label="바텀시트">{bs_header(title)}{h}<div class="bsheet__body">{body}</div>{bs_footer(buttons)}</section>'
def bs_long(content, title='Title', tabs=('A', 'B'), rows=('Text',) * 6, cta='버튼', chips=('타이틀',) * 6):
    t = bs_tabs(*tabs) if content != 'default' else ''
    flush = ''
    if content in ('default', 'tab'): body = '<div class="bs-ph">콘텐츠 영역</div>'
    elif content == 'input': body = '<div class="field"><label class="field__box"><input class="field__input" type="text" placeholder="Text" maxlength="10" data-count><span class="field__count">0/10</span></label></div>'
    else:
        chips = ''.join(tb(c, i == 0, 'box-tab') for i, c in enumerate(chips))
        t = bs_tabs(*tabs, extra=f'<div role="tablist" class="box-tabs box-tabs--scroll">{chips}</div>')
        body = '<ul class="list bs-list">' + ''.join(f'<li><label class="list-check"><span class="list-check__text">{r}</span><input class="control__input" type="checkbox"></label></li>' for r in rows) + '</ul>'
        flush = ' bsheet__body--flush'
    return f'<section class="bsheet bsheet--long" role="dialog" aria-modal="true" aria-label="바텀시트">{bs_header(title)}{t}<div class="bsheet__body scroll-area{flush}">{body}</div>{bs_footer([bs_btn("primary", cta)])}</section>'

def p_bsheet():
    shorts = [('Default', 'default', None), ('Chip Button', 'chip', None), ('Illustration', 'illust', None), ('Illustration + Single', 'illust', 1), ('Illustration + Side by Side', 'illust', 2), ('Text Area + Single', 'area', 1)]
    BTN = {None: None, 1: [bs_btn('primary')], 2: [bs_btn('secondary'), bs_btn('primary')]}
    sgrid = ''.join(f'<div class="state"><span class="state-label">{n}</span><div class="bs-static">{bs_short(c, BTN[b])}</div></div>' for n, c, b in shorts)
    lgrid = ''.join(f'<div class="state"><span class="state-label">{n}</span><div class="bs-static">{bs_long(c)}</div></div>' for n, c in [('Default', 'default'), ('Tab', 'tab'), ('Tab + Text Input', 'input'), ('Tab + Filter', 'filter')])
    demo_btns = ''.join(f'<button type="button" class="btn btn--secondary btn--sm" data-bsheet="{k}">{n}</button>' for k, n in [('chip', 'Short · Chip Button'), ('illust', 'Short · Illustration'), ('filter', 'Long · Tab + Filter')])
    tpls = (f'<template id="bs-chip">{bs_short("chip", None, "회고 만들기", "누구와 회고하나요?", icons=("Team", "Person"), labels=("팀과 함께", "혼자서"))}</template>'
            f'<template id="bs-illust">{bs_short("illust", [bs_btn("secondary", "다른 방식"), bs_btn("primary", "이걸로 할게요")], "회고 방식", "KPT 회고를<br>추천해요")}</template>'
            f'<template id="bs-filter">{bs_long("filter", "필터", ("유형", "기간"), ("진행 중", "완료", "내가 만든 회고", "초대받은 회고", "즐겨찾기", "보관함", "이번 주", "지난달", "댓글 있음", "사진 있음"), "적용하기", ("전체", "KPT", "PMI", "SSC", "5F", "Mad Sad Glad"))}</template>')
    content = page_head('Components', 'Bottom Sheet', '바텀시트는 화면 하단에 고정되어, 현재 화면과 관련된 작업을 하거나 마치는 데 필요한 정보를 보여 줍니다. 손잡이(핸들바)가 없어 크기를 줄이거나 늘릴 수 없고, 닫기 버튼이나 위쪽 딤드를 눌러 닫습니다.', status=('ok', '확정'), node='1-1511')
    content += f"""<section class="section"><h2>예시</h2><p>버튼을 누르면 바텀시트가 올라옵니다. 닫기 버튼, 시트 아래 버튼, 위쪽 딤드를 누르면 닫힙니다.</p>
<div class="canvas canvas--sunk"><div class="cb-demo pp-demo">{demo_btns}</div></div>{tpls}<div class="bsheet-dim" id="bsheet-dim" hidden></div></section>
<section class="section"><h2>Short</h2><p>내용 높이에 맞춰 늘어납니다. Content(Default · Chip Button · Illustration · Text Area)와 Button(None · Single · Side by Side)을 조합합니다. 버튼이 없으면 Home Indicator만 남습니다.</p><div class="canvas canvas--sunk"><div class="states bs-grid">{sgrid}</div></div></section>
<section class="section"><h2>Long</h2><p>높이 670으로 고정되고, 본문(Body)이 남는 공간을 채웁니다. 내용이 넘치면 본문만 스크롤됩니다. 하단에는 CTA 버튼 그룹을 둡니다.</p><div class="canvas canvas--sunk"><div class="states bs-grid">{lgrid}</div></div></section>
<section class="section"><h2>구성</h2>{table(['영역', '값'], [
    ['시트', '너비 375 · 위 모서리 16 · 흰 배경(Gray 0) · 그림자 <a href="elevation.html">Shadow 400</a> · 세로 자동 배치'],
    ['① Header', '높이 56 · 가운데 <a href="typography.html">Title 16 Bold</a> · 오른쪽 닫기 버튼 40(아이콘 24). Show Title · Show Close로 켜고 끕니다'],
    ['② Title (Short)', '<a href="typography.html">Title 20 Bold</a> Gray 900, 가운데 정렬, 최대 2줄 · 좌우 20'],
    ['③ Toggle (Long)', '<a href="tabs.html">Text 탭</a>(같은 너비) 52 · Filter는 아래에 <a href="tabs.html">Box 탭</a> 74'],
    ['④ Body', '좌우 20 · 위 24(제목 다음) 또는 20(헤더·탭 다음) · 아래 24(Short) / 20(Long). Filter 목록은 좌우 여백 없이 <a href="lists.html">체크박스 리스트</a>. 내용이 넘치면 <a href="scroll-bar.html">Scroll Bar</a>로 스크롤'],
    ['Illustration', '<a href="illustration.html">Illustration</a> 160 × 160, 기본 Retro/KPT. Illustration 속성으로 바꿉니다'],
    ['⑤ Footer', '<a href="button.html">버튼 그룹</a>(안전영역 포함 106) 또는 버튼이 없을 때 Home Indicator 34'],
    ['딤드', 'Opacity 72, 시트는 화면 아래에 붙습니다']])}</section>
<section class="section"><h2>코드</h2>{code(BS_CODE)}</section>
<section class="section"><h2>결정 기록</h2><div class="callouts">
  {callout('ok', '반영', '2026-10-27', 'Variant 속성을 정리했습니다. Short는 Content(Default · Chip Button · Illustration · Text Area)와 Button(None · Single · Side by Side), Long은 Content(Default · Tab · Tab + Text Input · Tab + Filter)입니다. 이름의 두 칸 띄어쓰기도 없앴습니다.')}
  {callout('ok', '반영', '2026-10-27', '켜고 끄기 속성을 두 세트 모두 Show Title(헤더 제목)과 Show Close(닫기 버튼)로 통일했습니다. 왼쪽 빈 자리에 잘못 연결돼 있던 속성은 지웠습니다.')}
  {callout('ok', '반영', '2026-10-27', '큰 제목 색(#212529, 팔레트 밖)을 Gray 900 스타일에 연결했습니다.')}
  {callout('ok', '반영', '2026-10-27', '버튼 그룹에 이미 안전영역이 있는데 겹쳐 있던 Home Indicator 4개를 지웠습니다.')}
  {callout('ok', '반영', '2026-10-27', '세로 자동 배치로 바꿨습니다. Short는 내용 높이에 맞추고(357 · 354 · 426 · 308), Long은 670으로 고정해 본문이 남는 공간을 채웁니다. 제목 아래 1px 틈과 25px 간격은 0 · 24로 맞췄습니다.')}
  {callout('ok', '반영', '2026-10-27', '복사된 옛 그림 그룹을 Illustration 인스턴스(기본 Retro/KPT, 160)로 바꾸고 Illustration 속성으로 교체할 수 있게 했습니다.')}
  {callout('ok', '반영', '2026-10-27', '칩 두 개(164 + 8 + 164 = 336)와 Text Area(336)를 본문 너비 335에 맞췄습니다.')}
  {callout('ok', '반영', '2026-10-27', 'Long 본문이 버튼 영역을 침범하던 문제를 고쳤습니다. 본문은 헤더나 탭 아래 20부터 시작하고 버튼 위에서 끝납니다.')}
  {callout('ok', '반영', '2026-10-27', 'Filter 목록을 회색 자리 표시와 숨은 글자에서 꺼내 같은 체크박스 리스트 6줄로 순서대로 정렬했습니다. 분리돼 있던 마지막 줄은 지웠습니다.')}
  {callout('ok', '반영', '2026-10-27', '외부 라이브러리 Text Input을 로컬 Fields/Text Input으로 바꿨습니다.')}
  {callout('ok', '반영', '2026-10-27', '탭 B 글자가 A보다 2px 위에 있던 문제를 원본 Text 탭으로 되돌려 맞췄습니다.')}
  {callout('ok', '반영', '2026-10-27', 'Anatomy와 Usage를 손으로 그린 도형 대신 실제 컴포넌트 인스턴스로 다시 만들고, 번호를 30×30으로 맞추고 Short 4번에도 영역 표시를 넣었습니다. 숨은 레이어와 Frame 같은 이름도 정리했습니다.')}
  {callout('ok', '반영', '2026-10-27', '본문이 넘칠 때 브라우저 기본 스크롤 대신 <a href="scroll-bar.html">Scroll Bar</a>(Opacity 22 → 32 → 48)를 씁니다. 본문에 scroll-area 클래스를 함께 붙입니다.')}
  {callout('ok', '반영', '2026-10-27', 'Usage 프레임 뒤에 가려져 있던 키보드 설명을 보이는 위치로 옮기고, 아래 안내 글을 왼쪽 64에 맞췄습니다.')}
</div></section>"""
    return content

BS_CODE = """<link rel="stylesheet" href="css/buttons.css">
<link rel="stylesheet" href="css/illustration.css">
<link rel="stylesheet" href="css/bottom-sheet.css">

<div class="bsheet-dim">                         <!-- 딤드를 누르면 닫기 -->
  <section class="bsheet" role="dialog" aria-modal="true" aria-labelledby="bs-title">
    <div class="bsheet__header">
      <p class="bsheet__header-title">회고 방식</p>
      <button class="bsheet__close" aria-label="닫기">…Close 아이콘…</button>
    </div>
    <h2 class="bsheet__title" id="bs-title">KPT 회고를 추천해요</h2>
    <div class="bsheet__body">
      <div class="bsheet__illust"><img class="illust" src="img/illustrations/retro-kpt.svg" alt=""></div>
    </div>
    <div class="bsheet__footer">
      <div class="btn-group btn-group--horizontal"><div class="btn-group__buttons">
        <button class="btn btn--secondary btn--block">다른 방식</button>
        <button class="btn btn--primary btn--block">이걸로 할게요</button>
      </div></div>
      <div class="bsheet__safe">…Home Indicator…</div>
    </div>
  </section>
</div>

<!-- Long: <section class="bsheet bsheet--long"> + header + <div class="bsheet__tabs">탭</div>
     + <div class="bsheet__body scroll-area"> (넘치면 Scroll Bar로 스크롤) + footer -->"""

PP_CODE = """<link rel="stylesheet" href="css/buttons.css">
<link rel="stylesheet" href="css/popup.css">

<div class="popup-dim">
  <div class="popup" role="dialog" aria-modal="true" aria-labelledby="pp-title">
    <div class="popup__text">
      <p class="popup__title" id="pp-title">작성을 그만둘까요?</p>
      <p class="popup__sub">지금 나가면 작성한 내용이 사라져요.</p>
    </div>
    <!-- With Illustration: <div class="popup__illust"><img class="illust illust--120" src="img/illustrations/content-recommend.svg" alt=""></div> -->
    <div class="popup__actions">                      <!-- Side by Side -->
      <button class="btn btn--secondary">나가기</button>
      <button class="btn btn--primary">계속 쓰기</button>
    </div>
    <!-- Stacked: <div class="popup__actions popup__actions--stack"> btn--primary + btn--ghost -->
  </div>
</div>"""

def logo_card(n, label, cap, bg=None, cls=''):
    svgtxt = (LOGO / f'{n}.svg').read_text()
    style = f' style="background:{bg}"' if bg else ''
    return (f'<figure class="lg {cls}"><div class="lg-stage"{style}>{logo_svg(n, label)}</div>'
            f'<figcaption><span><strong>{label}</strong>{cap}</span>'
            f'<button type="button" class="copy copy--inline" data-copy="{esc(svgtxt)}" data-copy-msg="{label} SVG를 복사했어요">SVG 복사</button></figcaption></figure>')

IL = [
    ('content', 'Content', '콘텐츠 이미지', '화면 안에서 상황을 보여 주는 그림입니다. 빈 화면, 회고 단계, 완료 화면, 초대에 씁니다.', [
        ('content-space-empty', 'Space Empty', '스페이스에 아직 회고가 없을 때'), ('content-space', 'Space', '스페이스 소개'), ('content-recommend', 'Recommend', '회고 방식 추천'),
        ('content-write', 'Write', '회고 작성'), ('content-start', 'Start', '회고 시작'), ('content-done', 'Done', '회고 완료'),
        ('content-invite', 'Invite', '회고 초대')]),
    ('banner', 'Banner', '배너', '"같이 회고해요!" 홍보 배너입니다. 바탕색까지 그림이라 배경이 투명하지 않습니다.', [
        ('banner-1x1', '1:1', '정사각 배너 · 500 × 500'), ('banner-2x1', '2:1', '가로 배너 · 1000 × 500')]),
    ('retro', 'Retro', '회고 설명', '회고 방식을 소개하는 그림입니다. 방식 선택과 방식 설명 화면에 씁니다.', [
        ('retro-custom', 'Custom', '커스텀 회고'), ('retro-untitled', 'Untitled', '무제 회고'), ('retro-ssc', 'SSC', 'Start · Stop · Continue'), ('retro-kpt', 'KPT', 'Keep · Problem · Try'),
        ('retro-mad-sad-glad', 'Mad Sad Glad', '감정 회고'), ('retro-pmi', 'PMI', 'Plus · Minus · Interesting'), ('retro-5f', '5F', 'Facts · Feelings · Findings · Future · Feedback')]),
    ('splash', 'Splash', '스플래시', '앱을 처음 열었을 때 기능을 소개하는 온보딩 그림입니다. 순서대로 씁니다.', [
        ('splash-step-by-step', 'Step by Step', '1 · 차근차근, 단계적인 회고'), ('splash-schedule', 'Schedule', '2 · 일정과 기록'), ('splash-report', 'Report', '3 · 회고 리포트'), ('splash-goal', 'Goal', '4 · 목표')]),
]
def p_illustration():
    def card(slug, name, use, cat):
        wide = ' il-card--wide' if slug.endswith('2x1') else ''
        return (f'<figure class="il-card{wide}"><div class="il-card__img"><img src="img/illustrations/{slug}.svg" alt="" loading="lazy"></div>'
                f'<figcaption><span class="il-card__name">{cat}/{name}</span><span class="il-card__use">{use}</span>'
                f'<button type="button" class="copy copy--inline il-card__dl" data-copy="{esc((R / "img/illustrations" / (slug + ".svg")).read_text().strip())}" data-copy-msg="{cat}/{name} SVG를 복사했어요">SVG 복사</button></figcaption></figure>')
    sections = ''.join(f'<section class="section"><h2>{label} · {kr}</h2><p>{desc}</p><div class="il-grid">' + ''.join(card(s, n, u, label) for s, n, u in items) + '</div></section>'
                       for key, label, kr, desc, items in IL)
    sizes = ''.join(f'<figure class="il-size"><img class="illust illust--{w}" src="img/illustrations/content-recommend.svg" alt=""><figcaption>{w} · {u}</figcaption></figure>'
                    for w, u in [(120, 'Popup'), (160, '목록·카드 안 빈 상태'), (200, '전체 화면 빈 상태'), (280, '스플래시')])
    content = page_head('Brand', 'Illustration', '일러스트는 화면의 상황과 회고 방식을 그림으로 보여 주는 브랜드 그래픽입니다. 쓰임에 따라 Content, Banner, Retro, Splash 네 가지로 나누고, 500 × 500 원본을 비율대로 줄여 씁니다.',
                        status=('ok', '확정'), node='292-4132')
    content += f'''<section class="section"><h2>종류</h2>{table(['분류', '쓰는 곳', '개수'], [['Content · 콘텐츠 이미지', '빈 화면, 회고 단계, 완료, 초대', '7'], ['Banner · 배너', '"같이 회고해요!" 홍보', '2'], ['Retro · 회고 설명', '회고 방식 선택과 설명', '7'], ['Splash · 스플래시', '처음 실행할 때 온보딩', '4']])}</section>
{sections}
<section class="section"><h2>크기</h2><p>원본은 500 × 500이고 배경은 투명합니다. Banner/2:1만 1000 × 500입니다. 정해진 크기로만 줄여 쓰고, 원본보다 키우지 않습니다.</p><div class="canvas il-canvas"><div class="il-sizes">{sizes}</div></div>
{table(['규칙', '내용'], [['배경', '투명. 놓이는 화면의 배경색이 그대로 보입니다. Banner는 바탕색까지 그림입니다'], ['색', '<a href="color.html">Blue · Gray 팔레트</a>의 Color 스타일만 씁니다'], ['대체 텍스트', '꾸밈용이므로 <code>alt=""</code>로 둡니다. 뜻은 옆의 제목과 설명이 전합니다'], ['Figma', '각 일러스트가 컴포넌트입니다. 인스턴스를 드래그로 늘리거나 줄여도 비율대로 함께 바뀝니다. 내보내기는 SVG, PNG 2x·3x']])}</section>
<section class="section"><h2>Popup에서 쓰기</h2><p><a href="popup.html">Popup</a>의 With Illustration은 그림 자리에 Content/Recommend가 120 크기로 들어 있습니다. Figma에서 Illustration 속성으로 다른 일러스트로 바꿀 수 있습니다(Banner/2:1 제외).</p></section>
<section class="section"><h2>코드</h2>{code(IL_CODE)}</section>
<section class="section"><h2>결정 기록</h2><div class="callouts">
  {callout('ok', '반영', '2026-10-27', '배너 2개는 Content에서 분리해 Banner/1:1, Banner/2:1로 묶었습니다.')}
  {callout('ok', '반영', '2026-10-27', '쓰임에 따라 Content(콘텐츠 이미지) · Retro(회고 설명) · Splash(스플래시)로 이름을 정리했습니다. 이미지1·2, 무제, 회고 시작2, Group 이름 등을 바꿨습니다.')}
  {callout('ok', '반영', '2026-10-27', '모든 일러스트를 500 기준으로 맞췄습니다. 스플래시 4개는 280에서 500으로 키우고, 그룹이던 초대 그림은 500 프레임에 넣었습니다.')}
  {callout('ok', '반영', '2026-10-27', '흰 배경을 지워 투명하게 바꿨습니다. 배너 2개는 바탕색이 그림의 일부라 유지합니다.')}
  {callout('ok', '반영', '2026-10-27', '팔레트 밖 색 7곳을 가까운 팔레트 색으로 바꾸고(#D9D9D9 → Gray 400 등), 연결이 빠진 색 121곳을 원본 Color 스타일에 연결했습니다.')}
  {callout('ok', '반영', '2026-10-27', '보이지 않던 흰 사각형 4개, 프레임 밖 사각형, 숨은 가이드 그룹을 지우고 보드 간격을 31px로 맞췄습니다. SSC 표지판 글자는 모두 36으로 맞췄습니다.')}
  {callout('ok', '반영', '2026-10-27', '인스턴스를 드래그로 리사이즈하면 안쪽 요소가 따라 줄지 않아 그림이 어그러지던 문제를 고쳤습니다. 모든 요소를 Scale 제약으로 바꾸고, 글자·선·둥근 모서리는 윤곽선(벡터)으로 바꿨습니다. 500 크기의 모양은 그대로입니다.')}
  {callout('ok', '추가', '2026-10-27', '각 일러스트를 컴포넌트로 만들고 내보내기를 SVG · PNG 2x · 3x로 통일했습니다. Popup의 그림 자리는 Illustration 속성으로 바꿀 수 있습니다.')}
</div></section>'''
    return content

IL_CODE = """<link rel="stylesheet" href="css/illustration.css">

<!-- 꾸밈용 그림: alt="" -->
<img class="illust illust--200" src="img/illustrations/content-space-empty.svg" alt="">

<!-- Popup · With Illustration -->
<div class="popup__illust">
  <img class="illust illust--120" src="img/illustrations/content-recommend.svg" alt="">
</div>

<!-- 가로 배너 (2:1) -->
<img class="illust illust--banner-wide" src="img/illustrations/banner-2x1.svg" alt="같이 회고해요!">"""

def p_logo():
    content = page_head('Brand', 'Logo', 'Layer 로고는 회고를 뜻하는 화살표와 Layer의 첫 글자 L을 겹친 모양입니다. 대부분의 경우 Basic을 씁니다. 로고 아래의 버튼을 누르면 SVG 코드가 복사됩니다.',
                        status=('ok', '확정'), node='1-4960')
    content += f'''<section class="section"><h2>심볼</h2><div class="canvas lg-hero"><div class="lg-hero__mark">{logo_svg("symbol-three-colors", "Layer 심볼")}</div>
<dl class="lg-anatomy"><div><dt><span class="sq" style="background:#172031"></span>화살표</dt><dd>지난 일을 돌아보는 회고. Blue 900</dd></div><div><dt><span class="sq" style="background:#6C9CFA"></span>L</dt><dd>Layer의 첫 글자. Blue 600</dd></div><div><dt><span class="sq" style="background:#E2EBFE"></span>겹친 칸</dt><dd>두 모양이 만나는 자리. 배경에 따라 색이 바뀝니다</dd></div></dl></div></section>
<section class="section"><h2>파비콘</h2><p>앱 아이콘과 브라우저 탭에 씁니다. 바탕 색에 따라 세 가지가 있습니다.</p><div class="lg-grid lg-grid--3">{logo_card("favicon-basic", "Basic", "밝은 배경", "#F2F4F8")}{logo_card("favicon-blue", "Blue", "파란 바탕")}{logo_card("favicon-dark-blue", "Dark Blue", "어두운 바탕")}</div>
{table(["버전", "바탕", "화살표", "L", "겹친 칸"], [["Basic", "흰색", "Blue 900", "Blue 600", "Blue 200"], ["Blue", "Blue 600", "Blue 900", "흰색", "Blue 400"], ["Dark Blue", "Blue 900", "흰색", "Blue 600", "Blue 700"]])}</section>
<section class="section"><h2>가로형</h2><p>심볼과 Layer 글자를 나란히 놓은 로고입니다. 밝은 배경에는 Basic, 어두운 배경에는 파비콘을 붙인 버전을 씁니다.</p><div class="lg-grid">{logo_card("logo-horizontal-basic", "Basic", "밝은 배경", "#FFFFFF", "lg--wide")}{logo_card("logo-horizontal-on-dark", "With Favicon", "어두운 배경 (Blue 900)", "#172031", "lg--wide")}</div></section>
<section class="section"><h2>응용</h2><p>굿즈, 발표 자료처럼 브랜딩 응용이 필요할 때 씁니다. 앱 화면에서는 쓰지 않습니다.</p><div class="lg-grid lg-grid--2">{logo_card("symbol-single-color", "Single Color", "한 가지 색", "#F2F4F8")}{logo_card("symbol-three-colors", "Three Colors", "세 가지 색", "#F2F4F8")}</div></section>
<section class="section"><h2>Figma 컴포넌트</h2><p>앱 화면에는 그림을 복사하지 말고 <code>Logo</code> 컴포넌트를 놓습니다.</p>{table(["Type", "크기", "쓰는 곳"], [["Horizontal", "64 × 21 (심볼 + Layer 글자)", "웹 LNB 펼침 상단"], ["Symbol", "20 × 20 (심볼만)", "LNB 접힘 등 좁은 자리"]])}<p class="note">색은 Blue 900(화살표) · Blue 600(L) · Blue 200(겹친 칸) 토큰에 연결되어 있습니다. 크기를 바꿀 때는 비율을 유지해 늘립니다.</p></section>
<section class="section"><h2>결정 기록</h2><div class="callouts">
  {callout("ok", "반영", "2026-10-27", "겹친 칸 색을 밝은 배경용 버전 모두 <strong>Blue 200</strong>(#E2EBFE)으로 통일했습니다. 응용의 Three Colors가 Blue 100이었던 것을 Figma와 코드 모두 고쳤습니다.")}
  {callout("ok", "확정", "2026-10-27", "모서리 둥글기는 쓰임에 따라 다르게 유지합니다. 단독 파비콘은 크기의 18%(188px에 34px), 가로형에 붙은 파비콘은 17%(120px에 20px)입니다.")}
</div></section>'''
    return content

# Token releases: newest first. Add a row and a file in downloads/ for every change (see 버전 규칙).
TOKEN_RELEASES = [
    ('0.2.1', '2026-11-03', 'downloads/layer-tokens-v0.2.1.json', 151, '토큰 값은 0.2.0과 같음. 웹 키트 추가(layer.css · layer-icons.js · layer-examples.html), components.json에 빠져 있던 코드 클래스 8개(LNB · Section Header · Logo · OS Bar 등)와 컴포넌트별 예시 마크업 위치(code.example) · web 규칙, DESIGN.md에 Web (HTML) 규칙, llms.txt'),
    ('0.2.0', '2026-11-03', 'downloads/layer-tokens-v0.2.0.json', 151, '정리 배포. 레이아웃 토큰 9개(mobile-width · web-width · lnb · lnb-folded · card-column · side-panel · margin-list 40 · margin-work 20 · panel-padding 40), 오류 · 위험 색 Red 500으로 통일(text.error · status.error), overlay.dim-popover 삭제(팝오버 · 메뉴는 딤드 없음). components.json 82개 + nested(안쪽에서 바꾸는 인스턴스) · 템플릿 2종, DESIGN.md에 레이아웃 · 템플릿 · 딤드 · 바탕 규칙'),
    ('0.1.9', '2026-10-29', 'downloads/layer-tokens-v0.1.9.json', 152, 'typography.title.22-bold · title.14-bold · title.15-bold · caption.11-semibold, radius.20 · modal-lg · button-xs, color.green.900 추가. components.json에 Card/ · Dropdown · 웹 모달. ※ 이 파일은 11-03까지 계속 보완되어 0.2.0 직전 상태와 같습니다(dim-popover 포함, 0.2.0에서 삭제)'),
    ('0.1.8', '2026-10-29', 'downloads/layer-tokens-v0.1.8.json', 134, 'typography.heading.28-bold(웹 페이지 제목) · radius.card-lg(웹 섹션 카드 16) 추가. components.json에 Empty State · LNB · Cards'),
    ('0.1.7', '2026-10-29', 'downloads/layer-tokens-v0.1.7.json', 132, '토큰 값 변화 없음. components.json에 List/Menu Item 추가, Avatar Size 42'),
    ('0.1.6', '2026-10-29', 'downloads/layer-tokens-v0.1.6.json', 132, '토큰 값 변화 없음. Date Time Picker 규칙(오늘 이전 날짜 Disabled) 반영'),
    ('0.1.5', '2026-10-29', 'downloads/layer-tokens-v0.1.5.json', 132, '토큰 값 변화 없음. components.json에 App Bar/Text Button(Default · Disabled), DESIGN.md에 전체 화면 작성 영역 규칙(안내 문구 Gray 400)'),
    ('0.1.4', '2026-10-29', 'downloads/layer-tokens-v0.1.4.json', 132, 'spacing.32 · spacing.40 추가(섹션 간격, 화면의 큰 덩어리 사이)'),
    ('0.1.3', '2026-10-29', 'downloads/layer-tokens-v0.1.3.json', 130, 'typography.body.15-medium-long 추가(행간 180%, 긴 글). Badge Gray · Size 25 반영'),
    ('0.1.2', '2026-10-29', 'downloads/layer-tokens-v0.1.2.json', 129, '토큰 값 변화 없음. components.json · DESIGN.md에 Badge White, 그래픽 아이콘 24 크기 규칙 반영'),
    ('0.1.1', '2026-10-28', 'downloads/layer-tokens-v0.1.1.json', 129, 'typography.body.13-medium 추가(카드 설명). components.json에 Badge 추가, 그래픽 아이콘 White 쓰임 규칙 보완'),
    ('0.1.0', '2026-10-28', 'downloads/layer-tokens-v0.1.0.json', 128, '첫 초안. color(팔레트 55 · 역할 19), spacing 7, radius 19, font 4, typography 15, shadow 8, focus 1. AI 패키지(DESIGN.md · components.json) 함께 공개'),
]
# AI package files per version: (label, path, download name, what it is)
AI_INSTR = open('site/downloads/ai-instructions.md', encoding='utf-8').read().strip()

AI_FIRST = """아래 Figma 파일에 새 페이지를 만들고, 다음 화면을 그려 줘.
(커뮤니티에서 복제한 내 Layer DS 파일 링크)

(여기에 화면 설명)"""

AI_FIRST_WEB = """다음 화면을 웹페이지(HTML)로 만들어 줘.

(여기에 화면 설명)"""

AI_SLASH = """/layer-design-system 레이어 홈 화면을 모바일 웹페이지로 만들어 줘. 회고 카드 2장(하나는 D-4, 하나는 작성 중)

/layer-design-system 탐색 모드로, 해외여행 보험 프로모션 화면 3개"""

AI_EXPLORE = """/layer-design-system 탐색 모드로 해 줘. 해외여행 보험 가입 프로모션 화면(모바일)이야.
- 지킬 것: Layer 토큰(색 · 글자 · 간격 · 모서리 · 그림자), 버튼 · 배지 같은 기본 컴포넌트, 해요체
- 자유롭게: 레이아웃, 정보 구성, 비주얼, 조합. 없는 묶음은 토큰으로 새로 만들어도 돼
- 내용: 가입하면 최대 1,150 포인트 / 보험료 3,290원부터(40세 라이트 플랜) / 할인 3가지(미리 3% · 함께 최대 20% · 다시 5%) / 알아보기 버튼
- 서로 다른 방향 3개(예: 정보 중심 · 비주얼 강조 · 비교표형), 시안마다 콘셉트 한 줄과 시스템에서 벗어난 부분을 적어 줘"""

AI_FIX = """두 번째 카드를 마감된 회고로 바꿔 줘. 인원은 6명 중 6명 제출.
메뉴는 닫힌 상태로 해 줘.
같은 내용으로 웹 화면도 그려 줘.
진행 중인 회고가 하나도 없을 때 화면도 옆에 하나 더 그려 줘."""

AI_EXAMPLES = [
 ('모바일 · 스페이스 회고 목록', '카드가 여러 장 쌓이는 목록 화면. 카드마다 상태 · 마감 · 제출 인원을 적었습니다.', """모바일 화면 그려 줘.

화면: 스페이스 "떡잎마을방범대"에 들어갔을 때 보이는 회고 목록
맨 위: 뒤로 가기, 제목 "떡잎마을방범대", 오른쪽에 더보기
탭: 진행 중(선택) · 마감
카드 목록(위에서부터)
  1. 스프린트 2회차 이후 회고 — 작성 중, 마감 11월 7일, 6명 중 3명 제출
  2. 중간발표 이후 회고 — 내가 제출 완료, 마감일 없음, 6명 중 5명 제출
아래: "회고 시작하기" 버튼"""),
 ('웹 · 회고 관리', '왼쪽 메뉴(LNB)가 있는 웹 화면. 메뉴가 열린 상태까지 부탁한 예시입니다.', """웹 화면 그려 줘.

화면: 스페이스 "떡잎마을방범대"의 회고 관리 화면
왼쪽 메뉴: 펼친 상태, 현재 스페이스 선택
제목: 떡잎마을방범대
두 열로 나눠서
  왼쪽 "진행 중인 회고" 2개
    - 스프린트 2회차 이후 회고 — 작성 중, 마감 11월 7일, 6명 중 3명
    - 디자인 QA 회고 — 제출 완료, 마감일 없음, 6명 중 5명
  오른쪽 "마감된 회고" 1개
    - 중간발표 이후 회고 — 분석 완료, 6명 중 6명
열려 있는 것: 첫 번째 카드의 더보기를 눌러 메뉴가 열린 상태
  (회고 마감 · 회고 수정 · 회고 삭제 — 삭제는 빨간 글자)"""),
 ('모바일 · 회고 작성 중', '질문에 답하는 흐름 화면. 진행 단계와 입력 상태를 적었습니다.', """모바일 화면 그려 줘.

화면: 회고 작성 중 3번째 질문(전체 5개). 하단 탭은 없음
맨 위: 닫기(X), 제목 없음
진행 표시: 5단계 중 3단계
질문: 이번 스프린트에서 가장 아쉬웠던 점은 무엇인가요?
답변 칸: "회의가 길어져서 개발 시간이 부족했어요"라고 입력된 상태, 글자 수 표시
아래 버튼: 이전 · 다음(다음이 주 버튼)"""),
 ('모바일 · 개인 분석 결과', '분석 컴포넌트를 쓰는 화면. 항목 이름과 개수를 그대로 적었습니다.', """모바일 화면 그려 줘.

화면: "중간발표 이후 회고"의 결과 중 개인 분석 탭
맨 위: 뒤로 가기, 제목 "중간발표 이후 회고"
탭: 팀 분석 · 개인 분석(선택)
내용(위에서부터)
  이회고님은 "회의 내용 문서화"를 가장 잘 하고 있어요
    - 회의 내용 문서화 / 회의 시간 준수 / 적극적인 피드백
  이회고님은 "커뮤니케이션" 외 2가지가 부족해요
    - 커뮤니케이션 부족 / 파트별 주차 계획 / 진행과정 이해 부족
  이회고님은 "진행사항 공유하기" 외 2가지를 개선하면 좋아요
    - 진행사항 공유하기 / 매주 파트별 스프린트 / 회의록 보고 팔로업 하기"""),
]

AI_BRIEF = '''모바일 화면 하나 설계해 줘. (첨부: DESIGN.md · components.json · tokens.json)

화면: 하단 탭 "실행목표"가 선택된 메인 화면
맨 위: 제목 "실행목표", 뒤로 가기 없음
탭: 진행 중(선택) · 지난
카드 목록
  1. 스프린트 1회차 이후 회고 — 실행 중
     목표: 긴 회의시간 줄이기 / 회의 후 내용 꼭 기록해두기
  2. 중간발표 이후 회고 — 실행 중, 아직 목표 없음'''

AI_EXAMPLE = '''{
  "screen": "모바일 · 실행목표",
  "template": "Template/Mobile",
  "variant": {"Background": "Secondary"},
  "props": {"Show App Bar": true, "Show Navigation Bar": true},
  "nested": {
    "App Bar/Top App Bar": {"variant": {"Style": "Home"}, "props": {"Title": "실행목표"}},
    "App Bar/Navigation Bar": {"variant": {"On": "Action Item"}}
  },
  "slots": {"Content": [
    {"frame": {"direction": "VERTICAL", "gap": "spacing.20"}, "children": [
      {"component": "Tabs/Text Tabs", "variant": {"Size": "18"}, "props": {"Show Tab 3": false},
       "nested": {"Tab 1": {"props": {"Title": "진행 중"}, "variant": {"State": "Selected"}},
                  "Tab 2": {"props": {"Title": "지난"}, "variant": {"State": "Unselected"}}}},
      {"frame": {"direction": "VERTICAL", "gap": "spacing.12"}, "children": [
        {"component": "Card/Goal (Mobile)", "variant": {"Badge": "On"},
         "props": {"Title": "스프린트 1회차 이후 회고", "Item 1": "긴 회의시간 줄이기", "Show Item 3": false}},
        {"component": "Card/Goal (Mobile)", "variant": {"Badge": "On"},
         "props": {"Title": "중간발표 이후 회고", "Show Items": false, "Show Empty": true}}
      ]}
    ]}
  ]}
}'''

AI_FILES = {'0.2.1': [('DESIGN.md', 'downloads/DESIGN-v0.2.1.md', 'DESIGN.md', 'AI가 가장 먼저 읽는 입구. Google DESIGN.md 형식(맨 위 YAML 토큰 + 화면 · 레이아웃 · 템플릿 · 웹(HTML) 규칙 · 하지 말 것)'),
                      ('components.json', 'downloads/layer-components-v0.2.1.json', 'layer-components-v0.2.1.json', '컴포넌트 82개의 쓰임 · 피할 것 · Figma 키와 속성 · nested · 부분별 토큰 · 코드 클래스 · 예시 마크업 위치(code.example), 웹 규칙'),
                      ('layer.css', 'kit/layer.css', 'layer.css', '웹 키트: 토큰 · 컴포넌트 스타일 전부를 한 파일로'),
                      ('layer-examples.html', 'kit/layer-examples.html', 'layer-examples.html', '웹 키트: 컴포넌트 72개의 실제 HTML 마크업'),
                      ('layer-icons.js', 'kit/layer-icons.js', 'layer-icons.js', '웹 키트: 아이콘 72개(data-icon)')],
            '0.2.0': [('DESIGN.md', 'downloads/DESIGN-v0.2.0.md', 'DESIGN.md', 'AI가 가장 먼저 읽는 입구. Google DESIGN.md 형식(맨 위 YAML 토큰 + 화면 · 레이아웃 · 템플릿 규칙 · 하지 말 것)'),
                      ('components.json', 'downloads/layer-components-v0.2.0.json', 'layer-components-v0.2.0.json', '컴포넌트 82개의 쓰임 · 피할 것 · Figma 키와 속성 · nested(안쪽 인스턴스) · 부분별 토큰 · 코드 클래스, 아이콘 48 · 일러스트 20. 새 화면은 Template/Web · Template/Mobile에서 시작')],
            '0.1.9': [('DESIGN.md', 'downloads/DESIGN-v0.1.9.md', 'DESIGN.md', 'AI가 가장 먼저 읽는 입구. Google DESIGN.md 형식(맨 위 YAML 토큰 + 화면 규칙 · 하지 말 것)'),
                      ('components.json', 'downloads/layer-components-v0.1.9.json', 'layer-components-v0.1.9.json', '컴포넌트 82개(Section Header, Analysis 7종, Card/Template · Detail · Summary, Card/Question Group (Web) · Answer/Emotion Scale · Answer/Score Bar · Card/Goal (Mobile), Template/Web(Type=List · Work) · Mobile, Popover · Menu · Menu Item · Member Item 추가, Card/ 5종 · Dropdown · Logo · 작성 패널 · Segmented Control · Modal (Web) 포함, Text 탭 통합)의 쓰임 · Figma 키와 속성 · 부분별 토큰 · 코드 클래스, 아이콘 45 · 일러스트 20')],
            '0.1.8': [('DESIGN.md', 'downloads/DESIGN-v0.1.8.md', 'DESIGN.md', 'AI가 가장 먼저 읽는 입구. Google DESIGN.md 형식(맨 위 YAML 토큰 + 화면 규칙 · 하지 말 것)'),
                      ('components.json', 'downloads/layer-components-v0.1.8.json', 'layer-components-v0.1.8.json', '컴포넌트 47개(웹 LNB · Cards 포함)의 쓰임 · Figma 키와 속성 · 부분별 토큰 · 코드 클래스, 아이콘 45 · 일러스트 20')],
            '0.1.7': [('DESIGN.md', 'downloads/DESIGN-v0.1.7.md', 'DESIGN.md', 'AI가 가장 먼저 읽는 입구. Google DESIGN.md 형식(맨 위 YAML 토큰 + 화면 규칙 · 하지 말 것)'),
                      ('components.json', 'downloads/layer-components-v0.1.7.json', 'layer-components-v0.1.7.json', '컴포넌트 44개의 쓰임 · Figma 키와 속성 · 부분별 토큰 · 코드 클래스, 아이콘 45 · 일러스트 20')],
            '0.1.6': [('DESIGN.md', 'downloads/DESIGN-v0.1.6.md', 'DESIGN.md', 'AI가 가장 먼저 읽는 입구. Google DESIGN.md 형식(맨 위 YAML 토큰 + 화면 규칙 · 하지 말 것)'),
                      ('components.json', 'downloads/layer-components-v0.1.6.json', 'layer-components-v0.1.6.json', '컴포넌트 43개의 쓰임 · Figma 키와 속성 · 부분별 토큰 · 코드 클래스, 아이콘 45 · 일러스트 20')],
            '0.1.5': [('DESIGN.md', 'downloads/DESIGN-v0.1.5.md', 'DESIGN.md', 'AI가 가장 먼저 읽는 입구. Google DESIGN.md 형식(맨 위 YAML 토큰 + 화면 규칙 · 하지 말 것)'),
                      ('components.json', 'downloads/layer-components-v0.1.5.json', 'layer-components-v0.1.5.json', '컴포넌트 43개의 쓰임 · Figma 키와 속성 · 부분별 토큰 · 코드 클래스, 아이콘 45 · 일러스트 20')],
            '0.1.4': [('DESIGN.md', 'downloads/DESIGN-v0.1.4.md', 'DESIGN.md', 'AI가 가장 먼저 읽는 입구. Google DESIGN.md 형식(맨 위 YAML 토큰 + 화면 규칙 · 하지 말 것)'),
                      ('components.json', 'downloads/layer-components-v0.1.4.json', 'layer-components-v0.1.4.json', '컴포넌트 42개의 쓰임 · Figma 키와 속성 · 부분별 토큰 · 코드 클래스, 아이콘 45 · 일러스트 20')],
            '0.1.3': [('DESIGN.md', 'downloads/DESIGN-v0.1.3.md', 'DESIGN.md', 'AI가 가장 먼저 읽는 입구. Google DESIGN.md 형식(맨 위 YAML 토큰 + 화면 규칙 · 하지 말 것)'),
                      ('components.json', 'downloads/layer-components-v0.1.3.json', 'layer-components-v0.1.3.json', '컴포넌트 42개의 쓰임 · Figma 키와 속성 · 부분별 토큰 · 코드 클래스, 아이콘 45 · 일러스트 20')],
            '0.1.2': [('DESIGN.md', 'downloads/DESIGN-v0.1.2.md', 'DESIGN.md', 'AI가 가장 먼저 읽는 입구. Google DESIGN.md 형식(맨 위 YAML 토큰 + 화면 규칙 · 하지 말 것)'),
                      ('components.json', 'downloads/layer-components-v0.1.2.json', 'layer-components-v0.1.2.json', '컴포넌트 42개의 쓰임 · Figma 키와 속성 · 부분별 토큰 · 코드 클래스, 아이콘 45 · 일러스트 20')],
            '0.1.1': [('DESIGN.md', 'downloads/DESIGN-v0.1.1.md', 'DESIGN.md', 'AI가 가장 먼저 읽는 입구. Google DESIGN.md 형식(맨 위 YAML 토큰 + 화면 규칙 · 하지 말 것)'),
                      ('components.json', 'downloads/layer-components-v0.1.1.json', 'layer-components-v0.1.1.json', '컴포넌트 42개(Badge 추가)의 쓰임 · Figma 키와 속성 · 부분별 토큰 · 코드 클래스, 아이콘 45 · 일러스트 20')],
            '0.1.0': [('DESIGN.md', 'downloads/DESIGN-v0.1.0.md', 'DESIGN.md', 'AI가 가장 먼저 읽는 입구. Google DESIGN.md 형식(맨 위 YAML 토큰 + 화면 규칙 · 하지 말 것)'),
                      ('components.json', 'downloads/layer-components-v0.1.0.json', 'layer-components-v0.1.0.json', '컴포넌트 41개의 쓰임 · Figma 키와 속성 · 부분별 토큰 · 코드 클래스, 아이콘 45 · 일러스트 20')]}
def ai_compare():
    # marker positions in the 375 × 812 screen: (n, x, y)
    MA = [(1, 172, 202), (2, 110, 246), (3, 32, 49), (4, 343, 477)]
    MB = [(1, 172, 226), (2, 110, 269), (3, 32, 52), (4, 329, 459)]
    def screen(img, marks, alt):
        m = ''.join(f'<span class="cmp-mark" style="left:{x / 3.75:.2f}%;top:{y / 8.12:.2f}%">{n}</span>' for n, x, y in marks)
        return f'<div class="cmp-screen"><img src="{img}" alt="{alt}" width="375" height="812" loading="lazy">{m}</div>'
    cols = (f'<div class="cmp-col"><p class="cmp-title"><span class="cmp-tag">A</span>DESIGN.md → HTML 시안</p><p class="cmp-sub">레이어를 처음 보는 AI · DESIGN.md 한 파일만</p>{screen("img/ai-demo-a.png", MA, "A: DESIGN.md만으로 만든 HTML 시안")}</div>'
            f'<div class="cmp-col"><p class="cmp-title"><span class="cmp-tag cmp-tag--b">B</span>components.json → Figma 화면</p><p class="cmp-sub">라이브러리 인스턴스 조립 · 변수 연결</p>{screen("img/ai-demo-b.png", MB, "B: components.json으로 만든 Figma 화면")}</div>')
    rows = [['<span class="badge-n">1</span>선택된 카드', '연한 파랑 바탕 + 파란 테두리 + 파란 글자 (추측)', 'Blue 600 채움 + 흰 글자 · 흰 아이콘 — Two Choice <code>Pressed/Selected</code>'],
            ['<span class="badge-n">2</span>카드 아이콘', '선 아이콘을 새로 그림', '그래픽 아이콘 Team · Person — 인스턴스 교체'],
            ['<span class="badge-n">3</span>뒤로 아이콘', '꺾쇠(‹)', '<code>Icon/Assets/Arrow-left</code>'],
            ['<span class="badge-n">4</span>글자 수', '입력창 밖 아래, 0/20', '입력창 안 오른쪽. 상한을 바꾸는 속성이 없어 0/10 고정 — 컴포넌트 보완 필요'],
            ['같은 점', '색 역할 · 글자 크기 · 좌우 여백 20 · 칩 · 하단 버튼 하나', '같음 (실제 컴포넌트 · 변수)']]
    return (f'<div class="canvas canvas--sunk cmp">{cols}</div>'
            f'<div class="cmp-legend">{table(["", "A · DESIGN.md → HTML", "B · components.json → Figma"], rows)}</div>'
            '<p class="note">A는 빠른 시안, B는 디자이너가 이어서 작업할 실제 화면에 맞습니다. 같은 요청(회고 만들기 1단계)으로 만들었습니다.</p>')

def p_tokens():
    latest = TOKEN_RELEASES[0]
    def dl(ver, path, primary=False):
        cls = 'btn btn--primary btn--sm' if primary else 'copy copy--inline'
        return (f'<button type="button" class="{cls}" data-dl="{path}" data-dl-name="layer-tokens-v{ver}.json">{"JSON 다운로드" if primary else "다운로드"}</button>'
                '')
    hist = [[f'<strong>v{v}</strong>' + (' ' + chip('ok', '최신') if i == 0 else ''), d, str(n), c, f'<span class="tk-dl">{dl(v, p)}</span>'] for i, (v, d, p, n, c) in enumerate(TOKEN_RELEASES)]
    names = [['색 역할', 'color.text.primary', 'text/primary <small>(Color Role)</small>', '--color-text-primary'],
             ['팔레트', 'color.gray.900', 'color/gray/900 <small>(Color, 숨김)</small>', '--color-gray-900'],
             ['간격', 'spacing.screen-x', 'spacing/screen-x <small>(Spacing)</small>', '--spacing-screen-x'],
             ['모서리', 'radius.button', 'radius/button <small>(Radius)</small>', '--radius-button'],
             ['글자', 'typography.body.15-medium', 'Body/15 Medium <small>(텍스트 스타일)</small>', '.text-body-15-medium'],
             ['그림자', 'shadow.modal', 'Shadow/400 <small>(그림자 스타일)</small>', '--shadow-modal']]
    groups = [['color', '74', '팔레트 55(gray · blue · purple · green · red · orange · opacity) + 역할 19(text · bg · border · overlay · status)', '<a href="color.html">Color</a>'],
              ['spacing', '9', '4 · 8 · 12 · 16 · 20 · 24 · 32 · 40 + screen-x', '<a href="spacing.html">Spacing</a>'],
              ['layout', '9', '화면 너비 2 · LNB 2 · 카드 열 · 오른쪽 패널 · 템플릿 여백 3', '<a href="layout.html">Layout</a>'],
              ['radius', '19', '4 · 6 · 8 · 10 · 12 · 16 · full + 용도 이름 12', '<a href="radius.html">Radius</a>'],
              ['font · typography', '19', '글꼴 1 · 굵기 3 · 텍스트 스타일 15', '<a href="typography.html">Typography</a>'],
              ['shadow', '8', '100 ~ 400 + 용도 이름 4(card · floating-button · layer · modal)', '<a href="elevation.html">Elevation</a>'],
              ['focus', '1', '키보드 Focus 표시 2px (코드 전용)', '<a href="state.html">State</a>']]
    content = page_head('Foundations', 'Tokens', '토큰은 색, 간격, 모서리, 글자, 그림자를 이름으로 부르는 약속입니다. Figma 변수 · 스타일, CSS, JSON이 같은 이름을 쓰고, 화면을 만들 때는 숫자 대신 이 이름을 고릅니다.', status=('ok', 'v0.2.0'))
    content += f'''<section class="section"><h2>다운로드</h2><div class="canvas tk-latest"><div><p class="tk-ver">v{latest[0]} <span>· {latest[1]}</span></p><p class="tk-sub">W3C Design Tokens 형식 · 토큰 {latest[3]}개 · Style Dictionary, Tokens Studio에서 바로 읽을 수 있습니다.</p></div><div class="tk-dl">{dl(latest[0], latest[2], True)}</div></div>
<p class="note tk-msg" id="tk-msg" role="status" aria-live="polite"></p></section>
<section class="section"><h2>AI 패키지</h2><p>다른 AI가 같은 디자인 시스템을 쓰게 하려면 토큰 JSON에 두 파일을 더해 함께 줍니다. 값은 토큰 JSON, 화면 규칙은 DESIGN.md, 컴포넌트를 불러오는 방법은 components.json에 있습니다.</p>
{table(['파일', '내용', '받기'], [[f'<strong>{l}</strong>', w, f'<span class="tk-dl"><button type="button" class="copy copy--inline" data-dl="{p}" data-dl-name="{n}">다운로드</button></span>'] for l, p, n, w in AI_FILES[latest[0]]] + [['<strong>tokens.json</strong>', '정확한 값의 원본(위 다운로드)', f'<span class="tk-dl">{dl(latest[0], latest[2])}</span>']])}
{table(['쓰는 곳', '줄 파일', '결과물'], [['채팅 AI (Claude, ChatGPT 등)', 'DESIGN.md', '레이어 스타일의 HTML 시안 — 분위기 · 규칙은 맞고 세부는 근사치'], ['Google Stitch 등 디자인 생성 도구', 'DESIGN.md', '시안 여러 장 — 아이디어 탐색용'], ['Claude + Figma MCP', 'components.json + DESIGN.md', '라이브러리 인스턴스로 조립된 Figma 화면 — 디자이너가 이어서 작업'], ['개발 AI (Claude Code, Cursor 등)', '세 파일 모두', '토큰과 컴포넌트 클래스를 쓰는 화면 코드'], ['변환 도구 (Style Dictionary)', 'tokens.json', 'CSS · iOS · Android 값 파일']])}
<h3 class="tk-h3">같은 화면, 두 방식</h3>
{ai_compare()}</section>
<section class="section"><h2>구성</h2>{table(['그룹', '개수', '내용', '페이지'], groups)}</section>
<section class="section"><h2>이름 규칙</h2><p>같은 토큰은 세 곳에서 모양만 다르고 같은 이름입니다. JSON은 점(.), Figma는 빗금(/), CSS는 하이픈(-)으로 잇습니다.</p>{table(['종류', 'JSON', 'Figma', 'CSS'], names)}
<p>이름에는 값이 아니라 역할을 씁니다(<code>text/secondary</code> ○, <code>text/gray-700</code> ×). 단계 토큰만 값을 이름으로 씁니다(<code>spacing/20</code>, <code>radius/12</code>).</p></section>
<section class="section"><h2>고르는 순서</h2><ol class="tk-steps">
<li><strong>역할 토큰</strong> — 색은 <code>text · bg · border · overlay · status</code>, 간격은 <code>screen-x</code>, 모서리는 용도 이름(<code>radius/button</code>)을 먼저 찾습니다.</li>
<li><strong>단계 토큰</strong> — 맞는 역할이 없으면 팔레트(<code>color/gray/600</code>)나 단계(<code>spacing/12</code>, <code>radius/8</code>)를 씁니다.</li>
<li><strong>숫자</strong> — 쓰지 않습니다. 버튼 위아래 13처럼 높이를 맞추려고 컴포넌트 안에서 생긴 값만 예외입니다.</li></ol>
<p><a href="state.html">State</a>: Hover는 기본색에서 팔레트 한 단계, Pressed는 두 단계 옮깁니다. 상태 색은 역할 토큰으로 만들지 않습니다. Disabled는 <code>bg/secondary</code> + <code>text/disabled</code>, Focus는 <code>border/focus</code> 2px(코드 전용)입니다.</p></section>
<section class="section"><h2>추가 · 변경 규칙</h2><ul class="tk-steps">
<li>실제로 쓰이는 곳이 있을 때만 만듭니다. 쓰는 곳이 없는 토큰은 AI와 사람 모두를 헷갈리게 합니다.</li>
<li>모든 토큰에 쓰는 곳 설명을 붙입니다(Figma 변수 설명, JSON <code>$description</code>).</li>
<li>Figma 변수 · 스타일, CSS, JSON을 같은 날 함께 바꾸고, 이 페이지에 새 버전을 올립니다. 기준은 이 Figma 파일입니다.</li>
<li>버전 번호: 값만 고치면 <strong>0.1.x</strong>, 토큰을 더하면 <strong>0.x.0</strong>, 이름을 바꾸거나 지우면 <strong>x.0.0</strong>을 올립니다. 이름을 바꿀 때는 한 버전 동안 옛 이름을 남겨 둡니다.</li></ul></section>
<section class="section"><h2>히스토리</h2>{table(['버전', '날짜', '토큰 수', '바뀐 내용', '파일'], hist)}</section>
<section class="section"><h2>코드에서 쓰기</h2>{code("""<!-- 바로 쓰기: 토큰 CSS -->
<link rel="stylesheet" href="css/color.css">
<link rel="stylesheet" href="css/spacing.css">
<link rel="stylesheet" href="css/radius.css">
<link rel="stylesheet" href="css/elevation.css">

/* JSON으로 직접 만들기: Style Dictionary 4 */
new StyleDictionary({
  source: ['layer-tokens-v0.1.0.json'], usesDtcg: true,
  platforms: { css: { transformGroup: 'css', files: [{ destination: 'tokens.css', format: 'css/variables', options: { outputReferences: true } }] } }
});""")}</section>'''
    return content

def p_ai_guide():
    content = page_head('시작하기', 'AI로 화면 만들기', 'Claude에게 디자인 시스템 파일을 주고 말로 부탁하면, 우리 컴포넌트로 화면을 만들어 줍니다. Figma에 그리게 할 수도 있고, 바로 열어 보는 웹페이지(HTML)로 받을 수도 있습니다. 준비는 처음 한 번만 하면 됩니다.', status=('ok', 'v0.2.1'))
    strip = ('<ol class="aig-steps">'
        '<li><b>1</b><strong>파일 받기</strong><span>방법 B(프로젝트)만</span></li>'
        '<li><b>2</b><strong>Claude에 알려 주기</strong><span>A Skill(추천) · B 프로젝트</span></li>'
        '<li><b>3</b><strong>받을 곳 정하기</strong><span>Figma(복제본) 또는 웹페이지</span></li>'
        '<li><b>4</b><strong>부탁하기</strong><span>채팅창에 말로</span></li></ol>')
    def dl(path, name):
        return f'<button type="button" class="copy copy--inline" data-dl="downloads/{path}" data-dl-name="{name}">다운로드</button>'
    files = table(['파일', '무엇인가요', '받기'], [
        ['<strong>DESIGN.md</strong>', 'AI가 가장 먼저 읽는 규칙집 — 색, 글자, 화면 틀, 딤드, 웹페이지 규칙, 하지 말 것', dl('DESIGN-v0.2.1.md', 'DESIGN.md')],
        ['<strong>layer-components-v0.2.1.json</strong>', '쓸 수 있는 컴포넌트 82개의 목록 — 언제 쓰는지, 바꿀 수 있는 값, Figma 위치, 웹 마크업 위치', dl('layer-components-v0.2.1.json', 'layer-components-v0.2.1.json')],
        ['<strong>layer-tokens-v0.2.1.json</strong>', '색 · 간격 · 모서리 · 글자 크기 값 151개', dl('layer-tokens-v0.2.1.json', 'layer-tokens-v0.2.1.json')],
        ['<strong>AI 안내문</strong>', 'Claude가 어떻게 그릴지 정해 둔 글. 프로젝트 <strong>지침</strong>에 복사해서 붙여넣습니다(2단계)', dl('ai-instructions.md', 'ai-instructions.md')],
        ['<strong>web 폴더</strong>', '웹페이지로 만들 때 쓰는 부품 — <code>layer-inline.css</code>(채팅 미리보기에 붙여 넣는 스타일) · <code>layer.js</code>(HTML 파일용, 한 줄로 스타일 + 아이콘) · <code>layer.css</code>(스타일 전부) · <code>layer-icons.js</code>(아이콘) · <code>layer-examples.html</code>(컴포넌트 72개의 실제 HTML) · 로고 · 일러스트 · 폰트. ZIP에만 들어 있어요', '<span class="tk-note">ZIP에 포함</span>']])
    kit = ('<div class="aig-kit"><div><strong>한 번에 받기 · layer-ai-kit-v0.2.1.zip</strong>'
        '<span>아래 파일 4개와 web 폴더가 한 폴더에 들어 있어요. 압축을 푼 폴더를 2단계에서 그대로 씁니다.</span></div>'
        '<button type="button" class="btn btn--primary btn--sm" data-dl="" data-dl-name="layer-ai-kit-v0.2.1.zip" data-zip="layer-ai-kit-v0.2.1|downloads/DESIGN-v0.2.1.md=DESIGN.md,downloads/layer-components-v0.2.1.json=layer-components-v0.2.1.json,downloads/layer-tokens-v0.2.1.json=layer-tokens-v0.2.1.json,downloads/ai-instructions.md=ai-instructions.md,downloads/skill/checklist.md=checklist.md,kit/layer-inline.css=web/layer-inline.css,kit/layer.js=web/layer.js,kit/layer.css=web/layer.css,kit/layer-icons.js=web/layer-icons.js,kit/layer-examples.html=web/layer-examples.html,fonts/PretendardVariable.woff2=web/fonts/PretendardVariable.woff2,fonts/OFL.txt=web/fonts/OFL.txt,kit/logo/favicon-basic.svg=web/logo/favicon-basic.svg,kit/logo/favicon-blue.svg=web/logo/favicon-blue.svg,kit/logo/favicon-dark-blue.svg=web/logo/favicon-dark-blue.svg,kit/logo/logo-horizontal-basic.svg=web/logo/logo-horizontal-basic.svg,kit/logo/logo-horizontal-on-dark.svg=web/logo/logo-horizontal-on-dark.svg,kit/logo/symbol-single-color.svg=web/logo/symbol-single-color.svg,kit/logo/symbol-three-colors.svg=web/logo/symbol-three-colors.svg,kit/illustrations/banner-1x1.svg=web/illustrations/banner-1x1.svg,kit/illustrations/banner-2x1.svg=web/illustrations/banner-2x1.svg,kit/illustrations/content-done.svg=web/illustrations/content-done.svg,kit/illustrations/content-invite.svg=web/illustrations/content-invite.svg,kit/illustrations/content-recommend.svg=web/illustrations/content-recommend.svg,kit/illustrations/content-space-empty.svg=web/illustrations/content-space-empty.svg,kit/illustrations/content-space.svg=web/illustrations/content-space.svg,kit/illustrations/content-start.svg=web/illustrations/content-start.svg,kit/illustrations/content-write.svg=web/illustrations/content-write.svg,kit/illustrations/retro-5f.svg=web/illustrations/retro-5f.svg,kit/illustrations/retro-custom.svg=web/illustrations/retro-custom.svg,kit/illustrations/retro-kpt.svg=web/illustrations/retro-kpt.svg,kit/illustrations/retro-mad-sad-glad.svg=web/illustrations/retro-mad-sad-glad.svg,kit/illustrations/retro-pmi.svg=web/illustrations/retro-pmi.svg,kit/illustrations/retro-ssc.svg=web/illustrations/retro-ssc.svg,kit/illustrations/retro-untitled.svg=web/illustrations/retro-untitled.svg,kit/illustrations/splash-goal.svg=web/illustrations/splash-goal.svg,kit/illustrations/splash-report.svg=web/illustrations/splash-report.svg,kit/illustrations/splash-schedule.svg=web/illustrations/splash-schedule.svg,kit/illustrations/splash-step-by-step.svg=web/illustrations/splash-step-by-step.svg">ZIP 다운로드</button></div>')
    s1 = ('<section class="section"><h2>1단계 · 파일 받기</h2><p>ZIP 하나로 받는 것을 추천합니다(웹페이지용 web 폴더는 ZIP에만 있어요). 아래 표에서 하나씩 받을 수도 있습니다. 파일 이름은 바꾸지 않아도 됩니다. 열어 볼 필요도 없습니다 — 읽는 건 AI입니다.</p>'
        + kit + files + '<p id="tk-msg" class="note" aria-live="polite"></p></section>')
    s2 = ('<section class="section"><h2>2단계 · Claude 프로젝트에 올리기</h2>'
        '<p>Claude의 <strong>프로젝트</strong>는 자료와 지시문을 넣어 두는 폴더입니다. 한 번 올려 두면 그 안에서 여는 모든 채팅이 파일을 이미 읽은 상태로 시작해서, 매번 첨부할 필요가 없습니다.</p>'
        '<ol class="aig-list">'
        '<li>Claude 왼쪽 메뉴의 <strong>프로젝트</strong> 옆 <strong>+</strong>를 눌러 새 프로젝트를 만듭니다. "처음부터 시작"을 고르고 이름을 정합니다(예: "Layer 화면 만들기").</li>'
        '<li>프로젝트 화면의 <strong>지침</strong>을 열고, 아래 AI 안내문을 통째로 붙여넣어 저장합니다. 안내문 오른쪽 위 "복사" 버튼을 쓰면 편합니다.</li>'
        '<li><strong>컨텍스트</strong>에서 추가를 눌러 <strong>압축을 푼 layer-ai-kit-v0.2.1 폴더</strong>를 통째로 넣습니다(web 폴더 포함). 폴더 안 AI 안내문 파일이 같이 들어가도 괜찮습니다. ZIP 파일 그대로는 넣지 않습니다. 넣은 뒤 web 폴더의 <strong>layer.js · layer.css</strong> 두 파일은 빼 주세요 — 크기가 커서 AI가 읽을 자리를 많이 차지하고, 채팅에서는 쓰지 않습니다(같은 내용이 layer-inline.css에 들어 있어요).</li>'
        '<li><strong>메모리 · 예정됨</strong>은 건드리지 않아도 됩니다.</li></ol>'
        + table(['프로젝트 화면에 보이는 메뉴', '안내문은', '파일 3개는'], [
            ['지침 · 컨텍스트 · 메모리 · 예정됨', '<strong>지침</strong>에 붙여넣기', '<strong>컨텍스트</strong>에 압축 푼 폴더 추가'],
            ['프로젝트 지식(Project knowledge) · Set project instructions', '<strong>Set project instructions</strong>에 붙여넣기', '<strong>프로젝트 지식</strong>의 +로 파일 3개 올리기(웹페이지로도 받으려면 web 폴더의 layer-inline.css · layer-icons.js · layer-examples.html도)']])
        + '<p class="note">Claude 화면은 버전마다 메뉴 이름이 다릅니다. 위 표에서 내 화면에 보이는 쪽을 따르세요.</p>'
        + '<details class="ai-raw"><summary>AI 안내문 전체 보기 · 복사</summary>' + code(AI_INSTR) + '</details>'
        + '<div class="callouts"><div class="callout"><span class="chip chip--ok">한 번만 써 볼 때</span><div><p class="cbody">프로젝트를 만들지 않고 새 채팅에 파일 3개를 첨부하고, 첫 메시지 맨 위에 AI 안내문을 붙여넣은 다음 요청을 이어서 써도 됩니다. 다만 채팅을 새로 열 때마다 다시 해야 합니다.</p></div></div></div>'
        + '<p class="note">Claude 도움말: <a href="https://support.claude.com/en/articles/14116274-organize-your-tasks-with-projects-in-claude-cowork" target="_blank" rel="noopener">프로젝트(지침 · 컨텍스트 화면)</a> · <a href="https://support.claude.com/en/articles/9519177" target="_blank" rel="noopener">프로젝트(프로젝트 지식 화면)</a></p></section>')
    s3 = ('<section class="section"><h2>3단계 · 결과를 받을 곳 정하기</h2>'
        '<p>두 가지 중 고릅니다. 둘 다 같은 Layer 컴포넌트로 만들어져서 모양은 같습니다.</p>'
        + table(['', 'Figma에 그리기', '웹페이지(HTML)로 받기'], [
            ['결과', 'Figma 파일 안의 화면(컴포넌트 인스턴스) — 디자이너가 바로 고쳐 쓸 수 있음', '브라우저에서 여는 화면 — 링크로 공유하거나 프로토타입처럼 볼 때'],
            ['준비', '<a href="figma-file.html">커뮤니티 파일 복제</a> + Claude에 Figma 연결 + Figma 유료 플랜(아래)', '없음. ZIP의 web 폴더만 프로젝트에 있으면 됨'],
            ['요청할 때', '"아래 Figma 파일에 그려 줘" + 파일 링크', '"웹페이지(HTML)로 만들어 줘"'],
            ['미리보기', 'Figma 파일에서 바로 확인', '채팅 미리보기는 외부 파일을 막아서, Claude가 layer-inline.css에서 필요한 스타일만 화면 안에 붙여 넣어 바로 보여 줌. HTML 파일로 받으면 고정 주소(jsDelivr) 한 줄(layer.js)로 불러옴. 그래도 스타일이 안 보이면 HTML 파일로 받아 브라우저로 열기']])
        + '<h3>Figma에 그리려면</h3><p>연결해 두면 Claude가 <strong>Figma 파일 안에 실제 Layer 컴포넌트로 화면을 그립니다</strong>.</p>'
        + table(['확인할 것', '내용'], [
            ['연결', 'Claude 설정의 <strong>커넥터(Connectors)</strong>에서 Figma를 찾아 연결하고 Figma 계정으로 로그인합니다.'],
            ['Figma 플랜', 'Figma에 그리기는 Professional 이상 플랜에서 됩니다(현재 베타). 그릴 파일의 편집 권한도 필요합니다.'],
            ['어디에 그릴지', '<a href="figma-file.html">Figma 파일 쓰기</a>에서 받은 <strong>내 복제본 Layer DS 파일</strong>. 컴포넌트가 그 파일 안에 있어서 라이브러리 게시 없이 바로 그릴 수 있습니다. 복제본 링크를 요청 첫 줄에 붙여 줍니다.']])
        + '<p class="note">자세한 조건은 <a href="https://developers.figma.com/docs/figma-mcp-server/write-to-canvas" target="_blank" rel="noopener">Figma 문서: Write to canvas</a>를 확인하세요.</p></section>')
    levels = table(['이렇게 쓰면', '예', '이렇게 나옵니다'], [
        ['<strong>한 줄</strong>', '회고 화면 만들어줘', '어떤 회고 화면인지(홈? 작성? 결과?)를 AI가 고르고, 카드 제목 · 날짜 같은 문구도 지어냅니다. 컴포넌트와 색은 맞지만 기획과 다를 수 있어요. <em>아이디어를 빨리 보고 싶을 때.</em>'],
        ['<strong>기본</strong>', '모바일 회고 홈 화면 그려 줘. 진행 중인 회고 2개, 마감된 회고 1개.', '화면 구조와 카드 상태는 맞습니다. 문구는 여전히 AI가 채워요.'],
        ['<strong>자세히</strong>', '아래 "화면별 요청 예시"처럼 문구와 숫자까지', '거의 그대로 쓸 수 있는 화면. <em>기획서 · 리뷰에 쓸 때 추천.</em>']])
    checklist = table(['', '적을 것', '왜 필요한가요'], [
        ['1', '<strong>모바일인지 웹인지</strong>', '화면 틀(375 / 1440)과 쓰는 컴포넌트가 달라집니다'],
        ['2', '<strong>서비스 안 어디인지</strong> — 하단 탭 "홈", 회고 작성 3번째 질문처럼', '앱 바 모양, 하단 내비게이션 표시, 현재 탭이 정해집니다'],
        ['3', '<strong>화면에 보일 문구와 숫자 그대로</strong>', '빠지면 AI가 지어내거나 컴포넌트 원래 글자(예: 탭 이름 "회고")가 남습니다'],
        ['4', '<strong>상태</strong> — 작성 중 · 제출 완료 · 마감, 선택된 탭, 비어 있음, 에러', '같은 카드라도 상태마다 배지 · 버튼 · 색이 다릅니다'],
        ['5', '<strong>열려 있는 것</strong> — 메뉴, 팝업, 바텀시트', '무엇을 눌러서 열렸는지 쓰면 위치까지 맞춰 그립니다']])
    ex = ''.join(f'<h3>{t}</h3><p>{d}</p>' + code(c) for t, d, c in AI_EXAMPLES)
    s4 = ('<section class="section"><h2>4단계 · 부탁하기</h2>'
        '<p>Layer Skill을 추가했다면 아무 채팅에서나(확실하게 하려면 맨 앞에 <a href="#skill-call">/layer-design-system</a>), 프로젝트 방식이면 프로젝트 안에서 새 채팅을 열고, 어디에 만들지와 어떤 화면인지를 씁니다. 첫 문장은 둘 중 하나로 시작하면 됩니다.</p>'
        + code(AI_FIRST) + code(AI_FIRST_WEB)
        + '<h3>"회고 화면 만들어줘"만 써도 되나요?</h3><p>됩니다. 다만 적은 만큼만 정확해집니다.</p>' + levels
        + '<h3>좋은 요청에 들어가는 다섯 가지</h3><p>전부 쓸 필요는 없지만, 많이 쓸수록 다시 고칠 일이 줄어듭니다. 특히 <strong>3번 문구</strong>가 결과를 가장 크게 바꿉니다.</p>' + checklist
        + '<h3>화면별 요청 예시</h3><p>그대로 복사해서 문구만 바꿔 쓰세요.</p>' + ex
        + '<h3>그린 뒤 고치기</h3><p>한 번에 완벽할 필요는 없습니다. 같은 채팅에서 이어서 말하면 그 화면을 고칩니다.</p>' + code(AI_FIX) + '</section>')
    sx = ('<section class="section" id="explore"><h2>자유롭게 여러 시안을 보고 싶을 때 · 탐색 모드</h2>'
        '<p>기본은 <strong>정확 모드</strong>예요. 레이어 회고 화면을 시스템 그대로 만들어서, 다른 주제를 부탁하면 회고 앱처럼 보일 수 있어요. '
        '아이디어를 넓게 보고 싶거나 회고가 아닌 주제라면 <strong>탐색 모드</strong>로 부탁하세요. 회고가 아닌 주제는 말하지 않아도 탐색 모드로 바뀌어요.</p>'
        + table(['', '정확 모드(기본)', '탐색 모드'], [
            ['언제', '레이어의 실제 화면, 개발에 넘길 시안', '"탐색 모드" · "자유롭게" · "여러 시안" · "아이데이션", 또는 회고가 아닌 주제'],
            ['지키는 것', '규칙 전부', '단위만 — 색 · 글자 · 간격 · 모서리 · 그림자 토큰, 기본 컴포넌트(버튼 · 배지 등), 해요체, 접근성'],
            ['자유로운 것', '—', '레이아웃 · 정보 구성 · 조합, 토큰으로 만든 새 묶음, Layer 스타일의 새 일러스트, 주제 문구'],
            ['결과', '시안 1개', '서로 다른 방향 3개 + 시안마다 콘셉트 한 줄 · 시스템에서 벗어난 부분']])
        + code(AI_EXPLORE)
        + '<h3>이렇게 나와요 — 해외여행 보험 프로모션 시안 3개</h3>'
        '<p>위 요청을 Skill로 부탁해 받은 실제 결과예요. 세 시안 모두 Layer 토큰 · 버튼 · 배지 · 앱 바는 그대로 쓰고, 레이아웃과 정보 구성 · 비주얼을 서로 다르게 풀었어요. 시안마다 위에 <strong>콘셉트</strong>와 <strong>벗어난 부분</strong>(x-로 시작하는 새 묶음)이 적혀 있어요.</p>'
        '<figure class="aig-fig"><a href="examples/explore-insurance.html"><img src="img/ai-explore-insurance.png" alt="탐색 모드 시안 3개: A 정보 중심(요약 상자와 번호 할인 목록), B 비주얼 강조(비행기 · 가방 일러스트 히어로, 탑승권 카드, 할인 도장), C 비교표형(요약 2칸과 할인 비교표 · 막대)" loading="lazy"></a><figcaption>A 정보 중심 · B 비주얼 강조 · C 비교표형</figcaption></figure>'
        + table(['시안', '방향', '새로 만든 묶음(벗어난 부분)'], [
            ['A · 정보 중심', '혜택 · 가격 · 할인을 위에서 아래로 한 줄씩', 'x-facts(요약 상자) · x-discounts(번호 할인 목록)'],
            ['B · 비주얼 강조', '탑승권 · 도장 은유로 떠날 준비의 설렘', 'x-hero + 새 일러스트(비행기 · 가방 · 방패) · x-pass(탑승권 카드) · x-stamps(할인 도장)'],
            ['C · 비교표형', '세 할인을 한 줄에 놓고 막대로 비교', 'x-summary(2칸 요약) · x-table(비교표 + 비율 막대)']])
        + '<p class="note">레퍼런스 캡처를 같이 올리고 "이 구성은 참고하고, 모양은 Layer로"라고 하면 첫 결과부터 원하는 방향에 가까워져요. 마음에 드는 시안의 새 묶음(이름 앞 x-)은 정식 컴포넌트 후보로 모아 두세요.</p>' + '</section>')
    s5 = ('<section class="section"><h2>결과 확인하기</h2>'
        + table(['확인', '어떻게'], [
            ['우리 컴포넌트로 그렸나요?', 'Figma: 레이어 목록에서 카드 · 버튼 아이콘이 ◇(인스턴스)인지 봅니다. 직접 그린 사각형이면 "직접 그리지 말고 Card/Retro (Mobile) 컴포넌트로 바꿔 줘". 웹페이지: 카드 · 버튼이 예시 페이지(ZIP 안 web/layer-examples.html)와 같은 모양인지 봅니다.'],
            ['문구가 요청대로인가요?', '탭 이름 · 배지 · 버튼 글자가 기본 글자로 남지 않았는지 봅니다. Claude가 끝에 알려 주는 "지어낸 문구"도 확인하세요.'],
            ['"부족: …"이라고 했나요?', '디자인 시스템에 아직 없는 요소라는 뜻입니다. 비슷한 컴포넌트로 대신해 달라고 하거나, 시스템에 추가할 후보로 모아 두세요.']])
        + '</section>')
    faq = ('<section class="section"><h2>자주 묻는 질문</h2>'
        + table(['질문', '답'], [
            ['Figma 파일은 어디서 받나요?', '<a href="figma-file.html">Figma 파일 쓰기</a> — 커뮤니티 파일을 내 파일로 복제해서 씁니다. Figma에 그리게 할 때도 이 복제본에 그립니다.'],
            ['Claude 말고 다른 AI도 되나요?', '파일은 일반 텍스트라 다른 AI에게도 줄 수 있습니다. 다만 Figma에 바로 그리려면 그 도구가 Figma 연결을 지원해야 합니다.'],
            ['ChatGPT에서도 쓸 수 있나요?', '네. 가장 쉬운 방법은 <strong>Skill ZIP을 그대로 올리는 것</strong>이에요. '
             '위 방법 A에서 <strong>layer-design-system.zip</strong>을 받아 ChatGPT 새 채팅에 첨부하고, 이렇게 써요: '
             '<em>"이 ZIP을 풀어서 SKILL.md를 읽고, 이 채팅에서는 그 규칙과 references 폴더 자료로 작업해 줘. 첫 요청: 레이어 홈 화면을 모바일 웹페이지로 만들어 줘."</em> '
             'ChatGPT가 ZIP 안의 안내서와 자료를 읽고 같은 규칙(정확 · 탐색 모드, 검수 체크리스트)으로 만들어요. '
             '자주 쓸 때는 ChatGPT <strong>프로젝트</strong> 파일에 이 ZIP을 넣고, 프로젝트 지침에 "항상 layer-design-system.zip의 SKILL.md를 따른다"라고 적어 두면 매번 첨부하지 않아도 돼요. '
             '웹페이지 결과는 캔버스에서 미리 볼 수 있어요. Figma에 직접 그리기는 Claude에서만 됩니다.'],
            ['디자인 시스템이 업데이트되면?', '<a href="updates.html">업데이트</a> 페이지에서 새 버전 파일을 받아, 컨텍스트(또는 프로젝트 지식)의 예전 파일을 새 파일로 바꿉니다. Skill을 쓰면 Skill ZIP을 다시 받아 올립니다.'],
            ['웹과 모바일을 한 번에 부탁해도 되나요?', '됩니다. "같은 내용으로 웹 화면도 그려 줘"라고 이어서 말하면 됩니다.'],
            ['웹페이지 결과를 개발에 그대로 써도 되나요?', '시안 · 프로토타입용입니다. 모양과 클래스는 디자인 시스템과 같지만, 실제 앱 코드(데이터 연결, 동작)는 개발에서 따로 만듭니다.'],
            ['웹페이지가 비슷하지만 조금 달라 보여요', 'Claude에게 "layer-examples.html의 마크업을 그대로 쓰고 컴포넌트 CSS를 새로 쓰지 마"라고 다시 말해 주세요. 부품 모양은 예시 페이지(ZIP 안 web/layer-examples.html)와 같아야 합니다.'],
            ['설계도(JSON)는 뭔가요?', 'Figma 연결이 없을 때 Claude가 주는 "화면 조립 설명서"입니다. 직접 읽거나 쓸 필요는 없습니다. 아래에서 예시를 볼 수 있어요.']])
        + '<details class="ai-raw"><summary>설계도 예시와 용어</summary>' + code(AI_EXAMPLE)
        + table(['말', '뜻'], [
            ['template', '화면의 틀 — 모바일 375 화면, 웹 1440 화면'],
            ['props', '컴포넌트 겉에서 바로 바꾸는 값 — 카드 제목, 목표 문구, 켜고 끄기'],
            ['nested', '컴포넌트 <strong>안에 들어 있는 또 다른 컴포넌트</strong>를 바꾸는 값 — 탭 묶음 안의 "탭 한 칸", 화면 틀 안의 "앱 바"'],
            ['slots', '틀이나 카드 안에 내용을 넣는 빈자리'],
            ['notes', '시스템에 없어서 못 만든 것 — "부족: …"']])
        + '</details></section>')
    result = table(['항목', '1차(보완 전)', '2차(보완 후)'], [
        ['없는 이름 · 토큰', '0건', '0건'],
        ['탭 이름 · 선택', '기본값 그대로', '요청대로'],
        ['칩 · 배지 문구', '블록마다 같은 문구', '블록마다 맞게'],
        ['목록 화면 바탕', '흰 카드가 흰 화면에 묻힘', 'Gray 100 바탕'],
        ['웹 열 머리', '개수를 파란 Badge로', 'Section Header']])
    webres = table(['확인', '결과'], [
        ['컴포넌트 CSS를 새로 썼나', '0줄 — 카드 · 탭 · 앱 바 · LNB · 메뉴 모두 layer.css 클래스 그대로. 직접 쓴 CSS는 배치(쌓기 · 간격)뿐이고 값도 var(--spacing-*)'],
        ['문구 · 숫자', '요청대로(6명 중 3명 → 3 / 6, 열 제목 개수 Section Header). 날짜가 없던 마감 카드 하나만 날짜를 지어냄 — 스스로 알려 줌'],
        ['빈틈 → 고침', '회고 카드 배지 한 자리에 D-day 또는 상태(웹 · 모바일), 웹 카드 Show Description, 설정 목록 한 줄을 .menu-row로 이름 바꿈(2026-11-03)'],
        ['같이 고친 것', '키트 예시에 화면 뼈대(모바일 · 웹)와 Sub 앱 바 추가, 메뉴 위치용 .menu-anchor 추가']])
    s6 = ('<section class="section"><h2>테스트 결과</h2><h3>웹페이지 · 2026-11-03</h3><p>이 대화를 모르는 AI에게 ZIP 키트와 요청서만 주고 "모바일 · 스페이스 회고 목록"과 "웹 · 회고 관리(메뉴 열림)"를 웹페이지로 만들게 했습니다.</p>'
        + '<div class="aig-shots"><figure><img src="img/ai-web-mobile.png" alt="AI가 만든 모바일 회고 목록 웹페이지" loading="lazy"><figcaption>모바일 · 스페이스 회고 목록</figcaption></figure><figure><img src="img/ai-web-web.png" alt="AI가 만든 웹 회고 관리 웹페이지, 첫 카드 메뉴 열림" loading="lazy"><figcaption>웹 · 회고 관리(메뉴 열림)</figcaption></figure></div>'
        + webres
        + '<h3>Figma · 2026-11-02</h3><p>파일 3개와 요청서만 주고 모바일 실행목표 · 웹 회고 관리 · 모바일 개인 분석 화면을 설계하게 했습니다. 결과는 손대지 않고 Figma에 옮겼습니다(Figma Page 1 "AI 생성 테스트" · "2차" 섹션).</p>' + result + '</section>')
    import os
    sk_files = ['downloads/skill/SKILL.md=SKILL.md', 'downloads/skill/checklist.md=references/checklist.md',
        'downloads/DESIGN-v0.2.1.md=references/DESIGN.md', 'downloads/layer-components-v0.2.1.json=references/components.json',
        'downloads/layer-tokens-v0.2.1.json=references/tokens.json', 'kit/layer-inline.css=references/web/layer-inline.css',
        'kit/layer-examples.html=references/web/layer-examples.html', 'kit/layer-icons.js=references/web/layer-icons.js']
    for d in ('logo', 'illustrations'):
        sk_files += [f'kit/{d}/{f}=references/web/{d}/{f}' for f in sorted(os.listdir(R / 'kit' / d))]
    sk = ('<section class="section" id="skill"><h2>Layer Skill 추가하기</h2>'
        '<p><strong>Skill</strong>은 Claude에 한 번 넣어 두는 "작업 안내서 + 자료 묶음"이에요. Layer Skill을 추가하면 프로젝트를 만들거나 파일을 올리지 않아도, '
        '<strong>아무 채팅에서나</strong> "레이어 회고 화면 만들어 줘"라고 하면 Claude가 알아서 Layer 규칙 · 컴포넌트 · 웹 키트를 꺼내 써요. '
        '다 만든 뒤에는 <strong>검수 체크리스트</strong>(틀 · 컴포넌트 · 버튼 · 색 · 문구 · 웹 스타일 빠짐)로 스스로 점검하고 고친 것을 알려 줘요.</p>'
        '<div class="aig-kit"><div><strong>layer-design-system.zip</strong>'
        '<span>SKILL.md(작업 순서) · 검수 체크리스트 · DESIGN.md · components.json · tokens.json · 웹 키트가 들어 있어요. 압축을 풀지 말고 그대로 올립니다.</span></div>'
        '<button type="button" class="btn btn--primary btn--sm" data-dl="" data-dl-name="layer-design-system.zip" data-zip="layer-design-system|' + ','.join(sk_files) + '">Skill 받기</button></div>'
        '<ol class="aig-list">'
        '<li>Claude <strong>설정 → 기능(Capabilities)</strong>에서 <strong>코드 실행 및 파일 생성</strong>이 켜져 있는지 확인합니다. Skill은 이 기능 위에서 돌아가요.</li>'
        '<li>설정 왼쪽 메뉴 아래 <strong>사용자 지정 → Skills</strong>에서 <strong>Skill 업로드</strong>를 누르고, 받은 <strong>layer-design-system.zip</strong>을 고릅니다.</li>'
        '<li><strong>미리보기</strong>에 이름 <strong>layer-design-system</strong>과 설명이 나오면 맞는 파일이에요. <strong>업로드</strong>를 누르면 보안 스캔을 거쳐 추가됩니다.</li>'
        '<li>Skills 목록에 생기고 켜져 있으면 끝. 이제 방법 B(1 · 2단계)는 건너뛰고 <a href="#s3">3단계</a>로 가서 받을 곳을 정하고 부탁하면 됩니다.</li></ol>'
        '<figure class="aig-fig"><img src="img/skill-upload.png" alt="Claude 설정의 Skill 업로드 화면. layer-design-system.zip을 고르면 미리보기에 이름과 설명, 보안 스캔이 보이고 아래에 업로드 버튼이 있다" loading="lazy"><figcaption>Skill 업로드 화면 — 미리보기에 이름 · 설명이 보이면 업로드를 누릅니다</figcaption></figure>'
        '<h3 id="skill-call">Skill 부르기 — 확실하게 쓰고 싶을 때</h3>'
        '<p>Skill은 요청에 "레이어 · Layer"가 들어 있으면 Claude가 알아서 꺼내 써요. 그런데 <strong>보험 · 쇼핑처럼 레이어와 상관없는 주제</strong>를 부탁하거나, 꼭 이 Skill로 만들게 하고 싶을 때는 '
        '채팅창에 <strong>/</strong>를 입력하고 <strong>layer-design-system</strong>을 골라 부르세요. 그 뒤에 이어서 요청을 쓰면 됩니다.</p>'
        '<figure class="aig-fig aig-fig--sm"><img src="img/skill-slash.png" alt="채팅 입력창에 /layer-design-system 을 입력한 모습" loading="lazy"><figcaption>채팅창에 /layer-design-system 입력</figcaption></figure>'
        + code(AI_SLASH)
        + table(['확인할 것', '내용'], [
            ['플랜', 'Pro · Max · Team · Enterprise에서 쓸 수 있어요. Enterprise는 관리자가 Skills를 켜 둬야 해요.'],
            ['팀원과 함께 쓰기', 'Skill은 내 계정에만 들어가요. 팀원은 각자 같은 ZIP을 올리면 됩니다(Team · Enterprise 관리자는 조직 전체에 한 번에 넣을 수 있어요).'],
            ['업데이트', '새 버전이 나오면 Skill을 다시 받아 같은 방법으로 올립니다. Skill 안에 자료가 없을 때는 GitHub 최신본을 읽도록 되어 있어요.'],
            ['개발 도구에서 쓰기', 'Claude Code · Cursor · Codex처럼 컴퓨터 터미널에서 쓰는 AI라면 ZIP 대신 명령어 한 줄로 설치합니다(Node.js 필요): <code>npx skills add Nakyeonng/layer-ds --skill layer-design-system</code>. 업데이트는 <code>npx skills update</code>.'],
            ['프로젝트와 같이 써도 되나요?', '네. 다만 같은 자료가 두 번 들어가니 Skill을 쓰면 프로젝트의 Layer 파일은 빼도 돼요.']])
        + '<p class="note">Claude 도움말: <a href="https://support.claude.com/en/articles/12512180-using-skills-in-claude" target="_blank" rel="noopener">Using Skills in Claude</a> · Skill을 못 쓰는 환경이면 아래 방법 B(프로젝트)로 하세요.</p></section>')
    s3 = s3.replace('<section class="section"><h2>3단계', '<section class="section" id="s3"><h2>3단계', 1)
    choose = ('<div class="path-choose">'
        '<a class="path-card path-card--a" href="#skill"><span class="path-tag path-tag--a">방법 A · 추천</span><strong>Layer Skill 추가</strong><span>ZIP 하나 올리면 끝 → 3 · 4단계</span></a>'
        '<a class="path-card" href="#path-b"><span class="path-tag">방법 B</span><strong>프로젝트로 쓰기</strong><span>Skill을 못 쓸 때만 → 1 · 2 · 3 · 4단계</span></a></div>')
    box_a = ('<div class="path-box path-box--a"><div class="path-box__head"><span class="path-tag path-tag--a">방법 A · 추천</span>'
        '<strong>Skill로 쓰기</strong><span class="path-box__skip">끝나면 <a href="#s3">3단계로 →</a></span></div>' + sk + '</div>')
    box_b = ('<div class="path-box" id="path-b"><div class="path-box__head"><span class="path-tag">방법 B</span>'
        '<strong>프로젝트로 쓰기 — Skill을 못 쓸 때만</strong><span class="path-box__skip">Skill을 추가했다면 건너뛰고 <a href="#s3">3단계로 →</a></span></div>'
        '<p class="path-box__why">무료 플랜이거나, 회사 계정에서 코드 실행 · Skills가 막혀 있을 때 이 방법을 씁니다.</p>' + s1 + s2 + '</div>')
    join = '<div class="path-join"><span>여기부터 A · B 공통</span></div>'
    return content + strip + choose + box_a + box_b + join + s3 + s4 + sx + s5 + faq + s6

def p_figma_file():
    COMM = "https://www.figma.com/community/file/1699490552460986431/layer-ds"
    content = page_head('시작하기', 'Figma 파일 쓰기', 'Layer Design System의 Figma 파일은 Figma 커뮤니티에 공개되어 있습니다. 누구나 복제해서 내 파일로 가져갈 수 있고, 그 안의 컴포넌트 · 변수 · 스타일을 그대로 써서 화면을 만들 수 있습니다. 무료(Starter) 플랜에서도 됩니다.', status=('ok', 'v0.2.1'))
    hero = ('<div class="aig-kit"><div><strong>Layer DS · Figma 커뮤니티 파일</strong>'
            '<span>컴포넌트 82개 · 변수 116개 · 텍스트 스타일 22개 · 화면 틀 2종 · 예시 화면 16장</span></div>'
            f'<a class="btn btn--primary btn--sm" href="{COMM}" target="_blank" rel="noopener">커뮤니티에서 열기</a></div>')
    strip = ('<ol class="aig-steps">'
        '<li><b>1</b><strong>파일 열기</strong><span>커뮤니티 페이지</span></li>'
        '<li><b>2</b><strong>내 파일로 복제</strong><span>Open in Figma</span></li>'
        '<li><b>3</b><strong>틀에서 시작</strong><span>Templates 인스턴스</span></li>'
        '<li><b>4</b><strong>컴포넌트로 채우기</strong><span>Assets 패널</span></li></ol>')
    s1 = ('<section class="section"><h2>1 · 내 파일로 복제하기</h2>'
          '<ol class="aig-list">'
          f'<li>위 버튼으로 <a href="{COMM}" target="_blank" rel="noopener">커뮤니티 파일</a>을 엽니다. Figma에 로그인되어 있어야 합니다.</li>'
          '<li><strong>Open in Figma</strong>(또는 Duplicate)를 누르면 내 <strong>Drafts</strong>에 복제본이 생깁니다. 이 복제본이 이제 내 파일입니다.</li>'
          '<li>팀과 같이 쓰려면 복제본을 팀 폴더로 옮기고 팀원을 편집자로 초대합니다. 무료 플랜은 팀 폴더에 디자인 파일을 3개까지 둘 수 있고, Drafts에 초대한 사람은 보기만 할 수 있습니다.</li></ol>'
          + '<div class="callouts"><div class="callout"><span class="chip chip--ok">왜 복제하나요</span><div><p class="cbody">무료 플랜은 라이브러리를 게시하거나 다른 파일에서 켤 수 없습니다. 대신 복제본 안의 컴포넌트는 그 파일의 로컬 컴포넌트라서, 같은 파일 안에서는 라이브러리 없이 인스턴스로 그대로 씁니다.</p></div></div></div></section>')
    s2 = ('<section class="section"><h2>2 · 파일 둘러보기</h2><p>왼쪽 페이지 목록이 문서 목차입니다. 이 사이트와 같은 순서입니다.</p>'
          + table(['페이지', '내용'], [
              ['📘 Cover · 🚀 시작하기', '표지, 소개 · 쓰는 법 · 코드와 AI · 버전'],
              ['BRAND', 'Logo · Illustration(20)'],
              ['FOUNDATIONS', 'Color · Typography · Spacing · Radius · Elevation · Layout · Iconography · State — 견본이 변수 · 스타일에 연결되어 있음'],
              ['COMPONENTS (25페이지)', '페이지마다 설명 → 원본 컴포넌트 → 속성 → 안쪽 요소(nested) → 스펙 → 쓰지 않을 때 → 코드 클래스'],
              ['📐 Templates', 'Template/Mobile(Background) · Template/Web(Type=List · Work) — 모든 새 화면의 시작점'],
              ['📱 예시 화면', '서비스 대표 화면(모바일 8 · 웹 8), AI 생성 테스트']]) + '</section>')
    s3 = ('<section class="section"><h2>3 · 화면 만들기</h2>'
          + table(['순서', '하는 일', '팁'], [
              ['새 페이지', '복제본에 페이지를 하나 만듭니다(예: "내 시안")', '문서 페이지 안에는 작업하지 않습니다'],
              ['틀 놓기', 'Assets 패널에서 <code>Template/Mobile</code> 또는 <code>Template/Web</code>을 끌어옵니다', '앱 바 제목 · 현재 탭은 인스턴스를 더블클릭해 안쪽에서 바꿉니다'],
              ['슬롯 채우기', 'Content(웹 Work는 List · Panel) 슬롯에 카드 · 목록 · 버튼 컴포넌트를 넣습니다', '묶음은 오토 레이아웃 + spacing 변수'],
              ['글자 · 상태', '오른쪽 속성 패널에서 Title · Count · Status 같은 속성으로 바꿉니다', '컴포넌트 기본 글자가 남지 않게'],
              ['값', '색은 역할 토큰(text · bg · border), 글자는 텍스트 스타일, 간격은 spacing 변수', '색 코드를 직접 넣지 않습니다']], ) 
          + '<div class="callouts"><div class="callout"><span class="chip chip--ok">하지 말 것</span><div><p class="cbody">인스턴스를 Detach하거나 도형으로 다시 그리지 않습니다. 원본 컴포넌트를 고치면 복제본 안의 모든 화면이 함께 바뀌니, 원본 수정은 문서 페이지에서 신중하게 합니다.</p></div></div></div></section>')
    s4 = ('<section class="section"><h2>4 · 다른 파일에서 쓰려면</h2>'
          + table(['내 플랜', '방법'], [
              ['무료(Starter)', '복제본 파일 안에서 페이지를 늘려 작업합니다. 프로젝트마다 커뮤니티 파일을 새로 복제해 템플릿처럼 시작해도 됩니다.'],
              ['유료(Professional 이상)', '복제본을 팀 라이브러리로 게시하고(Assets → 라이브러리 → Publish), 작업 파일에서 그 라이브러리를 켭니다. 이후 원본을 고치면 업데이트로 받을 수 있습니다.']]) + '</section>')
    s5 = ('<section class="section"><h2>5 · 업데이트 받기</h2><p>커뮤니티 파일을 고쳐도 이미 복제한 파일은 바뀌지 않습니다. 새 버전은 <a href="updates.html">업데이트</a>에서 확인하고, 필요하면 커뮤니티 파일을 다시 복제해 새 파일에서 이어 작업합니다. 지금 버전은 표지와 시작하기 페이지에 적혀 있습니다.</p></section>')
    s6 = ('<section class="section"><h2>AI로 화면 만들기와 함께 쓰기</h2><p>Claude에게 Figma에 그려 달라고 할 때, 그릴 곳은 <strong>이 복제본 파일</strong>입니다. 컴포넌트가 그 파일 안에 있어서 라이브러리 없이 바로 인스턴스로 그립니다.</p>'
          + table(['', '할 일'], [
              ['1', '위 방법으로 커뮤니티 파일을 복제하고, 복제본의 공유 링크(Share → Copy link)를 복사합니다'],
              ['2', '<a href="ai-guide.html">AI로 화면 만들기</a>대로 Claude 프로젝트에 키트 파일과 AI 안내문을 넣고, Claude에 Figma를 연결합니다'],
              ['3', '요청 첫 줄에 "아래 Figma 파일에 새 페이지를 만들고 그려 줘" + 복제본 링크를 붙입니다'],
              ['4', 'Claude는 components.json의 이름 · 위치로 복제본 안의 컴포넌트를 찾아 인스턴스로 놓습니다']])
          + code('아래 Figma 파일에 새 페이지를 만들고, 다음 화면을 그려 줘.\nhttps://www.figma.com/design/(내 복제본 파일)/...\n\n모바일 · 스페이스 "떡잎마을방범대" 회고 목록\n…')
          + '<div class="callouts"><div class="callout"><span class="chip chip--ok">무료 플랜이라면</span><div><p class="cbody">Figma 문서 기준으로 AI가 Figma 파일에 직접 그리는 기능은 유료 플랜(Professional 이상)에서 되고, 무료 좌석은 AI가 Figma를 읽는 횟수도 한 달 20번으로 제한됩니다. 무료 플랜이면 AI 시안은 <a href="ai-guide.html">웹페이지로 받기</a>를 쓰고, 마음에 드는 시안을 복제본에서 컴포넌트로 옮겨 다듬는 흐름을 추천합니다.</p></div></div></div></section>')
    return content + hero + strip + s1 + s2 + s3 + s4 + s5 + s6

def p_updates():
    log = [
        ['2026-11-05', '<a href="ai-guide.html">AI로 화면 만들기</a>', '자주 묻는 질문에 "ChatGPT에서도 쓸 수 있나요?" 추가 — Skill ZIP을 채팅에 올려 그대로 적용하는 법, 자주 쓸 때는 프로젝트에 넣기', '코드'],
        ['2026-11-04', '문서 사이트', 'GitHub Pages로도 공개 — <a href="https://nakyeonng.github.io/layer-ds/" target="_blank" rel="noopener">nakyeonng.github.io/layer-ds</a>(로그인 없이 열리는 고정 주소, llms.txt 포함). README에 링크', '코드'],
        ['2026-11-04', '<a href="ai-guide.html#skill-call">AI로 화면 만들기</a>', 'Skill 업로드 화면 캡처 · 넣는 순서를 실제 메뉴(사용자 지정 → Skills → Skill 업로드)로 고침. Skill 부르기(/layer-design-system) 안내 추가. 탐색 모드에 실제 결과(해외여행 보험 시안 3개) 예시 추가', '코드'],
        ['2026-11-04', '<a href="ai-guide.html#explore">AI로 화면 만들기</a> · Skill', '탐색 모드 추가 — 정확 모드(기본, 규칙 전부)와 탐색 모드(토큰 · 기본 컴포넌트 · 해요체 · 접근성만 지키고 레이아웃 · 조합 · 새 묶음 · 일러스트는 자유, 서로 다른 시안 3개 + 벗어난 부분 표시). 회고가 아닌 주제는 자동으로 탐색 모드, 회고 전용 요소 제외. Skill · DESIGN.md · AI 안내문 · 검수 체크리스트에 반영', '코드'],
        ['2026-11-04', '<a href="ai-guide.html#skill">AI로 화면 만들기</a> · Skill', 'Layer Skill(layer-design-system.zip) 추가 — Claude 설정 → 기능 → Skills에 한 번 올리면 프로젝트 없이 아무 채팅에서 Layer 화면 만들기. 작업 순서(준비 → 설계 → 그리기 → 검수 → 알려 주기)와 검수 체크리스트(틀 · 컴포넌트 · 버튼 · 겹침 · 색 · 내용 · 웹 스타일 빠짐 · Figma) 포함. AI 안내문에도 검수 단계 추가. GitHub skill/ 폴더', '코드'],
        ['2026-11-04', '<a href="ai-guide.html">AI로 화면 만들기</a> · 웹 키트', 'Claude 채팅 미리보기가 외부 스크립트(jsDelivr)를 막아 스타일이 빠지던 문제 대응: 붙여 넣기용 <code>layer-inline.css</code> 추가(기본 + 클래스 이름별 부품, 압축). AI는 화면에 쓴 부품만 &lt;style&gt;에 넣고 아이콘 · 로고는 SVG를 직접 넣음. layer.js 한 줄은 HTML 파일 · 사이트용으로. 프로젝트에는 layer.js · layer.css를 빼고 올리도록 안내', '코드'],
        ['2026-11-04', '<a href="ai-guide.html">AI로 화면 만들기</a> · GitHub', '웹 키트를 GitHub(Nakyeonng/layer-ds) + jsDelivr 고정 주소로 공개 — 채팅 미리보기 · 공유용 HTML에서도 레이어 스타일이 그대로 적용. AI 안내문 · DESIGN.md · components.json에 고정 주소, 저장소에 다시 만드는 스크립트(build_all.sh) · 사용 조건(LICENSE.md). 보안 정리: 예시 이름을 가상 이름으로, 공개 파일에서 원본 Figma 파일 주소 삭제, Pretendard 라이선스(OFL) 동봉', '코드'],
        ['2026-11-04', '<a href="popover.html">Popover · Menu</a> · <a href="lists.html">Lists</a>', 'List/Member Item "팀원 추가"의 + 아이콘이 동그라미 왼쪽 위로 치우치던 문제 수정(아이콘 칸 24 → 16, 가운데 정렬). 웹 키트 layer.css에도 반영', '코드'],
        ['2026-11-04', '<a href="ai-guide.html">AI로 화면 만들기</a> · <a href="tokens.html">Tokens</a>', '받기 칸의 "열기" · "예시 보기" 링크 숨김(공유 링크에서는 파일을 새 창으로 열 수 없음). 다운로드 버튼만 남김, 웹 키트 예시는 ZIP 안 web/layer-examples.html', '코드'],
        ['2026-11-04', '모든 문서 페이지', '페이지 머리의 Figma 링크를 비공개 원본 파일에서 <a href="https://www.figma.com/community/file/1699490552460986431/layer-ds" target="_blank" rel="noopener">Figma 커뮤니티 파일</a>로 바꿈(누구나 열 수 있음)', '코드'],
        ['2026-11-04', '<a href="figma-file.html">Figma 파일 쓰기</a>', '새 페이지: Figma 커뮤니티 파일(Layer DS) 복제 · 둘러보기 · 화면 만들기 · 다른 파일에서 쓰기(무료 · 유료) · 업데이트 받기 · AI로 화면 만들기와 함께 쓰기. AI로 화면 만들기의 "어디에 그릴지"를 내 복제본 파일로, AI 안내문 · components.json에 복제본에서 컴포넌트 찾는 규칙', '코드'],
        ['2026-11-04', 'Figma 파일', '외부 공유용으로 Figma 문서 정리: 페이지 44개(Cover · 시작하기 · Brand 2 · Foundations 8 · Components 25 · Templates · 예시 화면 · 보관). 컴포넌트 페이지마다 설명 → 원본 컴포넌트 → 속성 → 안쪽 요소 → 스펙 → 쓰지 않을 때 → 코드 클래스, Foundations는 변수 · 스타일에 연결된 견본. 원본 컴포넌트 전부를 문서 페이지로 옮김(끊긴 인스턴스 0), 정리 전 보드는 보관 페이지에', 'Figma'],
        ['2026-11-03', '<a href="cards.html">Cards</a> · <a href="lists.html">Lists</a>', '회고 카드 배지를 한 자리로: D-day <em>또는</em> 상태 하나만. 웹 — 작성 전 + 마감일 있음은 D-day(Badge Blue, 배지 노출 인스턴스 Label), 나머지는 상태. 모바일 — 새 속성 Progress(Before D-day · Writing 작성 중 · Submitted 제출 완료), 버튼 문구 규칙(회고 작성 · 회고 확인 · 분석 확인). 웹 카드 Show Description. 설정 목록 한 줄 CSS .menu-item → .menu-row(메뉴 Menu Item과 이름 겹침 해소)', 'Figma, 코드'],
        ['2026-11-03', '<a href="ai-guide.html">AI로 화면 만들기</a> · <a href="tokens.html">Tokens</a>', 'v0.2.1: 웹페이지(HTML)로도 받을 수 있게 웹 키트 추가 — layer.css(토큰 · 컴포넌트 스타일 한 파일) · layer-icons.js(아이콘 72, data-icon) · layer-examples.html(컴포넌트 72개 실제 마크업 + 화면 뼈대). 새 CSS: LNB(펼침 · 접힘) · Section Header · Logo · OS Bar · .layout-mobile--secondary · .menu-anchor. components.json에 코드 클래스 8개 · code.example · web 규칙, DESIGN.md에 Web (HTML), llms.txt · llms-full.txt. 가이드 3단계를 "받을 곳 정하기(Figma · 웹페이지)"로, ZIP에 web 폴더, 웹페이지 생성 테스트 결과', '코드'],
        ['2026-11-03', '<a href="ai-guide.html">AI로 화면 만들기</a>', '파일 4개를 한 번에 받는 ZIP(layer-ai-kit-v0.2.0.zip) 추가. 2단계를 지금 Claude 프로젝트 화면(지침 · 컨텍스트 · 메모리 · 예정됨) 기준으로 고침', '코드'],
        ['2026-11-03', '<a href="ai-guide.html">AI로 화면 만들기</a>', '처음 쓰는 사람 기준으로 다시 씀: 4단계(파일 받기 → Claude 프로젝트에 올리기 → Figma 연결 → 부탁하기), 한 줄 · 기본 · 자세히 요청 비교, 좋은 요청 다섯 가지, 화면별 요청 예시 4개, 고치기 예시, 결과 확인, 자주 묻는 질문. 요청서 양식 대신 AI 안내문(프로젝트 지침에 붙여넣기)', '코드'],
        ['2026-11-03', '<a href="ai-guide.html">AI로 화면 만들기</a>', '새 페이지(요청서는 평소 말로 쓰는 형식): 준비할 파일 · 설계 순서(템플릿 → nested → 슬롯 → 속성 · nested 문구 → 토큰) · 요청서 양식(다운로드) · 출력 JSON 예시 · 확인 규칙 · 테스트 1 · 2차 결과', '코드'],
        ['2026-11-03', '<a href="tokens.html">Tokens</a>', 'v0.2.0 배포: tokens.json · DESIGN.md · components.json v0.2.0, 업데이트 페이지에 버전 요약 · 호환되지 않는 변경 정리', '코드'],
        ['2026-11-03', '<a href="popover.html">Popover · Menu</a>', 'Popover · Menu 뒤 딤드를 없앰(드롭다운 · 더보기 모두 그림자로만). overlay/dim-popover 토큰 · Figma 변수 삭제, 웹 08 화면 딤드 제거. 딤드는 모달 계열(overlay/dim)만', 'Figma, 코드'],
        ['2026-11-02', 'AI 생성 테스트 보완', 'Card/Retro (Web)에 Title · Description · Date · Count · Total 텍스트 속성(기존 화면 1,331개 인스턴스 글자 유지), Template/Mobile에 Background=Surface · Secondary, 새 컴포넌트 Section Header(Size=16 · 18), Card/Goal (Mobile) 빈 상태 노출. components.json에 nested(안쪽에서 바꾸는 인스턴스: 탭 이름, 배지 · 칩 문구, 앱 바 · 내비게이션 · LNB) 추가', 'Figma, 코드'],
        ['2026-11-02', '전체 컴포넌트', '쓰이지 않던 Component 18(실행목표 상태 드롭다운) · Tags/Tag(옛 이름표 → Badge Gray)를 컴포넌트에서 해제해 디자인으로만 남김. components.json에서 제외', 'Figma, 코드'],
        ['2026-11-02', '정합성 점검', 'LNB 구분선 · 프로필 글자를 변수 · Body 13 Medium에 연결, Card/Retro (Web) 날짜 구분선을 Gray 400 변수에, 직접 그린 Person 아이콘 2개를 인스턴스로. 문서의 옛 표기(Toast Caution Red 400, App Bar/Text Button, Template/Web List · Work) 정리, Empty State 속성 키 갱신', 'Figma, 코드'],
        ['2026-10-30', '<a href="analysis.html">Analysis</a>', '새 페이지 · 새 보드 Components · Analysis: Section Title · Progress Panel · Satisfaction(도넛 + 범례) · Goal Rate(막대 + 말풍선) · Keyword Group · Keyword Item(Good · Bad · Improve × Web · Mobile) · Highlight Title. CSS analysis.css', 'Figma, 코드'],
        ['2026-10-30', '대표 화면 · 웹 04 회고 완료 분석', '직접 그린 분석 영역(그룹) → Analysis/Section Title + Progress Panel + Keyword Group 3열', 'Figma'],
        ['2026-10-30', '<a href="cards.html">Cards</a>', '새 컴포넌트 Card/Template(Type=Default · Custom × Platform=Web · Mobile, Show Button · Illustration), Card/Template Detail(Size=335 · 240), Card/Template Summary(질문 슬롯). CSS .template-card · .template-detail · .template-summary', 'Figma, 코드'],
        ['2026-10-30', '<a href="lists.html">Lists</a> · <a href="button.html">Button</a>', 'List/Icon List에 Action=None · Marker=Number 추가. Outlined Button에 Icon 속성 추가, Size 40 아이콘을 Show Icon에 연결', 'Figma'],
        ['2026-10-30', '대표 화면 · 웹 06 템플릿 리스트', '직접 짠 템플릿 카드 6장 → Card/Template(Default · Web) 인스턴스', 'Figma'],
        ['2026-10-30', '<a href="cards.html">Cards</a>', 'Card/Answer를 Platform(Mobile · Web) × Type(Text · Emotion · Score) 세트로, Show Name 추가. 새 부품 Answer/Emotion Scale · Answer/Score Bar, 새 컴포넌트 Card/Question Group (Web)(질문 + 답 슬롯). CSS .answer-card--web · .emotion-scale · .score-bar · .question-group', 'Figma, 코드'],
        ['2026-10-30', '<a href="cards.html">Cards</a>', '새 컴포넌트 Card/Goal (Mobile)(흰 카드 335 · Title 18 · Body 16 · Badge Outlined Blue로 통일 · More 세로 점 · Show Empty). Card/Goal (Web)·(Mobile)에 Show Items(목표 없는 카드). Card/Retro (Mobile) 더보기를 오른쪽 끝에 붙임. CSS .goal-card--mobile', 'Figma, 코드'],
        ['2026-10-30', '<a href="cards.html">Cards</a>', 'Card/Retro (Mobile)에 Status=Open · Closed(마감 회고: Gray 100 · 기간 표기 · 분석 확인 Primary) · Show Description · Period 추가 (Page 2 회고 관리 · 스페이스 상세 카드)', 'Figma, 코드'],
        ['2026-10-29', '<a href="layout.html">Layout</a>', 'Template/Web List · Web Work를 Template/Web 하나(Type=List · Work)로 합침. 새 웹 형태는 Type을 추가해 수용하는 규칙 추가', 'Figma, 코드'],
        ['2026-10-29', '<a href="layout.html">Layout</a>', '새 페이지. 템플릿 3종(Template/Web List · Web Work · Mobile, 슬롯), 그리드 스타일 Layout/Mobile 375 · Web List · Web Work, Figma 변수 모음 Layout 9개. 기준 기기 375 × 812 확정. CSS layout.css', 'Figma, 코드'],
        ['2026-10-29', '대표 화면 · 웹 02 · 05~08', 'Web/List로: 본문 여백 68(28 + 40 겹침) → 40, 열 사이 40을 layout/margin-list에 연결, 그리드 스타일 연결. 08 팝오버 위치를 옮긴 버튼에 맞춤', 'Figma'],
        ['2026-10-29', '대표 화면 · 웹 03 · 04', 'Web/Work로: 접은 LNB 뒤 18 → 20, 목록과 패널 사이 30 → 20, 작업 패널 안쪽 좌우 → 40(layout/panel-padding), 그리드 스타일 연결', 'Figma'],
        ['2026-10-29', '대표 화면 · 모바일 01~08', '그리드 스타일 Layout/Mobile 375 연결(직접 걸린 그리드 제거)', 'Figma'],
        ['2026-10-29', '<a href="avatar.html">Avatar</a>', 'Size 24 → 28(24는 너무 작아 보여서). 24는 LNB에서만 쓰여 일괄 변경. LNB 접힘(Fold=On)의 직접 그린 프로필도 Profile 28 인스턴스로 교체. CSS .avatar--24 → .avatar--28', 'Figma, 코드'],
        ['2026-10-29', '<a href="navigation-bar.html">Navigation Bar</a>', 'OS Bar 시스템 부품(Time · Home Indicator)은 플랫폼 키트 원격 인스턴스를 그대로 쓰는 예외로 확정(교체 · 토큰 연결 안 함)', '코드'],
        ['2026-10-29', '<a href="color.html">Color</a>', 'text/error · status/error를 Red 400 → Red 500으로(오류 · 위험 색 하나로, 입력 오류 안내도 Red 500). overlay/dim-popover(Opacity 32) 추가: 팝오버 · 메뉴 뒤 딤드는 모달(72)보다 얕게', 'Figma, 코드'],
        ['2026-10-29', '<a href="popover.html">Popover · Menu</a>', '새 컴포넌트 Popover(제목 · 개수 · 편집 · Content 슬롯), Menu(Items 슬롯) + Menu/Menu Item(Default · Danger × Default · Hover). CSS .popover · .menu · .menu-item', 'Figma, 코드'],
        ['2026-10-29', '<a href="popover.html">List/Member Item</a>', '새 컴포넌트 List/Member Item(Type=Add · Member). CSS .member-item', 'Figma, 코드'],
        ['2026-10-29', '<a href="avatar.html">Avatar</a>', 'Profile에 Show Leader(대표자 왕관) 추가, 모든 크기. CSS .avatar-leader', 'Figma, 코드'],
        ['2026-10-29', '<a href="button.html">Button</a>', 'Button/Text Button을 App Bar 문서에서 Button 문서(Text Buttons 섹션)로 옮김', 'Figma'],
        ['2026-10-29', '대표 화면 · 웹 08 멤버관리', '본문 → 웹 02 정리본, 남은 프레임 삭제, 팀원 버튼 → Dropdown(Team · Pressed), 인원 패널 → Popover + List/Member Item(대표자 Show Leader), 더보기 → Menu(대표자 변경 Hover · 팀원 삭제 Danger), 딤드 → overlay/dim-popover', 'Figma'],
        ['2026-10-29', '<a href="lists.html">Lists</a>', 'List/Icon List에 Action=None · Marker=Star(★ 고정 질문) 추가, Number · Text 속성으로 번호와 문구를 인스턴스에서 바꿈. CSS .list-card--fixed · .num-badge--star', 'Figma, 코드'],
        ['2026-10-29', '<a href="button.html">Button</a>', 'Filled Button에 Show Label 추가(아이콘만 있는 버튼). App Bar/Text Button을 Button/Text Button으로 옮기고 Type=Accent · Neutral(Body 14 Medium Gray 500) 합침. CSS .btn--icon-only · .text-button', 'Figma, 코드'],
        ['2026-10-29', '<a href="popup.html">Popup</a>', 'Modal (Web)에 Show Back(제목 앞 뒤로 가기) 추가', 'Figma, 코드'],
        ['2026-10-29', '대표 화면 · 웹 07 질문 리스트', 'LNB · 본문 → 인스턴스 + 웹 02 본문, 모달 → Modal (Web)(뒤로 가기 · 제목 · 완료 버튼), 질문 줄 → List/Icon List(사전 질문 None · Star, 메인 질문 Reorder · Number), 추가 버튼 → Button 40 Light Blue 아이콘만, 삭제 → Text Button Neutral, 소제목 Subtitle 16 SemiBold · 안내 Body 14 Medium Gray 500, 딤드 토큰 연결', 'Figma'],
        ['2026-10-29', '<a href="iconography.html">Iconography</a>', '새 아이콘 Info_Filled(채운 원 정보). Info Banner 기본 아이콘을 Info(테두리)에서 Info_Filled로', 'Figma, 코드'],
        ['2026-10-29', '<a href="tooltip.html">Tooltip</a>', 'Info Banner의 직접 그린 아이콘을 Icon/Assets/Info 인스턴스로 바꾸고 Icon 교체 속성 추가', 'Figma, 코드'],
        ['2026-10-29', '<a href="typography.html">Typography</a>', 'Title 22 Bold(웹 모달 제목) · Title 14 Bold(웹 소제목 · 접기 제목 · 이전/다음 · 템플릿 카드) 추가, 22개. Accordion/Section (Web) · Button/Pager · 웹 04 소제목을 Title 14 Bold로 다시 연결', 'Figma, 코드'],
        ['2026-10-29', '<a href="popup.html">Popup</a>', 'Modal (Web)에 Title · Show Title · Show Footer 추가(목록형 모달). 제목이 없어도 닫기는 오른쪽', 'Figma, 코드'],
        ['2026-10-29', '<a href="tooltip.html">Tooltip</a>', '새 컴포넌트 Info Banner(Gray 200 한 줄 안내). CSS .info-banner', 'Figma, 코드'],
        ['2026-10-29', '대표 화면 · 웹 06 템플릿 리스트', '직접 짠 LNB · 본문 → LNB 인스턴스 + 정리된 웹 02 본문, 모달 → Modal (Web)(제목 · 버튼 없음 · 바탕 Gray 100), 탭 → Text Tabs 14 + 구분선, 안내 → Info Banner, 카드 태그 → Badge Gray 22, 카드 그림 → 라이브러리 Retro 일러스트, 카드 제목 Title 14 Bold, 딤드 · 색 토큰 연결', 'Figma'],
        ['2026-10-29', '<a href="popup.html">Popup</a>', 'Modal (Web) 아래 버튼 영역 아래 여백 16 → 24', 'Figma, 코드'],
        ['2026-10-29', '<a href="popup.html">Popup</a>', '새 컴포넌트 Modal (Web)(520 × 652, 모서리 20, 닫기 · 단계 막대 · Content 슬롯 · 버튼 48 두 개). 새 토큰 radius/20 · radius/modal-lg. CSS .modal', 'Figma, 코드'],
        ['2026-10-29', '<a href="progress-bar.html">Progress Bar</a>', '여백 0 · 너비 채움으로 바꿔 모바일 · 웹 공통. 모바일 사용처 6곳은 감싸는 프레임(위 8 · 좌우 20 · 아래 20)으로 위치 유지', 'Figma, 코드'],
        ['2026-10-29', '<a href="button.html">Button</a>', '규칙: 웹 모달 아래 버튼은 48', '코드'],
        ['2026-10-29', '대표 화면 · 웹 05 회고 이름 설정', '모달 → Modal (Web) 인스턴스(Content 슬롯에 질문 · 입력을 넣음, 다음 Disabled), 입력창 · 툴팁 · 닫기 · 버튼을 로컬로, 뒤 배경을 정리된 웹 02 본문 복제로 교체, 딤드 → overlay/dim, 화면 밖 프레임 삭제', 'Figma'],
        ['2026-10-29', '<a href="tabs.html">Tabs</a>', 'Text 탭 통합: 모바일 Tabs/Text Tabs(7변형)와 Tabs/Text Tabs (Web)(6변형)을 하나의 Tabs/Text Tabs(Size=18 · 14, 2변형)로. 칸 수는 Show Tab 3 · 4, 구분선은 Show Divider. 웹 기준 값: 높이 40 · 여백 0 · 탭 간격 18은 8(이전 모바일 12) · 14는 4. 사용처 13곳 교체 — 모바일은 감싸는 프레임(위 12 · 좌우 20)으로 위치 유지. CSS .tabs 기본값 변경, .tabs--sm(.tabs--web 호환)', 'Figma, 코드'],
        ['2026-10-29', '<a href="tabs.html">Tabs</a>', 'Tabs/Text Tabs (Web)에 Size(14 · 18) · Outline(Off · On) 추가. 웹 04 상세 패널 위 질문 · 개별 · 분석을 낱개 탭에서 이 묶음(Item=3 · Size=18 · Outline=On)으로 교체. CSS .tabs--web-lg', 'Figma, 코드'],
        ['2026-10-29', '<a href="tabs.html">Tabs</a>', '새 컴포넌트 Segmented Control(Item=2 · 3) + Segmented Control/Item(Selected · Unselected · Hover). CSS .segmented', 'Figma, 코드'],
        ['2026-10-29', '<a href="iconography.html">Iconography</a>', '새 아이콘 Minus_Filled · More_Filled(채운 원 안 빼기 · 점 3개). 체크 원은 기존 Check_Filled와 같아 그대로 씀. Assets 28개', 'Figma, 코드'],
        ['2026-10-29', '대표 화면 · 웹 04 회고 완료 분석', '왼쪽 열 웹 03과 같게(Button 36 · Dropdown · Accordion/Section · 첫 카드 Selected), 위 탭 → Text Tab Item Size 18, 개인 · 팀 → Segmented Control, 분석 항목 아이콘 → Check_Filled(Gray 800) · Minus_Filled(Red 400) · More_Filled(Blue 600), 회색 80% 바탕 → Gray 100, 원격 아이콘 · 스타일 96곳 로컬로, 화면 밖 프레임 삭제. 요약 카드 · 회고 세 칸 틀은 다른 화면을 더 보고 정리', 'Figma'],
        ['2026-10-29', '<a href="writing-panel.html">Writing Panel</a>', '새 페이지 · 새 컴포넌트: Question Tag(읽기 전용 질문 태그), Button/Pager(이전 · 다음 32, Prev · Next × Default · Hover · Disabled), Question Index (Web) + Question Index Item(Unanswered · Current · Answered). CSS writing.css', 'Figma, 코드'],
        ['2026-10-29', '<a href="accordion.html">Accordion</a>', '새 컴포넌트 Accordion/Section (Web)(Collapsed · Expanded, 펼치면 웹 탭 + Card/Goal). CSS .section-accordion', 'Figma, 코드'],
        ['2026-10-29', '<a href="cards.html">Cards</a>', 'Card/Retro (Web)에 Selected(Off · On) 추가: 지금 열어 둔 회고, 테두리 Blue 400 + Shadow 100', 'Figma, 코드'],
        ['2026-10-29', '<a href="button.html">Button</a>', '규칙: 웹은 36이 기본, 작성 패널 아래처럼 한 영역을 마무리하는 행동(임시저장 · 작성 완료)은 40', '코드'],
        ['2026-10-29', '대표 화면 · 웹 03 회고 작성 중', '사전질문 태그 · 이전/다음 · 질문 전체보기를 새 컴포넌트로(관련 없는 Accordion/Index Title 프레임 제거), 실행목표 접기 → Accordion/Section (Web), 카드 테두리 덮어쓰기 → Selected=On(첫 카드만), 머리 버튼 · 드롭다운 → Button 36 · Dropdown, 원격 아이콘 · 버튼 9개 · 스타일 14곳을 로컬로, 숨은 · 화면 밖 레이어 7개 삭제', 'Figma'],
        ['2026-10-29', '<a href="logo.html">Logo</a>', '새 Figma 컴포넌트 Logo(Type=Horizontal · Symbol, 색은 Blue 900 · 600 · 200 토큰). LNB 상단의 직접 그린 로고 그룹을 이 인스턴스로 교체(4개 변형)', 'Figma, 코드'],
        ['2026-10-29', '<a href="avatar.html">Avatar</a>', 'Size 24 추가(웹 LNB 아래 프로필). LNB 펼침 변형의 직접 그린 프로필 원을 Avatar 24로 교체. CSS .avatar--24', 'Figma, 코드'],
        ['2026-10-29', '<a href="tabs.html">Tabs</a>', '새 묶음 컴포넌트 Tabs/Text Tabs (Web)(Item=2 · 3 · 4 Tabs, 탭 간격 4). 웹 02 실행목표 패널과 LNB 두 변형의 직접 묶은 탭을 이 컴포넌트로 교체. Figma Tabs 대지: 웹 줄 · Size 14 줄 추가, 아래 요소 겹침 해소', 'Figma'],
        ['2026-10-29', '<a href="tabs.html">Tabs</a>', 'Text Tab Item에 Size(18 · 14) 추가: 웹 패널 · LNB에서 글자만 14로 덮어쓰던 탭을 Size=14 변형으로. LNB 개인 · 팀은 Selected에 글자색만 회색으로 덮어써 있던 것을 Unselected 상태로 바로잡음. CSS .tabs--web', 'Figma, 코드'],
        ['2026-10-29', '대표 화면 색 대조', '정리한 화면 10개의 글자 · 면 색을 Page 2 원본과 대조. 모바일 06 날짜 선택을 원본대로(오전, 시간 미선택, 완료 버튼 활성), 모바일 04 제목을 원본 토큰 Purple 900으로 되돌림', 'Figma'],
        ['2026-10-29', '<a href="cards.html">Cards</a>', 'Card/Retro (Mobile) 인원 수 색 바로잡음: 모바일 02 정리 때 "1 / 10" 전체를 Purple 600으로 잘못 칠했던 것을 원본대로 제출 인원 Blue 600 + "/ 10" Gray 500으로. 숫자를 Count · Total 두 글자로 나눔. 웹 카드 마감 인원 수 원시 색 → Gray 700 토큰', 'Figma, 코드'],
        ['2026-10-29', '<a href="cards.html">Cards</a>', '새 컴포넌트 Card/Goal (Web)(웹 실행목표 패널의 회고별 목표 묶음, Badge On · Off, 목표 3줄). CSS .goal-card', 'Figma, 코드'],
        ['2026-10-29', '<a href="tabs.html">Tabs</a>', 'Text Tab Item: Unselected · Hover가 위 정렬, Selected는 아래 정렬이라 글자 크기가 다르면 높이가 어긋나던 것을 모두 아래 정렬로 맞춤', 'Figma'],
        ['2026-10-29', '대표 화면 · 웹 02 실행목표 패널', '직접 짠 목표 묶음 3개 → Card/Goal (Web), "실행 중" 라벨 → Badge Outlined Blue, 구분선 원시 색 → Gray 100 토큰, 탭 높이 어긋남 수정', 'Figma'],
        ['2026-10-29', '<a href="badge.html">Badge</a>', '변형 10개 너비 고정(55) → Hug(글자에 맞춤). 인스턴스 67곳도 Hug', 'Figma'],
        ['2026-10-29', '<a href="button.html">Button</a>', 'Figma 대지: Size 36 줄 이름표 추가, 아래 Ghost · Outlined · Floating · Group 섹션을 내려 겹침 해소', 'Figma'],
        ['2026-10-29', '<a href="cards.html">Cards</a>', '새 페이지. 카드 4종을 Card/ 이름으로 묶음: Card/Space · Card/Retro (Mobile) · Card/Answer(새로 만듦), Card/Retro (Web)(웹 Cards 정리: 한글 속성 → Status × Deadline, 상태 태그 → Badge Outlined, 제목 Title 15 Bold). 보드 "Components · Card". CSS cards.css', 'Figma, 코드'],
        ['2026-10-29', '<a href="dropdown.html">Dropdown</a>', '오른쪽 여백 12 → 16(Chevron 쪽이 좁아 보여서), 너비는 내용에 맞춤', 'Figma, 코드'],
        ['2026-10-29', '<a href="button.html">Button</a>', 'Filled에 Size=36 추가(웹: 좌우 12 · 간격 4 · 모서리 8 · 아이콘 18, 원본 웹 화면 값). 새 토큰 radius/button-xs(8). CSS .btn--xs', 'Figma, 코드'],
        ['2026-10-29', '<a href="dropdown.html">Dropdown</a>', '높이 40 → 36, 모서리 button-xs(8): 원본 웹과 같은 높이로 버튼 36과 나란히', 'Figma, 코드'],
        ['2026-10-29', '<a href="button.html">Button</a>', 'Size 40 아이콘이 Show Icon과 연결돼 있지 않던 것을 연결, 아이콘을 바꾸는 Icon 속성 추가', 'Figma'],
        ['2026-10-29', '<a href="dropdown.html">Dropdown</a>', '새 컴포넌트(웹 상단 필터 36, Default · Hover · Pressed). CSS .dropdown', 'Figma, 코드'],
        ['2026-10-29', '<a href="badge.html">Badge</a>', 'Style=Outlined 추가(Gray · Blue · Green · Dark, 22, Caption 11 SemiBold, 테두리 1px). 기존 변형은 Style=Filled', 'Figma, 코드'],
        ['2026-10-29', '<a href="typography.html">Typography</a> · <a href="color.html">Color</a>', 'Title 15 Bold(웹 섹션 · 카드 제목) · Caption 11 SemiBold(상태 태그) 추가, 20개. color/green/900 추가', 'Figma, 코드'],
        ['2026-10-29', '대표 화면 · 웹 02 회고 스페이스', '직접 짠 버튼 → Button 40 Blue(+Add), KPT · 팀원 → Dropdown, 원격 카드 → Card/Retro (Web), 원격 탭 · 스타일 · 색을 로컬 토큰으로(색 39 · 글자 24), 패널 radius card, 화면 밖 프레임 삭제. 웹 01 섹션 제목도 Title 15 Bold로', 'Figma'],
        ['2026-10-29', '대표 화면 · 모바일 01 · 02 · 03', '직접 짠 카드를 Card/Space · Card/Retro (Mobile) · Card/Answer 인스턴스로 바꿈', 'Figma'],
        ['2026-10-29', '<a href="tokens.html">Tokens</a>', 'tokens.json · DESIGN.md · components.json v0.1.9', '코드'],
        ['2026-10-29', '<a href="empty-state.html">Empty State</a>', 'Border 속성 추가: None(흰 카드가 틀, 웹 홈 위 두 칸) · Dashed(카드 안 빈 영역 구분, 분석 칸). 원본 화면에서 위 두 칸은 점선이 없었던 것을 반영', 'Figma, 코드'],
        ['2026-10-29', '<a href="tooltip.html">Tooltip</a>', 'Function Tooltip 변형 5개의 글자가 Label 속성에 연결되어 있지 않던 것을 연결', 'Figma'],
        ['2026-10-29', '<a href="empty-state.html">Empty State</a>', '새 컴포넌트. 점선 박스(Opacity 12) + 안내 1~2줄(Body 15 Medium Gray 500) + 선택 아이콘(Show Icon · Icon). CSS .empty-state', 'Figma, 코드'],
        ['2026-10-29', '웹 컴포넌트', 'Page 2 웹 섹션에 있던 LNB(206곳 사용)와 웹 Cards(1,263곳)를 라이브러리 보드 "Components · Web"으로 옮김(인스턴스 연결 유지). LNB 속성 Property=space · home · fold-space · Property4 → Fold(Off · On) × Current(Home · Space), 안의 원격 아이콘 · 탭 46곳을 로컬로', 'Figma'],
        ['2026-10-29', '<a href="typography.html">Typography</a> · <a href="radius.html">Radius</a>', 'Heading 28 Bold를 웹 페이지 제목으로 정식 추가(18개), radius/card-lg(16) 용도 토큰 추가', 'Figma, 코드'],
        ['2026-10-29', '대표 화면 · 웹 01 홈 대시보드', '섹션 제목 → Title 15 Bold(웹 02 때 스타일 추가), 점선 빈 칸 3곳 → Empty State, 흰 섹션 카드 → card-lg, 툴팁 · 감정 아이콘 · 원격 스타일을 로컬로, 숨은 원격 Cards 3개 · 화면 밖 버튼 삭제', 'Figma'],
        ['2026-10-29', '<a href="tokens.html">Tokens</a>', 'JSON · DESIGN.md · components.json v0.1.8', '코드'],
        ['2026-10-29', '대표 화면 · 모바일 08 계정 탈퇴 확인', '배경을 정리한 07 화면으로 바꾸고, 원격 Popup(옛 속성 Two Button - Vertical)을 로컬 Popup(Basic · Side by Side)으로, 원격 상태 바 · 딤 스타일을 로컬 · overlay/dim으로. 모바일 대표 화면 8개 정리 끝', 'Figma'],
        ['2026-10-29', '<a href="lists.html">Lists</a>', '새 컴포넌트 List/Menu Item(설정 목록 한 줄 48, Right = Chevron · Value · None). CSS .menu-card · .menu-row(2026-11-03에 .menu-item에서 이름 바꿈)', 'Figma, 코드'],
        ['2026-10-29', '<a href="avatar.html">Avatar</a>', 'Size 42 추가(설정 화면 프로필 행). 사진 · 아이콘 × 32 · 42', 'Figma, 코드'],
        ['2026-10-29', '대표 화면 · 모바일 07 내 정보', '직접 짠 설정 목록 9줄을 List/Menu Item으로, 직접 그린 프로필 원을 Avatar 42로, 선을 돌려 만든 화살표를 Chevron-Right로, 원격 상태 바 · 앱 바 · 그림자를 로컬로, 색 · 글자 · 간격을 토큰과 스타일로, 숨은 레이어 · 화면 밖 버튼 묶음 삭제', 'Figma'],
        ['2026-10-29', '<a href="tokens.html">Tokens</a>', 'DESIGN.md · components.json v0.1.7', '코드'],
        ['2026-10-29', '<a href="date-picker.html">Date Time Picker</a>', 'Figma 4가지 상태 모두 오늘 이전 날짜를 Disabled로(지난 날짜 선택 불가)', 'Figma'],
        ['2026-10-29', '대표 화면 · 모바일 06 마감일 설정', '직접 그린 바텀시트(요일이 하루 밀린 달력 · 24/12시간 섞인 시간 칩)를 Date Time Picker(오후 1:00 선택)로, 뒤 화면의 뒤로 아이콘 · 입력칸을 Top App Bar · Select Field로, 원격 상태 바 · Progress Bar를 로컬로, 제목 여백 20 · 제목 ↔ 입력칸 40, 딤을 overlay/dim으로', 'Figma'],
        ['2026-10-29', '<a href="tokens.html">Tokens</a>', 'DESIGN.md · components.json v0.1.6', '코드'],
        ['2026-10-29', '<a href="app-bar.html">App Bar</a>', '오른쪽 텍스트 버튼을 App Bar/Text Button(Default · Disabled) 컴포넌트로 분리해 Top App Bar Sub 안에 넣음. 인스턴스에서 Label · State를 바꿈. 코드 .app-bar__text-button:disabled', 'Figma, 코드'],
        ['2026-10-29', '<a href="fields.html">Fields</a>', '전체 화면 작성 영역 규칙: 테두리 없음, Body 15 Medium Long, 안내 문구 Gray 400(이미 쓴 글처럼 보이지 않게)', '코드'],
        ['2026-10-29', '대표 화면 · 모바일 05 메인 질문 작성', '직접 짠 상단 바를 Top App Bar(Close · 제목 숨김 · 텍스트 버튼 Disabled "마치기") + 가운데 Accordion Index Title로, 원격 상태 바 · 아이콘 · Button Group(Side by Side) · 이전 버튼을 로컬로, "1/4"와 제목 · 작성 영역을 토큰과 스타일로, 숨은 레이어 5개 삭제', 'Figma'],
        ['2026-10-29', '<a href="tokens.html">Tokens</a>', 'DESIGN.md · components.json v0.1.5', '코드'],
        ['2026-10-29', '<a href="spacing.html">Spacing</a>', '섹션 간격 32 · 40 추가(화면의 큰 덩어리 사이). Figma 변수 spacing/32 · spacing/40', 'Figma, 코드'],
        ['2026-10-29', '대표 화면 · 모바일 04 작성 패턴 선택', '원격 상태 바(iPhone X) · 앱 바 · Progress Bar(옛 이름 Progrees) · Two Choice 2개 · Button Group(옛 속성)을 로컬로, 제목 색 Purple 900 → text/primary, 두 카드를 간격 8 오토 레이아웃으로, 제목 ↔ 카드 40(spacing/40), 숨은 프레임 삭제. 모바일 02 상단 박스 ↔ 목록 30 → 32', 'Figma'],
        ['2026-10-29', '<a href="tokens.html">Tokens</a>', 'JSON · DESIGN.md · components.json v0.1.4', '코드'],
        ['2026-10-29', '<a href="badge.html">Badge</a>', 'Color=Gray(Gray 100 + Gray 800, 사람 이름)와 Size 속성 추가: 22(제목 옆) · 25(카드 머리 이름표, 위아래 4 · 좌우 8). 3색 × 2크기 = 6개', 'Figma, 코드'],
        ['2026-10-29', '<a href="typography.html">Typography</a>', 'Body 15 Medium Long 추가(행간 180%, 회고 답변처럼 긴 글). 텍스트 스타일 17개', 'Figma, 코드'],
        ['2026-10-29', '대표 화면 · 모바일 03 회고 답변 보기', '원격 인스턴스·스타일을 로컬로, 상단(상태 바 · 앱 바 · 탭)을 흰 Header 프레임으로 묶음, 제목 좌우 20 · 카드 간격 20, 이름표를 Badge Gray 25로, 답변 카드 5개 모두 Shadow 100, 질문 바 양 끝 정렬 · 모서리 12', 'Figma'],
        ['2026-10-29', '<a href="tokens.html">Tokens</a>', 'JSON · DESIGN.md · components.json v0.1.3', '코드'],
        ['2026-10-29', '<a href="badge.html">Badge</a>', 'Color=White 추가: 연파랑 회고 카드 위의 D-day(Gray 0 바탕 + Blue 600 글자)', 'Figma, 코드'],
        ['2026-10-29', '<a href="iconography.html">Iconography</a>', '그래픽 아이콘 24 크기 허용(카드 안 인원 수처럼 좁은 줄)', 'Figma, 코드'],
        ['2026-10-29', '<a href="button.html">Button</a>', '버튼 변형 40개(Filled 20 · Ghost 8 · Outlined 8 · Floating 4)의 글자가 Label 속성에 연결되어 있지 않던 것을 연결. 인스턴스에서 Label을 바꾸면 글자가 바뀜', 'Figma'],
        ['2026-10-29', '대표 화면 · 모바일 02 스페이스 상세', '원격 인스턴스·스타일을 로컬로(색 48곳 · 글자 23곳), 직접 그린 그래픽 아이콘 2개를 Document · Team으로, 상단 두 박스를 오토 레이아웃 + Shadow 100 + border/divider로 다시 짬, 카드 버튼을 Button 40 Blue로, D-15를 Badge White로, 숨은 레이어·홈 표시줄 정리', 'Figma'],
        ['2026-10-29', '<a href="tokens.html">Tokens</a>', 'DESIGN.md · components.json v0.1.2', '코드'],
        ['2026-10-28', '<a href="badge.html">Badge</a>', '새 컴포넌트. 대표 화면(모바일 01 회고 홈)의 "진행 중 1" 라벨을 정리: 높이 22 · 좌우 6 · Radius 4 · Blue 100 바탕 + Blue 600 글자. Figma Badge 세트 · CSS .badge', 'Figma, 코드'],
        ['2026-10-28', '<a href="typography.html">Typography</a>', 'Body 13 Medium 추가(카드 설명). 텍스트 스타일 16개', 'Figma, 코드'],
        ['2026-10-28', '<a href="iconography.html">Iconography</a>', '그래픽 아이콘 White를 연한 원(Gray 200, 40px) 안 썸네일에도 쓰도록 규칙 추가', '코드'],
        ['2026-10-28', '대표 화면 · 모바일 01 회고 홈', '원격 인스턴스(상태 바 · 앱 바 · 탭 · 아이콘)를 로컬 컴포넌트로, 직접 그린 하단 탭을 Navigation Bar로, 색 · 모서리 · 간격 · 글자를 토큰과 스타일로 연결, 남은 레이어 2개 삭제', 'Figma'],
        ['2026-10-28', '<a href="tokens.html">Tokens</a>', 'JSON · DESIGN.md · components.json v0.1.1', '코드'],
        ['2026-10-28', '<a href="tokens.html">Tokens</a>', 'AI 패키지 공개: DESIGN.md(Google 형식, 공식 린터 오류 0) · components.json(컴포넌트 41 · 아이콘 45 · 일러스트 20), 두 방식 비교 예시', '코드, Figma'],
        ['2026-10-28', '<a href="tokens.html">Tokens</a>', '새 페이지. 토큰 규칙(이름 · 고르는 순서 · 추가 · 변경 · 버전)과 JSON v0.1.0 다운로드, 버전 히스토리', '코드'],
        ['2026-10-28', '전체 컴포넌트', 'Figma 컴포넌트 85개(세트·아이콘)에 설명 채움: 언제 쓰는지, 속성 뜻, 연결된 토큰, 코드 클래스. 정리 전인 Component 18·Tags/Tag에는 “새 화면에 쓰기 전 확인” 표시', 'Figma'],
        ['2026-10-28', '<a href="typography.html">Typography</a> · <a href="elevation.html">Elevation</a>', '라이브러리 독립: 원본 라이브러리의 텍스트 스타일 16개, 그림자 스타일 4개, 격자 스타일 1개를 이 파일 로컬 스타일로 만들고 연결 911곳을 옮김(값 동일, Caption/10 Bold만 확정대로 10px)', 'Figma'],
        ['2026-10-28', '<a href="button.html">Button</a> · <a href="avatar.html">Avatar</a>', '버튼 40 글자 40곳을 Subtitle 14 SemiBold 스타일에 연결, Profile 배경 #D0D3DB를 Gray 400 변수로(코드와 일치), 자식이 하나뿐인 프레임의 의미 없는 간격 10을 0으로(101곳)', 'Figma'],
        ['2026-10-27', '컴포넌트 CSS 11개', '색·간격·모서리 숫자를 토큰으로 교체(var(--color-text-primary, #212329) 형식, 숫자는 대비값으로 유지). Hover·Pressed는 팔레트 단계, 바텀시트·팝업 그림자는 --shadow-modal', '코드'],
        ['2026-10-27', '<a href="color.html">Color</a>', '역할 토큰 19개 추가(text·bg·border·overlay·status), 컴포넌트 기본 상태 색 414곳을 역할 토큰으로 연결, 팔레트 변수는 고르기 목록에서 숨김', 'Figma, 코드'],
        ['2026-10-27', '<a href="spacing.html">Spacing</a>', '새 페이지. 여섯 단계 + screen-x, Figma Spacing 변수 추가·996곳 연결, spacing.css 추가', 'Figma, 코드'],
        ['2026-10-27', '<a href="radius.html">Radius</a>', 'Figma에 용도 이름 12개 추가(radius/button 등)하고 컴포넌트를 용도 이름으로 연결', 'Figma'],
        ['2026-10-27', '<a href="color.html">Color</a>', 'Figma Color 변수 55개 추가(color/gray/900 ↔ --color-gray-900), 컴포넌트·문서 대지의 색 연결을 스타일에서 변수로 이동', 'Figma'],
        ['2026-10-27', '<a href="illustration.html">Illustration</a>', 'Figma 일러스트 대지를 Brand 템플릿(흰 배경, 제목·설명, 그룹 제목, 이름 라벨)으로 다시 구성', 'Figma'],
        ['2026-10-27', '<a href="radius.html">Radius</a>', 'Figma Radius 변수 7개 추가, 컴포넌트 모서리 1,160곳 연결 · 삭제 아이콘 바탕 3.6 → 4', 'Figma, 코드'],
        ['2026-10-27', '<a href="radius.html">Radius</a>', '새 페이지. 컴포넌트에서 쓰인 둥글기를 일곱 단계(4·6·8·10·12·16·Full)와 용도 토큰으로 정리, radius.css 추가', '코드'],
        ['2026-10-27', '<a href="state.html">State</a>', '새 페이지. Hover 한 단계 · Pressed 두 단계 규칙과 Selected · Disabled · Focus · 입력창 상태 정리', '코드'],
        ['2026-10-27', '<a href="bottom-sheet.html">Bottom Sheet</a>', '새 페이지. 속성을 Content·Button으로 정리, Show Title·Show Close로 통일, 세로 자동 배치(Short는 내용에 맞춤, Long은 670 고정)', 'Figma, 코드'],
        ['2026-10-27', '<a href="bottom-sheet.html">Bottom Sheet</a>', '중복 Home Indicator 삭제, 일러스트를 교체 가능한 Retro/KPT 인스턴스로, 칩·입력 너비 335, Filter 목록 정렬, 로컬 Text Input으로 교체, 탭 글자 높이 통일', 'Figma, 코드'],
        ['2026-10-27', '<a href="bottom-sheet.html">Bottom Sheet</a>', 'Anatomy·Usage를 실제 컴포넌트 인스턴스로 다시 구성, 번호 30×30, 레이어 이름 정리, 가려진 설명 위치 수정', 'Figma'],
        ['2026-10-27', '<a href="popup.html">Popup</a>', 'With Illustration 기본 그림을 Content/Recommend로 변경', 'Figma, 코드'],
        ['2026-10-27', '<a href="illustration.html">Illustration</a>', '배너 2개를 Banner/1:1 · Banner/2:1 그룹으로 분리', 'Figma, 코드'],
        ['2026-10-27', '<a href="illustration.html">Illustration</a>', '드래그 리사이즈 시 어그러짐 수정: Scale 제약, 글자·선·모서리 윤곽선 변환, 그룹을 프레임으로', 'Figma'],
        ['2026-10-27', '<a href="illustration.html">Illustration</a>', '쓰임별 이름(Content·Retro·Splash), 500 기준 통일, 투명 배경, 컴포넌트화, 내보내기 SVG·PNG 2x·3x', 'Figma, 코드'],
        ['2026-10-27', '<a href="illustration.html">Illustration</a>', '팔레트 밖 색 7곳 교체, Color 스타일 121곳 연결, 숨은·남는 레이어 삭제, 간격 정렬, SSC 글자 36', 'Figma, 코드'],
        ['2026-10-27', '<a href="popup.html">Popup</a>', 'With Illustration 그림 자리를 바꿀 수 있는 Illustration 인스턴스로 교체', 'Figma, 코드'],
        ['2026-10-27', '<a href="button.html">Button</a>', '버튼 그룹 속성을 Button = Single·Side by Side·Stacked로 변경(Popup과 같은 기준)', 'Figma, 코드'],
        ['2026-10-27', '<a href="typography.html">Typography</a>', 'Page 1의 Title 18 Bold 글자 22곳(같은 너비 탭, 파운데이션 제목, 타이포 견본 등)을 행간 140% 로컬 스타일로 연결', 'Figma, 코드'],
        ['2026-10-27', '<a href="popup.html">Popup</a>', 'Button 값 Single·Side by Side·Stacked로 변경, Stacked 두 번째 버튼 Ghost, 속성 Type 정리·Illustration 속성 중복 제거', 'Figma, 코드'],
        ['2026-10-27', '<a href="popup.html">Popup</a>', 'Title·Sub Title 텍스트/표시 속성 추가, 제목을 Title 18 Bold 140% 스타일로 연결, 분리된 버튼 인스턴스화', 'Figma, 코드'],
        ['2026-10-27', '<a href="popup.html">Popup</a>', 'Anatomy 제목·5번 설명·강조 사각형·번호 색 정리, 숨은 레이어 삭제', 'Figma'],
        ['2026-10-27', '<a href="date-picker.html">Date Time Picker</a>', '실제 달력대로 요일 배치, 오늘 = Blue 600, Day 컴포넌트(Default·Hover·Pressed·Selected·Today·Disabled) 추가', 'Figma, 코드'],
        ['2026-10-27', '<a href="date-picker.html">Date Time Picker</a>', '시간 12시간제(12:00, 1:00~11:00), 시간 줄 가로 스크롤 + 흐림, 날짜·시간을 모두 골라야 버튼 활성', 'Figma, 코드'],
        ['2026-10-27', '<a href="date-picker.html">Date Time Picker</a>', '속성 State로 정리, 텍스트 스타일 연결(크기 유지), Anatomy를 실제 인스턴스로, 숨은 레이어·1px 틈 정리', 'Figma'],
        ['2026-10-27', '<a href="chip-button.html">Chip Button</a>', 'Multi Choice에 Size 38(모서리 6px, Subtitle 14 SemiBold) 추가', 'Figma, 코드'],
        ['2026-10-27', '<a href="tabs.html">Tabs</a>', 'Text 탭에 밑줄 없는 버전(Underline = Off) 추가', 'Figma, 코드'],
        ['2026-10-27', '<a href="toast.html">Toast</a>', 'Caution 아이콘 Red 400, 속성 Type = Text·Info·Caution, Text의 숨은 아이콘 삭제', 'Figma, 코드'],
        ['2026-10-27', '<a href="toast.html">Toast</a>', '사라지는 시간 3초로 명시, 사용 예시를 실제 Toast·Button 컴포넌트로 교체, 빈 레이어 삭제', 'Figma, 코드'],
        ['2026-10-27', '<a href="tooltip.html">Tooltip</a>', 'Function Tooltip은 가리킨 영역을 누르거나 화면을 이동할 때까지 표시(3초 자동 사라짐 삭제), 화살표 가로 위치 16px로 통일', 'Figma, 코드'],
        ['2026-10-27', '<a href="tooltip.html">Tooltip</a>', 'Function Tooltip에 Color(Blue·Gray 900) 추가, 가운데 화살표 툴팁을 세트로 합침', 'Figma, 코드'],
        ['2026-10-27', '<a href="tooltip.html">Tooltip</a>', '화살표 없는 툴팁을 Hover Tooltip 항목으로 정리(대상 위 8px, 왼쪽 끝 맞춤), Guide는 유지', 'Figma, 코드'],
        ['2026-10-27', '<a href="lists.html">Lists</a>', '체크박스 리스트를 하나로 합치고 Controls 체크박스 인스턴스 사용, 이름 Checkbox List / Icon List', 'Figma, 코드'],
        ['2026-10-27', '<a href="lists.html">Lists</a>', '아이콘 리스트 배경 Gray 100, 순서 변경 = Drawer 아이콘, 삭제 = 빨간 네모 + Close 아이콘', 'Figma, 코드'],
        ['2026-10-27', '<a href="accordion.html">Accordion</a>', 'Index Item 컴포넌트 분리(Default·Hover·Pressed·Selected), Press → Pressed', 'Figma, 코드'],
        ['2026-10-27', '<a href="accordion.html">Accordion</a>', '숫자 동그라미 모서리 30으로 통일, Position 예시를 실제 컴포넌트로 다시 구성, 제목 오타 수정', 'Figma'],
        ['2026-10-27', '<a href="controls.html">Controls</a>', '라디오 추가(체크박스와 같은 속성·크기·색, 원 + 흰 점)', 'Figma, 코드'],
        ['2026-10-27', '<a href="controls.html">Controls</a>', 'Label Right 추가(With Label → Label Left), 호버·눌림 추가, 라벨 너비 글자에 맞춤', 'Figma, 코드'],
        ['2026-10-27', '<a href="controls.html">Controls</a>', '라벨형 선택 안 된 박스를 Default와 같게(Gray 400 테두리, 흰 배경), 쓰지 않는 Disabled 속성과 잘못된 설명 삭제', 'Figma'],
        ['2026-10-27', '<a href="scroll-bar.html">Scroll Bar</a>', 'Controls 보드에서 분리해 별도 보드로', 'Figma'],
        ['2026-10-27', '전체', 'Page 1의 지운 변수 연결을 원본 Color 스타일로 교체(스타일 없는 색은 값으로)', 'Figma'],
        ['2026-10-27', '<a href="tabs.html">Tabs</a>', 'Fixed 탭 선택 시 글자가 2px 올라가던 것을 같은 높이로 수정, 이름 Sheet → Fixed', 'Figma, 코드'],
        ['2026-10-27', '<a href="tabs.html">Tabs</a>', '호버 상태 추가(Text 탭 Gray 600 글자, Box 탭 Gray 200 배경)', 'Figma, 코드'],
        ['2026-10-27', '<a href="tabs.html">Tabs</a>', 'Box 탭 선택 Gray 800, 선택 안 된 글자 Gray 500을 원본 Color 스타일에 연결', 'Figma'],
        ['2026-10-27', '<a href="tabs.html">Tabs</a>', 'Scrollable을 375px로 줄이고 가장자리 흐림 + 옆으로 스크롤 추가, 숨은 레이어 정리', 'Figma, 코드'],
        ['2026-10-27', '전체', 'AI가 임시로 만든 변수 삭제. 색은 원본 Color 스타일로 연결', '방식'],
        ['2026-10-27', '<a href="fields.html">Fields</a>', 'Text Area의 Error·OverTyping을 Text Input 기준으로 통일(Error = 특수문자, OverTyping = 글자 수 초과)', 'Figma, 코드'],
        ['2026-10-27', '<a href="fields.html">Fields</a>', 'Text Input OverTyping 예시를 "최대 10자", 10/10으로 수정', 'Figma, 코드'],
        ['2026-10-27', '<a href="fields.html">Fields</a>', '입력한 글자색 Gray 900으로 통일(Text Area Blue 900, Select Field Gray 800 수정)', 'Figma, 코드'],
        ['2026-10-27', '<a href="fields.html">Fields</a>', 'Text Area 커서를 "|" 글자에서 막대로 변경, 포커스 상태에 흰 배경 추가', 'Figma, 코드'],
        ['2026-10-27', '<a href="fields.html">Fields</a>', '오류 테두리 Blue 600, 비활성·안내 문구 색은 현 상태 유지', '기록'],
        ['2026-10-27', '<a href="chip-button.html">Chip Button</a>', '비활성 상태 추가(버튼 비활성과 같은 Gray 100 배경, Gray 400 글자)', 'Figma, 코드'],
        ['2026-10-27', '<a href="chip-button.html">Chip Button</a>', '글자색 Gray 800 유지, 모서리 8px(버튼 12px과 다름)은 의도한 차이로 확정', '기록'],
        ['2026-10-27', '<a href="chip-button.html">Chip Button</a>', 'Two Choice 너비를 화면에 맞춰 늘어나도록 변경, 이름 오타 "Chioce" 수정', 'Figma, 코드'],
        ['2026-10-27', '<a href="progress-bar.html">Progress Bar</a>', 'Current Step 속성 추가, 사용 예시를 속성으로 다시 연결, 이름 오타 "Progrees" 수정', 'Figma, 코드'],
        ['2026-10-27', '<a href="progress-bar.html">Progress Bar</a>', '남은 단계 색 Opacity 4 유지', '기록'],
        ['2026-10-27', '<a href="button.html">Button</a>', 'Ghost·Outlined·Floating 속성 이름 오타 "Show lcon" → "Show Icon" 수정', 'Figma'],
        ['2026-10-27', '<a href="button.html">Button</a>', '상태 규칙 통일: 호버는 한 단계, 눌림은 두 단계 진하게(Primary·Blue·Floating 수정)', 'Figma, 코드'],
        ['2026-10-27', '<a href="button.html">Button</a>', 'Ghost·Outlined·Floating 비활성을 Filled 비활성(Gray 100 배경, Gray 400 글자)으로 통일', 'Figma, 코드'],
        ['2026-10-27', '<a href="button.html">Button</a>', 'Secondary·White·Outlined 글자색을 Gray 900으로 통일', 'Figma, 코드'],
        ['2026-10-27', '<a href="button.html">Button</a>', '높이 40px 크기 추가(Size 속성 48/40), 설명 문구 작성', 'Figma, 코드'],
        ['2026-10-27', '<a href="button.html">Button</a>', '파란 글자 버튼의 명도 대비 기준(4.5:1) 미달은 현 상태로 유지', '기록'],
        ['2026-10-27', '<a href="logo.html">Logo</a>', '겹친 칸 색을 Blue 200으로 통일(Three Colors 수정), 파비콘 모서리 비율은 쓰임별로 유지', 'Figma, 코드'],
        ['2026-10-27', '<a href="logo.html">Logo</a>', '로고·파비콘·응용 버전을 Figma 원본 벡터로 추가, 문서 사이트 로고를 실제 로고로 교체', '코드'],
        ['2026-10-26', '<a href="app-bar.html">App Bar</a>', 'Inverse의 더보기 아이콘을 흰색으로 통일', '코드'],
        ['2026-10-26', '<a href="iconography.html">Iconography</a>', 'Calendar_Filled → Camera_Filled 이름 변경', 'Figma, 코드'],
        ['2026-10-26', '<a href="iconography.html">Iconography</a>', 'Emotion의 Better·Good 색 순서는 의도한 것으로 확정', '기록'],
        ['2026-10-26', '<a href="elevation.html">Elevation</a>', '그림자 4단계와 용도 이름(Card, Floating Button, Layer, Modal) 정의', '코드'],
        ['2026-10-26', '<a href="typography.html">Typography</a>', 'Title 18 Bold 행간 140%, Caption 10 Bold 10px로 확정', '코드'],
        ['2026-10-26', '<a href="color.html">Color</a>', 'Orange 300 라벨 오타("Orange / 00") 수정', 'Figma, 코드'],
        ['2026-10-26', '전체', 'AI가 미리 만든 변수는 쓰지 않고, 실제 화면 분석으로 토큰을 만들기로 결정', '방식'],
    ]
    openq = [
        ['<a href="elevation.html">Elevation</a>', 'Shadow 200만 아래 그림자 구조가 달라 300과 구분이 어려움'],
        ['<a href="iconography.html">Iconography</a>', 'Figma 아이콘 3개만 순수 검정(#000) 사용'],
        ['<a href="navigation-bar.html">Navigation Bar</a>', '화면 기준 너비 375px와 393px 혼재'],
        ['<a href="button.html">Button</a>', '40px 버튼 글자가 Subtitle 14 스타일에 연결되지 않고 값(14px)으로만 들어감'],
        ['Figma 문서', 'Elevation, App Bar 페이지 설명 문구가 "Icons에 대한 설명 작성"으로 남아 있음'],
    ]
    content = page_head('시작하기', '업데이트', '디자인시스템에서 바뀐 것과 결정한 것을 날짜순으로 남깁니다. 아직 정하지 않은 것은 열린 질문에 모읍니다.')
    content += ('<section class="section"><h2>v0.2.0 · 2026-11-03</h2><p>대표 화면 16개(모바일 8 · 웹 8) 정리, Page 2 빈틈 채우기, 레이아웃 · 템플릿, AI 생성 테스트 2회를 거쳐 0.1.x를 한 번 정리한 버전입니다. 파일은 <a href="tokens.html">Tokens</a>에서 받습니다.</p>'
        + table(['구분', '내용'], [
            ['규모', '컴포넌트 82개(0.1.8의 47개에서 늘어남), 토큰 151개, 텍스트 스타일 22개, 아이콘 48 · 일러스트 20, 사이트 37쪽'],
            ['새로 생김', '<a href="layout.html">Layout</a>(토큰 9 · 그리드 스타일 3 · Template/Web Type=List · Work · Template/Mobile Background) · <a href="popover.html">Popover · Menu · Member Item</a> · <a href="analysis.html">Analysis 7종</a> · <a href="cards.html">Card/Template · Detail · Summary · Question Group · Goal (Mobile) · Answer Emotion · Score</a> · Section Header · Info Banner · Modal (Web) · Dropdown · Segmented Control · 작성 패널 부품'],
            ['속성 추가', 'Button Show Label(아이콘만) · Text Button Type=Neutral · Outlined Icon · Profile Show Leader · List/Icon List None · Star / Number · Modal (Web) Show Back · Show Title · Show Footer · Card/Retro (Mobile) Status=Closed · Card/Retro (Web) 텍스트 속성 · Card/Goal Show Items · Show Empty'],
            ['AI 파일', 'components.json에 nested(탭 이름 · 배지 · 칩 문구 · 앱 바 · 내비게이션 · LNB를 안쪽에서 바꾸는 법), DESIGN.md에 레이아웃 · 템플릿 · 딤드 · 바탕 · Section Header · OS Bar 예외 규칙'],
            ['<strong>호환되지 않는 변경</strong>', 'App Bar/Text Button → <code>Button/Text Button</code>(Type=Accent · Neutral) · Card/Answer → Platform × Type 세트 · Card/Retro (Mobile) → Status 세트 · Template/Mobile → Background 세트 · Profile Size 24 → 28(<code>.avatar--24</code> → <code>.avatar--28</code>) · <code>text.error</code> · <code>status.error</code> Red 400 → Red 500 · <code>overlay.dim-popover</code> 삭제 · Component 18 · Tags/Tag 컴포넌트 해제(디자인으로만 남음)'],
            ['검증', 'Figma 컴포넌트 152개 · 대표 화면 16개 정합성 점검(외부 인스턴스 · 변수 없는 색 · 스타일 없는 글자 0), AI 생성 테스트 2회(없는 이름 · 토큰 0건)']]) + '</section>')
    content += f'''<section class="section"><h2>결정 기록</h2>{table(['날짜', '영역', '내용', '반영'], log, num_cols=(0,))}</section>
<section class="section"><h2>열린 질문</h2>{table(['영역', '내용'], openq)}</section>'''
    return content

# ── page-specific styles ─────────────────────────────────
PAGES_CSS = r'''/* Page-level layouts for the documentation site */
.principles { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 20px; }
.principles > div { display: flex; flex-direction: column; gap: 6px; padding-top: 14px; border-top: 2px solid var(--fg); }
.principles h3 { margin: 0; font-size: 15px; }
.principles p { font-size: 14px; color: var(--fg-muted); }
.steps { margin: 0; padding-left: 22px; display: grid; gap: 10px; }
.steps li { padding-left: 4px; }
.steps strong { margin-right: 6px; }

/* Color */
.swatches { display: grid; grid-template-columns: repeat(var(--n), minmax(0, 1fr)); gap: 0; border-radius: 10px; overflow: hidden; border: 1px solid var(--line); }
.sw { display: flex; flex-direction: column; gap: 0; padding: 0; border: 0; background: var(--bg-sunk); color: var(--fg); font: inherit; text-align: left; cursor: pointer; min-width: 0; }
.sw-chip { position: relative; display: block; height: 64px; box-shadow: inset 0 -1px 0 var(--line); }
.sw-chip--checker { background-color: #fff; background-image: conic-gradient(#e6e8ec 25%, transparent 0 50%, #e6e8ec 0 75%, transparent 0); background-size: 12px 12px; }
.sw-chip--checker > span { position: absolute; inset: 0; }
.sw-tag { position: absolute; left: 8px; bottom: 6px; font-size: 11px; font-weight: 600; }
.sw-name { padding: 8px 8px 0; font-size: 13px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.sw-hex { padding: 0 8px 10px; font-size: 11.5px; color: var(--fg-faint); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.sw:hover .sw-name { color: var(--accent); }
.sw:focus-visible { outline: 2px solid var(--accent); outline-offset: -2px; }
@media (max-width: 700px) {
  .swatches[style*="--n:10"] { grid-template-columns: repeat(5, minmax(0, 1fr)); }
  .principles { grid-template-columns: 1fr; }
}

/* Tokens as copy buttons */
.token { font: 500 12.5px var(--font-mono); color: var(--fg); background: var(--code-bg); border: 0; border-radius: 4px; padding: 3px 7px; cursor: pointer; white-space: nowrap; }
.token:hover { color: var(--accent); }
.small { font-size: 12px; color: var(--fg-muted); }
.count { font-weight: 500; font-size: 14px; color: var(--fg-faint); margin-left: 6px; }

/* Typography */
.type-sample { white-space: nowrap; color: var(--fg); }
.type-hero { display: flex; flex-direction: column; gap: 6px; }
.type-hero__big { font-family: var(--font-family-primary); font-weight: 700; font-size: clamp(40px, 8vw, 64px); line-height: 1.1; letter-spacing: -1px; }
.type-hero__meta { font-size: 13px; color: #666b75; }

/* Elevation */
.lvl-stage { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 28px; padding: 48px 36px; }
.lvl { display: flex; flex-direction: column; gap: 20px; min-width: 0; }
.lvl-card { aspect-ratio: 19 / 18; max-width: 100%; background: #fff; border-radius: 12px; }
.lvl-name { color: #06080c; }
.lvl-use { color: rgba(6, 8, 12, 0.48); }
@media (max-width: 700px) { .lvl-stage { grid-template-columns: repeat(2, minmax(0, 1fr)); padding: 28px 20px; } }

/* Iconography */
.size-row { display: flex; flex-wrap: wrap; gap: 32px; align-items: flex-end; }
.size-demo { display: flex; flex-direction: column; align-items: center; gap: 10px; color: #212329; }
.size-demo code { background: #f2f4f8; color: #454952; }
.ic-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(96px, 1fr)); gap: 4px; }
.ic { display: flex; flex-direction: column; align-items: center; gap: 8px; padding: 14px 6px 10px; border: 0; border-radius: 8px; background: none; color: #212329; font: inherit; cursor: pointer; min-width: 0; }
.ic span:last-child { font-size: 11.5px; color: #666b75; text-align: center; overflow-wrap: anywhere; line-height: 1.3; }
.ic:hover { background: #f2f4f8; }
.ic--static { cursor: default; }
.ic--static:hover { background: none; }
.gp-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(124px, 1fr)); gap: 20px 12px; }
.gp { display: flex; flex-direction: column; gap: 8px; min-width: 0; }
.gp > span { font-size: 12px; color: #666b75; }
.gp-pair { display: grid; grid-template-columns: 1fr 1fr; height: 64px; border-radius: 8px; overflow: hidden; border: 1px solid #edf0f4; }
.gp-light, .gp-dark { display: flex; align-items: center; justify-content: center; }
.gp-dark { background: #212329; }
.emo-row { display: flex; flex-wrap: wrap; gap: 28px; }
.emo { display: grid; justify-items: center; gap: 6px; }
.emo small { font-size: 12px; color: #666b75; }

/* Logo */
.lg-hero { display: grid; grid-template-columns: 200px minmax(0, 1fr); gap: 40px; align-items: center; padding: 40px; }
.lg-hero__mark svg { display: block; width: 100%; height: auto; max-width: 200px; }
.lg-anatomy { margin: 0; display: grid; gap: 16px; color: #212329; }
.lg-anatomy dt { font-weight: 700; font-size: 15px; display: flex; align-items: center; gap: 10px; }
.lg-anatomy dd { margin: 4px 0 0 28px; font-size: 14px; color: #666b75; }
.sq { width: 18px; height: 18px; border-radius: 4px; box-shadow: inset 0 0 0 1px rgb(0 0 0 / 0.08); }
.lg-grid { display: grid; gap: 16px; }
.lg-grid--3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
.lg-grid--2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.lg { margin: 0; display: flex; flex-direction: column; border: 1px solid var(--line); border-radius: 12px; overflow: hidden; min-width: 0; }
.lg-stage { display: flex; align-items: center; justify-content: center; padding: 36px 24px; background: #fff; }
.lg-stage svg { display: block; width: 120px; height: auto; max-width: 100%; }
.lg--wide .lg-stage { padding: 44px 32px; }
.lg--wide .lg-stage svg { width: 320px; }
.lg figcaption { display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 12px 14px; border-top: 1px solid var(--line); font-size: 13px; }
.lg figcaption span { display: flex; flex-direction: column; color: var(--fg-muted); line-height: 1.4; }
.lg figcaption strong { color: var(--fg); font-size: 14px; }
.copy--inline { position: static; flex: none; }   /* same look as the code-block 복사 button, placed in flow */
@media (max-width: 700px) {
  .lg-hero { grid-template-columns: 1fr; padding: 28px 20px; gap: 24px; }
  .lg-hero__mark svg { max-width: 140px; }
  .lg-grid--3, .lg-grid--2 { grid-template-columns: 1fr; }
}

/* Components */
.phone-w { width: 375px; max-width: 100%; }
.stack { display: flex; flex-direction: column; gap: 8px; }
.stack--loose { gap: 20px; }
.dark-canvas { background: #212329; border-color: #212329; }
.nav-bar.is-static .nav-item { pointer-events: none; }
.states { display: flex; flex-wrap: wrap; gap: 24px 40px; }
.state { display: flex; flex-direction: column; gap: 10px; }
.state-label { font-size: 13px; font-weight: 600; color: #8b909c; }
.state-item { display: flex; width: 90px; }
.state-item .nav-item { pointer-events: none; }
.dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 8px; vertical-align: -1px; box-shadow: inset 0 0 0 1px rgb(0 0 0 / 0.08); }
.os-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 24px 32px; }
.os { margin: 0; display: flex; flex-direction: column; gap: 8px; min-width: 0; }
.os-img { border: 1px dashed #ced2da; border-radius: 6px; overflow: hidden; }
.os-img svg { display: block; width: 100%; height: auto; }
.os-img--android { aspect-ratio: 360 / 40; }
.os figcaption { font-size: 12px; color: #666b75; }
@media (max-width: 700px) { .os-grid { grid-template-columns: 1fr; } }
.av-row { display: flex; flex-wrap: wrap; gap: 40px; }
.av { display: flex; align-items: center; gap: 14px; }
.av > span:last-child { display: flex; flex-direction: column; font-size: 14px; font-weight: 600; color: #212329; line-height: 1.4; }
.av small { font-size: 12px; font-weight: 500; color: #8b909c; }
.bt-live { display: flex; flex-wrap: wrap; gap: 12px; align-items: center; }
.bt-grid { display: grid; grid-template-columns: 110px repeat(4, minmax(150px, 1fr)); gap: 16px 20px; align-items: center; min-width: 760px; }
.bt-grid .btn { width: 100%; max-width: 208px; pointer-events: none; }
.bt-grid .btn--floating { width: auto; }
.bt-h { font-size: 13px; font-weight: 600; color: #8b909c; }
.bt-name { font-size: 14px; font-weight: 600; color: #666b75; }
.bt-groups { display: flex; flex-wrap: wrap; gap: 24px; justify-content: center; }
.bt-g { margin: 0; width: 375px; max-width: 100%; display: flex; flex-direction: column; gap: 10px; }
.bt-g figcaption { font-size: 13px; font-weight: 600; color: #8b909c; }
.bt-g .btn-group { background: #fff; border-radius: 12px; overflow: hidden; }
.cb-static { pointer-events: none; }
.cb-states { align-items: flex-end; }
.cb-states--card .chip-button--card { width: 163px; }
.cb-two { max-width: 335px; }
.pb-demo { width: 375px; max-width: 100%; display: flex; flex-direction: column; align-items: center; gap: 4px; }
.pb-demo #pb-live { width: 100%; box-sizing: border-box; padding: 8px 20px 20px; }
#pb-live { align-self: stretch; }
.pb-ctrl { display: flex; gap: 8px; }
.pb-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 24px; min-width: 760px; }
.pb-list { display: flex; flex-direction: column; gap: 4px; }
.pb-row { display: flex; flex-direction: column; }
.pb-row .progress-bar { padding: 8px 0 12px; }
.fl-static { pointer-events: none; }
.fl-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 28px 24px; align-items: start; }
.fl-cell { gap: 12px; }
.fl-demo { display: flex; flex-direction: column; gap: 24px; max-width: 335px; }
.tb-static { pointer-events: none; }
.tb-demo { display: flex; flex-direction: column; gap: 20px; max-width: 375px; margin: 0 -28px; }
@media (max-width: 860px) { .tb-demo { margin: 0 -16px; } }
.tb-grid { display: grid; grid-template-columns: 150px repeat(3, minmax(90px, 1fr)); gap: 16px 20px; align-items: center; min-width: 520px; }
.tb-name { font-size: 14px; font-weight: 600; color: #666b75; }
.tb-cell { display: flex; }
.tb-one { display: flex; width: 90px; height: 44px; }
.ct-static { pointer-events: none; }
.ct-demo { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 24px; }
.ct-list { list-style: none; margin: 8px 0 0; padding: 0; display: flex; flex-direction: column; gap: 4px; }
.ct-list--end li { display: flex; justify-content: space-between; }
.ct-list--end .control { width: 100%; justify-content: space-between; }
.ct-grid { display: grid; grid-template-columns: 170px repeat(3, minmax(100px, 1fr)); gap: 14px 20px; align-items: center; min-width: 620px; }
.ct-name { font-size: 13px; font-weight: 600; color: #8b909c; }
.ct-dis { display: flex; gap: 16px; }
.sb-demo { height: 280px; padding: 4px 16px; font-size: 14px; color: #454952; }
.sb-demo p { margin: 0; padding: 10px 0; border-bottom: 1px solid #f2f4f8; }
.sb-spec { width: 10px; height: 160px; box-sizing: border-box; padding: 5px 3px; display: flex; flex-direction: column; }
.sb-spec span { width: 4px; height: 33.33%; border-radius: 99px; }
.ls-wrap .list { max-width: 375px; margin: 0 auto; }
.ls-wrap .list li { border-bottom: 1px solid #f2f4f8; }
.ls-cols { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 24px; }
.ls-cols .list { margin-top: 8px; }
.ls-cols .list-card { list-style: none; }
.ac-wrap { display: flex; justify-content: center; }
.ac-index-demo { width: 335px; max-width: 100%; display: flex; flex-direction: column; align-items: center; gap: 12px; min-height: 360px; }
.ac-stack { width: 335px; max-width: 100%; display: flex; flex-direction: column; gap: 12px; }
.ac-static { pointer-events: none; }
.dp-wrap { display: flex; justify-content: center; }
.pp-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(315px, 1fr)); gap: 28px 24px; align-items: start; }
.pp-static { pointer-events: none; }
.tk-latest { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 16px; }
.tk-ver { margin: 0; font-size: 22px; font-weight: 700; color: #212329; } .tk-ver span { font-size: 15px; font-weight: 500; color: #8b909c; }
.tk-sub { margin: 4px 0 0; font-size: 14px; color: #666b75; }
.tk-dl { display: inline-flex; align-items: center; gap: 12px; white-space: nowrap; }
.tk-open { display: none; }
.tk-msg:empty { display: none; }
.cmp { display: grid; grid-template-columns: repeat(2, minmax(0, 375px)); justify-content: center; gap: 40px; padding: 32px 28px; }
.cmp-col { min-width: 0; }
.cmp-title { display: flex; align-items: center; gap: 8px; margin: 0; font-size: 16px; font-weight: 600; line-height: 1.4; color: #212329; }
.cmp-tag { display: inline-flex; align-items: center; justify-content: center; width: 24px; height: 24px; border-radius: 6px; background: #212329; color: #fff; font-size: 13px; font-weight: 700; }
.cmp-tag--b { background: #6c9cfa; }
.cmp .cmp-sub { margin: 4px 0 20px; font-size: 13px; color: #8b909c; }
.cmp-screen { position: relative; width: 100%; aspect-ratio: 375 / 812; border-radius: 16px; overflow: hidden; background: #fff; box-shadow: 0 4px 12px rgb(6 8 12 / .04), inset 0 0 0 1px #e4e8ee; }
.cmp-screen img { display: block; width: 100%; height: 100%; }
.cmp-mark { position: absolute; display: inline-flex; align-items: center; justify-content: center; width: 24px; height: 24px; margin: -12px 0 0 -12px; border-radius: 50%; background: #212329; color: #fff; font-size: 13px; font-weight: 700; box-shadow: 0 0 0 2px #fff; }
.bd-row { display: flex; gap: 12px; flex-wrap: wrap; }
.bd-swatch > .dropdown { align-self: flex-start; width: auto; }
.cd-goal { width: 306px; max-width: 100%; box-sizing: border-box; padding: 18px; border-radius: 12px; background: #fff; }
.sa-demo { width: 296px; }
.cd-stack { display: grid; gap: 12px; width: 335px; max-width: 100%; margin: 0 auto; }
.cd-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 296px)); gap: 12px; justify-content: center; }
.es-demo { display: grid; gap: 16px; max-width: 640px; margin: 0 auto; }
.bd-colors { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; }
.bd-swatch { display: flex; flex-direction: column; gap: 8px; }
.bd-on { display: flex; align-items: center; justify-content: center; height: 72px; border-radius: 12px; }
.bd-on--white { background: var(--color-gray-0, #fff); box-shadow: inset 0 0 0 1px var(--color-gray-300, #dfe3ea); }
.bd-on--blue { background: var(--color-blue-50, #f1f6ff); }
.bd-card { display: flex; gap: 16px; width: 335px; max-width: 100%; box-sizing: border-box; padding: 16px; border-radius: 12px; background: var(--color-bg-surface, #fff); text-align: left; }
.bd-card__thumb { width: 40px; height: 40px; flex: none; border-radius: 50%; background: var(--color-gray-200, #edf0f4); }
.bd-card__body { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 6px; }
.bd-card__row { display: flex; align-items: center; gap: 8px; }
.bd-card__title { flex: 1; min-width: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; color: var(--color-text-primary, #212329); }
.bd-card__desc { color: var(--color-gray-600, #8b909c); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.cmp-legend td:first-child { white-space: nowrap; font-weight: 600; }
.badge-n { display: inline-flex; align-items: center; justify-content: center; width: 20px; height: 20px; margin-right: 8px; border-radius: 50%; background: #212329; color: #fff; font-size: 11px; font-weight: 700; vertical-align: 1px; }
@media (max-width: 640px) { .cmp { gap: 16px; padding: 20px 12px; } .cmp-sub { font-size: 12px; } .cmp-mark { width: 20px; height: 20px; margin: -10px 0 0 -10px; font-size: 11px; } }
.tk-steps { margin: 0; padding-left: 20px; display: grid; gap: 8px; }
td small { color: var(--fg-faint); }
.spc-stage { display: flex; flex-direction: column; gap: 14px; }
.spc-row { display: grid; grid-template-columns: 112px 120px 1fr; align-items: center; gap: 16px; color: #212329; }
.spc-bar { display: block; height: 24px; background: #c4d7fd; border-radius: 4px; }
.spc-val { font-size: 14px; color: #666b75; }
.role-sw { display: inline-block; width: 14px; height: 14px; border-radius: 4px; margin-right: 8px; vertical-align: -2px; box-shadow: inset 0 0 0 1px rgb(6 8 12 / .12); }
@media (max-width: 560px) { .spc-row { grid-template-columns: 100px 1fr; } .spc-val { grid-column: 1 / -1; } }
.rd-stage { display: grid; grid-template-columns: repeat(auto-fill, minmax(112px, 1fr)); gap: 28px 16px; }
.rd-item { display: flex; flex-direction: column; align-items: flex-start; gap: 2px; }
.rd-box { width: 88px; height: 88px; margin-bottom: 12px; background: #e9f0ff; box-shadow: inset 0 0 0 2px #6c9cfa; }
.rd-name { margin: 0; color: #212329; }
.rd-val { margin: 0; color: #666b75; }
.st-table { display: grid; gap: 10px; padding: 24px; }
.st-row { display: grid; grid-template-columns: minmax(150px, 1.4fr) repeat(3, minmax(72px, 1fr)); gap: 10px; align-items: center; }
.st-row--head span { font-size: 12px; font-weight: 600; color: #8b909c; }
.st-name { display: flex; flex-direction: column; gap: 2px; font-size: 14px; color: #212329; line-height: 1.4; }
.st-name small { font-size: 12px; color: #666b75; }
.st-sw { display: flex; align-items: center; justify-content: center; height: 44px; border-radius: 8px; font-size: 12px; font-weight: 600; color: #212329; text-align: center; }
.st-focus { display: flex; flex-wrap: wrap; align-items: center; gap: 32px; }
.st-fv { outline: 2px solid #6c9cfa; outline-offset: 2px; pointer-events: none; }
.st-fv-in { display: inline-flex; align-items: center; justify-content: center; box-sizing: border-box; height: 40px; padding: 0 16px; border-radius: 8px; outline: 2px solid #6c9cfa; outline-offset: -2px; font-size: 14px; font-weight: 600; line-height: 1.4; color: #212329; }
@media (max-width: 560px) { .st-row { grid-template-columns: repeat(3, 1fr); } .st-row .st-name { grid-column: 1 / -1; } .st-row--head span:first-child { display: none; } }
.bs-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 375px)); gap: 28px 24px; align-items: start; justify-content: center; }
.bs-static { pointer-events: none; }
.bs-static .bsheet { margin: 0 auto; }
.bs-slot { height: 163px; }
.bs-ph { display: flex; align-items: center; justify-content: center; height: 100%; min-height: 120px; background: #f2f4f8; color: #a9afbb; font: 500 15px/1.4 var(--font-family-primary); }
.bs-list { list-style: none; margin: 0; padding: 0; }
.bsheet-dim .bsheet { max-width: 430px; animation: bs-up .2s ease-out; }
@keyframes bs-up { from { transform: translateY(24px); opacity: 0; } to { transform: none; opacity: 1; } }
@media (prefers-reduced-motion: reduce) { .bsheet-dim .bsheet { animation: none; } }
.pp-demo { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; }
/* Illustration */
.il-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(168px, 1fr)); gap: 20px 16px; }
.il-card { display: flex; flex-direction: column; gap: 10px; margin: 0; min-width: 0; }
.il-card--wide { grid-column: span 2; }
.il-card__img { display: flex; align-items: center; justify-content: center; aspect-ratio: 1 / 1; padding: 12px; border-radius: 12px; background: #ffffff; box-shadow: inset 0 0 0 1px var(--line); }
.il-card--wide { container-type: inline-size; }
.il-card--wide .il-card__img { aspect-ratio: auto; height: calc((100cqw - 16px) / 2); }
.il-card__img img { display: block; width: 100%; height: 100%; object-fit: contain; }
.il-card figcaption { display: flex; flex-direction: column; gap: 2px; font-size: 13px; }
.il-card__name { font-weight: 600; }
.il-card__use { color: var(--fg-muted); }
.il-card__dl { align-self: flex-start; margin-top: 6px; }
.il-canvas { background: #ffffff; }
.il-canvas .il-size { color: #666b75; }
.il-sizes { display: flex; flex-wrap: wrap; align-items: flex-end; gap: 24px; }
.il-size { display: flex; flex-direction: column; align-items: center; gap: 8px; margin: 0; font-size: 12px; color: var(--fg-muted); }
@media (max-width: 560px) { .il-card--wide { grid-column: 1 / -1; } .il-card--wide .il-card__img { aspect-ratio: 2 / 1; } .il-sizes .illust--280 { width: 100%; max-width: 280px; } }
.dp-static { pointer-events: none; }
.fb-demo { display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 24px; }
.fb-phone { position: relative; width: 375px; max-width: 100%; height: 240px; border-radius: 16px; background: #fff; box-shadow: inset 0 0 0 1px rgb(6 8 12 / .08); overflow: hidden; }
.fb-host { position: absolute; left: 20px; right: 20px; bottom: 24px; }
.fb-host .toast { opacity: 0; transform: translateY(8px); transition: opacity .2s, transform .2s; }
.fb-host .toast.is-shown { opacity: 1; transform: none; }
.fb-btns { display: flex; flex-direction: column; gap: 8px; }
.fb-grid { display: grid; grid-template-columns: repeat(2, max-content); gap: 20px 48px; }
.fb-grid .state { align-items: flex-start; }
@media (max-width: 720px) { .fb-grid { grid-template-columns: max-content; } }
.fb-grid .tooltip { margin: 12px 0; align-self: flex-start; }
.fb-hover { display: flex; align-items: flex-end; gap: 16px; min-height: 120px; }
.fb-target { width: 32px; height: 32px; display: inline-flex; align-items: center; justify-content: center; border: 0; border-radius: 6px; background: #f2f4f8; color: #212329; cursor: pointer; }
.fb-target .icon, .fb-target svg { width: 20px; height: 20px; display: block; }
.fb-hint { font-size: 13px; color: var(--fg-faint); padding-top: 7px; }
.ac-index-demo .acc-index { width: 100%; }
.acc-title[hidden], .acc-index[hidden] { display: none; }
'''

def sentence_breaks(html):
    """Put a line break between sentences only where it helps: long paragraphs, never tiny fragments."""
    vis = lambda x: len(re.sub(r'<[^>]+>', '', x))
    def fix(m):
        open_tag, inner = m.group(1), m.group(2)
        if 'cbody' in open_tag: return m.group(0)             # callouts stay compact
        lead = 'lead' in open_tag
        total_min, chunk_min = (50, 20) if lead else (90, 40)
        if vis(inner) < total_min: return m.group(0)
        # split into sentences outside <code>
        parts, buf = [], ''
        for seg in re.split(r'(<code>.*?</code>)', inner):
            if seg.startswith('<code>'): buf += seg; continue
            pieces = re.split(r'(?<=[.!?])\s+(?=\S)', seg)
            for i, pc in enumerate(pieces):
                buf += pc
                if i < len(pieces) - 1: parts.append(buf); buf = ''
        parts.append(buf)
        if lead:                                              # lead: break once, after the defining first sentence
            return open_tag + (parts[0] + '<br>' + ' '.join(parts[1:]) if len(parts) > 1 and vis(parts[0]) >= chunk_min else ' '.join(parts)) + '</p>'
        out, chunk = '', ''
        for i, sent in enumerate(parts):
            if not chunk: chunk = sent
            elif vis(chunk) >= chunk_min: out += chunk + '<br>'; chunk = sent
            else: chunk += ' ' + sent
        out += chunk
        return open_tag + out + '</p>'
    return re.sub(r'(<p(?: [^>]*)?>)(.*?)</p>', fix, html, flags=re.S)

def main():
    build_color_css()
    (R / 'css/pages.css').write_text(PAGES_CSS)
    titles = {'index': 'Layer Design System', 'updates': '업데이트 · Layer DS', 'figma-file': 'Figma 파일 쓰기 · Layer DS', 'ai-guide': 'AI로 화면 만들기 · Layer DS', 'logo': 'Logo · Layer DS', 'illustration': 'Illustration · Layer DS', 'color': 'Color · Layer DS', 'typography': 'Typography · Layer DS',
              'elevation': 'Elevation · Layer DS', 'tokens': 'Tokens · Layer DS', 'spacing': 'Spacing · Layer DS', 'layout': 'Layout · Layer DS', 'radius': 'Radius · Layer DS', 'state': 'State · Layer DS', 'iconography': 'Iconography · Layer DS', 'app-bar': 'App Bar · Layer DS',
              'navigation-bar': 'Navigation Bar · Layer DS', 'avatar': 'Avatar · Layer DS', 'badge': 'Badge · Layer DS', 'empty-state': 'Empty State · Layer DS', 'cards': 'Cards · Layer DS', 'dropdown': 'Dropdown · Layer DS', 'popover': 'Popover · Menu · Layer DS', 'analysis': 'Analysis · Layer DS', 'writing-panel': 'Writing Panel · Layer DS', 'button': 'Button · Layer DS', 'chip-button': 'Chip Button · Layer DS', 'progress-bar': 'Progress Bar · Layer DS', 'fields': 'Fields · Layer DS', 'tabs': 'Tabs · Layer DS', 'controls': 'Controls · Layer DS', 'scroll-bar': 'Scroll Bar · Layer DS', 'lists': 'Lists · Layer DS', 'accordion': 'Accordion · Layer DS', 'date-picker': 'Date Time Picker · Layer DS', 'popup': 'Popup · Layer DS', 'bottom-sheet': 'Bottom Sheet · Layer DS', 'toast': 'Toast · Layer DS', 'tooltip': 'Tooltip · Layer DS'}
    builders = {'index': p_index, 'updates': p_updates, 'figma-file': p_figma_file, 'ai-guide': p_ai_guide, 'logo': p_logo, 'illustration': p_illustration, 'color': p_color, 'typography': p_typography, 'elevation': p_elevation, 'tokens': p_tokens, 'layout': p_layout, 'spacing': p_spacing, 'radius': p_radius, 'state': p_state,
                'iconography': p_iconography, 'app-bar': p_app_bar, 'navigation-bar': p_nav, 'avatar': p_avatar, 'badge': p_badge, 'empty-state': p_empty, 'cards': p_cards, 'dropdown': p_dropdown, 'popover': p_popover, 'analysis': p_analysis, 'writing-panel': p_writing, 'button': p_button, 'chip-button': p_chip, 'progress-bar': p_progress, 'fields': p_fields, 'tabs': p_tabs, 'controls': p_controls, 'scroll-bar': p_scrollbar, 'lists': p_lists, 'accordion': p_accordion, 'date-picker': p_datepicker, 'popup': p_popup, 'bottom-sheet': p_bsheet, 'toast': p_toast, 'tooltip': p_tooltip}
    for pid, fn in builders.items():
        (R / f'{pid}.html').write_text(shell(pid, titles[pid], sentence_breaks(fn()), wrapped=(pid == 'index')))
        if pid == 'index':  # full document for GitHub Pages (the artifact publishes the wrapped one)
            pathlib.Path('build').mkdir(exist_ok=True); (pathlib.Path('build') / 'index-pages.html').write_text(shell(pid, titles[pid], sentence_breaks(fn()), wrapped=False))
    print('built', len(builders), 'pages')

main()
