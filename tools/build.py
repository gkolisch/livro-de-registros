import os
import re
import hashlib
import shutil
import unicodedata

import markdown as md

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'site')

PASSWORD = 'judas'
PASSWORD_HASH = hashlib.sha256(PASSWORD.encode()).hexdigest()
AUTH_KEY = 'lr_auth'

EXCLUDE_FILES = {'Bem-vindo.md'}
SKIP_DIRS = {'.obsidian', 'site', 'tools', '.git', 'node_modules'}

FOLDER_LABELS = {
    '': 'Início',
    '01 - Episodios': 'Episódios',
    '02 - Personagens': 'Personagens',
    '03 - Instituicoes': 'Instituições',
    '04 - Conceitos (Lore)': 'Conceitos',
    '05 - Itens e Reliquias': 'Itens e Relíquias',
}
FOLDER_ORDER = ['01 - Episodios', '02 - Personagens', '03 - Instituicoes',
                '04 - Conceitos (Lore)', '05 - Itens e Reliquias']

DISPLAY_TITLE = {
    '00 - Home': 'Início',
    'SEM NOME': '-SEM NOME-',
    'Z (Jose Ferreira da Silva)': 'Z',
}


def slugify(title):
    if title == '00 - Home':
        return 'home'
    s = unicodedata.normalize('NFKD', title)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    s = s.strip('-')
    return s or 'pagina'


def collect_notes():
    notes = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        rel = os.path.relpath(dirpath, ROOT).replace('\\', '/')
        rel = '' if rel == '.' else rel
        for f in filenames:
            if not f.endswith('.md') or f in EXCLUDE_FILES:
                continue
            stem = f[:-3]
            notes.append({
                'title': stem,
                'display': DISPLAY_TITLE.get(stem, stem),
                'slug': slugify(stem),
                'rel': rel,
                'path': os.path.join(dirpath, f),
            })
    notes.sort(key=lambda n: n['title'].lower())
    return notes


CSS = """
:root {
  --bg: #0d0d11;
  --bg-2: #14141a;
  --panel: #17171f;
  --line: #26262f;
  --text: #ded9cd;
  --muted: #8b8577;
  --accent: #c9a35c;
  --accent-2: #8f2b34;
  --serif: Georgia, 'Times New Roman', serif;
  --mono: 'Courier New', monospace;
}
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body {
  background: var(--bg);
  color: var(--text);
  font-family: var(--serif);
  font-size: 17px;
  line-height: 1.65;
  display: flex;
  min-height: 100vh;
}
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }

.sidebar {
  width: 280px;
  flex-shrink: 0;
  background: var(--bg-2);
  border-right: 1px solid var(--line);
  padding: 24px 0 40px;
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
}
.brand {
  padding: 0 22px 18px;
  border-bottom: 1px solid var(--line);
  margin-bottom: 14px;
}
.brand a { color: var(--text); font-weight: bold; letter-spacing: .5px; }
.brand .sub { color: var(--muted); font-size: 12px; font-family: var(--mono); letter-spacing: 2px; text-transform: uppercase; margin-top: 3px; }
.nav-group { padding: 8px 22px 2px; color: var(--muted); font-size: 11px; font-family: var(--mono); letter-spacing: 2px; text-transform: uppercase; }
.nav-link {
  display: block;
  padding: 4px 22px;
  color: var(--text);
  font-size: 15px;
  border-left: 3px solid transparent;
}
.nav-link:hover { background: var(--panel); text-decoration: none; color: var(--accent); }
.nav-link.active { border-left-color: var(--accent); color: var(--accent); background: var(--panel); }

.main { flex: 1; min-width: 0; }
.topbar {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding: 14px 28px;
  border-bottom: 1px solid var(--line);
  position: sticky;
  top: 0;
  background: rgba(13,13,17,.92);
  backdrop-filter: blur(4px);
}
.topbar .crumb { margin-right: auto; color: var(--muted); font-family: var(--mono); font-size: 13px; }
.topbar a.logout { color: var(--muted); font-family: var(--mono); font-size: 13px; }
.topbar a.logout:hover { color: var(--accent-2); }

.content { max-width: 780px; padding: 40px 44px 90px; }
h1, h2, h3, h4 { font-family: var(--serif); font-weight: normal; line-height: 1.25; }
h1 { font-size: 40px; margin: 0 0 6px; letter-spacing: .3px; }
h2 { font-size: 24px; margin: 40px 0 12px; border-bottom: 1px solid var(--line); padding-bottom: 6px; color: var(--accent); }
h3 { font-size: 19px; margin: 28px 0 8px; }
h4 { font-size: 16px; margin: 20px 0 6px; color: var(--muted); }
p { margin: 14px 0; }
hr { border: none; border-top: 1px solid var(--line); margin: 34px 0; }
blockquote {
  margin: 18px 0;
  padding: 2px 0 2px 18px;
  border-left: 3px solid var(--accent);
  color: var(--text);
  font-style: italic;
}
blockquote p { margin: 6px 0; }
ul, ol { padding-left: 26px; }
li { margin: 5px 0; }
code {
  font-family: var(--mono);
  background: var(--panel);
  padding: 1px 6px;
  border-radius: 4px;
  font-size: 14px;
}
table { border-collapse: collapse; width: 100%; margin: 18px 0; font-size: 15px; }
th, td { border: 1px solid var(--line); padding: 8px 12px; text-align: left; vertical-align: top; }
th { background: var(--panel); color: var(--accent); font-weight: normal; }
a.wikilink { color: var(--accent); border-bottom: 1px dotted var(--accent); }
a.wikilink:hover { text-decoration: none; border-bottom-style: solid; }
.meta { color: var(--muted); font-size: 14px; font-family: var(--mono); }

.gate { margin: 0; display: flex; align-items: center; justify-content: center; background: radial-gradient(circle at 50% 20%, #1a1a23 0%, #0d0d11 60%); }
.gate-card {
  width: 100%;
  max-width: 380px;
  background: var(--panel);
  border: 1px solid var(--line);
  padding: 44px 40px;
  text-align: center;
}
.gate-card h1 { font-size: 30px; margin-bottom: 4px; }
.gate-card .sub { color: var(--muted); font-size: 12px; font-family: var(--mono); letter-spacing: 3px; text-transform: uppercase; margin-bottom: 28px; }
.gate-card input {
  width: 100%;
  background: var(--bg-2);
  border: 1px solid var(--line);
  color: var(--text);
  font-family: var(--mono);
  font-size: 16px;
  padding: 12px 14px;
  text-align: center;
  letter-spacing: 2px;
  outline: none;
}
.gate-card input:focus { border-color: var(--accent); }
.gate-card button {
  width: 100%;
  margin-top: 14px;
  background: var(--accent);
  color: #12120f;
  border: none;
  font-family: var(--mono);
  font-size: 14px;
  letter-spacing: 2px;
  text-transform: uppercase;
  padding: 12px;
  cursor: pointer;
}
.gate-card button:hover { background: #d8b573; }
.gate-card .err { color: var(--accent-2); font-size: 13px; margin-top: 12px; min-height: 18px; }
.foot { color: var(--muted); font-size: 13px; margin-top: 48px; border-top: 1px solid var(--line); padding-top: 18px; }

@media (max-width: 760px) {
  body { flex-direction: column; }
  .sidebar { width: 100%; height: auto; position: static; border-right: none; border-bottom: 1px solid var(--line); }
  .content { padding: 28px 22px 70px; }
  h1 { font-size: 30px; }
}
"""


def build_nav(notes, active_slug):
    home = [n for n in notes if n['slug'] == 'home']
    rest = [n for n in notes if n['slug'] != 'home']
    parts = []
    for n in home:
        cls = 'nav-link active' if n['slug'] == active_slug else 'nav-link'
        parts.append(f'<a class="{cls}" href="{n["slug"]}.html">{n["display"]}</a>')
    for folder in FOLDER_ORDER:
        group = [n for n in rest if n['rel'] == folder]
        if not group:
            continue
        parts.append(f'<div class="nav-group">{FOLDER_LABELS.get(folder, folder)}</div>')
        for n in group:
            cls = 'nav-link active' if n['slug'] == active_slug else 'nav-link'
            parts.append(f'<a class="{cls}" href="{n["slug"]}.html">{n["display"]}</a>')
    return '\n'.join(parts)


def build_page(title, nav_html, content_html, crumb):
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · O Livro de Registros</title>
<style>{CSS}</style>
</head>
<body>
<aside class="sidebar">
  <div class="brand">
    <a href="home.html">O Livro de Registros</a>
    <div class="sub">Registro confidencial</div>
  </div>
  {nav_html}
</aside>
<main class="main">
  <div class="topbar">
    <span class="crumb">{crumb}</span>
    <a class="logout" href="#" onclick="logout()">Sair</a>
  </div>
  <div class="content">
{content_html}
    <div class="foot">Este é um relato contado sobre um mundo paralelo. Considere-o uma obra de ficção.</div>
  </div>
</main>
<script>
var AUTH_KEY = '{AUTH_KEY}';
var AUTH_HASH = '{PASSWORD_HASH}';
if (localStorage.getItem(AUTH_KEY) !== AUTH_HASH) {{ location.replace('index.html'); }}
function logout() {{ localStorage.removeItem(AUTH_KEY); location.href = 'index.html'; }}
</script>
</body>
</html>
"""


GATE_JS = """
function sha256(ascii) {
  function r(v, a) { return (v >>> a) | (v << (32 - a)); }
  var maxW = Math.pow(2, 32);
  var result = '';
  var words = [];
  var bitLen = ascii.length * 8;
  var hash = sha256.h = sha256.h || [];
  var k = sha256.k = sha256.k || [];
  var primeCounter = k.length;
  var isComposite = {};
  for (var c = 2; primeCounter < 64; c++) {
    if (!isComposite[c]) {
      for (var i = 0; i < 313; i += c) { isComposite[i] = c; }
      hash[primeCounter] = (Math.pow(c, .5) * maxW) | 0;
      k[primeCounter++] = (Math.pow(c, 1 / 3) * maxW) | 0;
    }
  }
  ascii += '\\x80';
  while (ascii.length % 64 - 56) ascii += '\\x00';
  for (var i = 0; i < ascii.length; i++) {
    var j = ascii.charCodeAt(i);
    if (j >> 8) return '';
    words[i >> 2] |= j << ((3 - i) % 4) * 8;
  }
  words[words.length] = (bitLen / maxW) | 0;
  words[words.length] = bitLen;
  for (var j = 0; j < words.length;) {
    var w = words.slice(j, j += 16);
    var old = hash;
    hash = hash.slice(0, 8);
    for (var i = 0; i < 64; i++) {
      var w15 = w[i - 15], w2 = w[i - 2];
      var a = hash[0], e = hash[4];
      var temp1 = hash[7]
        + (r(e, 6) ^ r(e, 11) ^ r(e, 25))
        + ((e & hash[5]) ^ ((~e) & hash[6]))
        + k[i]
        + (w[i] = (i < 16) ? w[i] : (w[i - 16] + (r(w15, 7) ^ r(w15, 18) ^ (w15 >>> 3)) + w[i - 7] + (r(w2, 17) ^ r(w2, 19) ^ (w2 >>> 10))) | 0);
      var temp2 = (r(a, 2) ^ r(a, 13) ^ r(a, 22)) + ((a & hash[1]) ^ (a & hash[2]) ^ (hash[1] & hash[2]));
      hash = [(temp1 + temp2) | 0].concat(hash);
      hash[4] = (hash[4] + temp1) | 0;
    }
    for (var i = 0; i < 8; i++) { hash[i] = (hash[i] + old[i]) | 0; }
  }
  for (var i = 0; i < 8; i++) {
    for (var j = 3; j + 1; j--) {
      var b = (hash[i] >> (j * 8)) & 255;
      result += ((b < 16) ? '0' : '') + b.toString(16);
    }
  }
  return result;
}
var AUTH_KEY = '__AUTH_KEY__';
var AUTH_HASH = '__AUTH_HASH__';
function tryEnter() {
  var v = document.getElementById('pw').value.trim();
  var err = document.getElementById('err');
  if (sha256(v) === AUTH_HASH) {
    localStorage.setItem(AUTH_KEY, AUTH_HASH);
    location.href = 'home.html';
  } else {
    err.textContent = 'Senha incorreta.';
  }
}
document.getElementById('pw').addEventListener('keydown', function (e) {
  if (e.key === 'Enter') { tryEnter(); }
});
document.getElementById('pw').focus();
"""


def build_gate():
    gate_js = GATE_JS.replace('__AUTH_KEY__', AUTH_KEY).replace('__AUTH_HASH__', PASSWORD_HASH)
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Acesso · O Livro de Registros</title>
<style>{CSS}</style>
</head>
<body class="gate">
<div class="gate-card">
  <h1>O Livro de Registros</h1>
  <div class="sub">Acesso restrito</div>
  <input type="password" id="pw" placeholder="Senha" autocomplete="off">
  <button onclick="tryEnter()">Entrar</button>
  <div class="err" id="err"></div>
</div>
<script>
{gate_js}
</script>
</body>
</html>
"""


def main():
    notes = collect_notes()
    slug_map = {n['title']: n['slug'] for n in notes}

    def resolve(m):
        inner = m.group(1)
        target, sep, alias = inner.partition('|')
        target = target.strip()
        alias = (alias.strip() if sep else target)
        slug = slug_map.get(target)
        if slug is None:
            return alias
        return f'<a class="wikilink" href="{slug}.html">{alias}</a>'

    wiki_re = re.compile(r'\[\[([^\]]+)\]\]')

    if os.path.isdir(SITE):
        shutil.rmtree(SITE)
    os.makedirs(SITE)

    for n in notes:
        with open(n['path'], encoding='utf-8') as f:
            text = f.read()
        text = wiki_re.sub(resolve, text)
        body = md.markdown(text, extensions=['tables', 'fenced_code', 'sane_lists'])
        nav = build_nav(notes, n['slug'])
        crumb = FOLDER_LABELS.get(n['rel'], n['rel'])
        page = build_page(n['display'], nav, body, crumb)
        with open(os.path.join(SITE, n['slug'] + '.html'), 'w', encoding='utf-8') as f:
            f.write(page)

    with open(os.path.join(SITE, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(build_gate())

    with open(os.path.join(SITE, '404.html'), 'w', encoding='utf-8') as f:
        f.write('<html><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=index.html"></head><body></body></html>')

    print(f'Site gerado em {SITE}: {len(notes)} paginas + index + 404')


if __name__ == '__main__':
    main()
