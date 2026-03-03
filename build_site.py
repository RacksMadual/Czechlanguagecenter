#!/usr/bin/env python3
"""
Converts all Czech study markdown files into a single navigable HTML website.
Run: python3 build_site.py
Then open: index.html in your browser.
"""

import os
import re
import markdown

MODULES = [
    ("README.md",                     "Overview & Guide"),
    ("01_grammar_reference.md",       "01 · Grammar Reference (A2)"),
    ("02_vocabulary_by_topic.md",     "02 · Vocabulary by Topic"),
    ("03_citizenship_knowledge.md",   "03 · Citizenship Exam — All 30 Topics"),
    ("04_exam_practice.md",           "04 · A2 Exam Practice"),
    ("05_useful_phrases.md",          "05 · Useful Phrases"),
    ("06_B1_grammar_bridge.md",       "06 · B1 Grammar Bridge (A2→B1)"),
    ("07_B1_vocabulary_expansion.md", "07 · B1 Vocabulary Expansion"),
    ("08_B1_exam_practice.md",        "08 · B1 Exam Practice"),
    ("09_study_roadmap.md",           "09 · Study Roadmap"),
]

CSS = """
:root {
  --bg: #0f1117;
  --surface: #1a1d2e;
  --surface2: #252840;
  --accent: #4f8ef7;
  --accent2: #7c3aed;
  --green: #22c55e;
  --red: #ef4444;
  --yellow: #f59e0b;
  --text: #e2e8f0;
  --muted: #94a3b8;
  --border: #2d3154;
  --sidebar-w: 280px;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Segoe UI', system-ui, sans-serif; background: var(--bg);
       color: var(--text); display: flex; min-height: 100vh; font-size: 15px; }

/* SIDEBAR */
#sidebar {
  width: var(--sidebar-w); min-height: 100vh; background: var(--surface);
  border-right: 1px solid var(--border); position: fixed; top: 0; left: 0;
  overflow-y: auto; z-index: 100; display: flex; flex-direction: column;
}
#sidebar-header {
  padding: 24px 20px 16px; border-bottom: 1px solid var(--border);
}
#sidebar-header h1 { font-size: 14px; color: var(--accent); font-weight: 700;
  letter-spacing: .05em; text-transform: uppercase; }
#sidebar-header p { font-size: 12px; color: var(--muted); margin-top: 4px; }
#sidebar nav { padding: 12px 0; flex: 1; }
.nav-section { padding: 8px 20px 4px; font-size: 11px; color: var(--muted);
  text-transform: uppercase; letter-spacing: .08em; }
.nav-item { display: block; padding: 9px 20px; color: var(--text); text-decoration: none;
  font-size: 13px; border-left: 3px solid transparent; transition: all .15s; cursor: pointer;
  border: none; background: none; width: 100%; text-align: left; }
.nav-item:hover { background: var(--surface2); color: var(--accent); }
.nav-item.active { background: var(--surface2); color: var(--accent);
  border-left-color: var(--accent); }
.badge { display: inline-block; padding: 1px 7px; border-radius: 10px;
  font-size: 10px; font-weight: 600; margin-left: 6px; }
.badge-a2 { background: #1d4ed8; color: #bfdbfe; }
.badge-b1 { background: #6d28d9; color: #ddd6fe; }
.badge-both { background: #065f46; color: #a7f3d0; }

/* MAIN */
#main { margin-left: var(--sidebar-w); flex: 1; }
.page { display: none; padding: 48px 56px; max-width: 900px; }
.page.active { display: block; }
.page-header { margin-bottom: 32px; padding-bottom: 20px;
  border-bottom: 1px solid var(--border); }
.page-header h1 { font-size: 26px; font-weight: 700; color: var(--accent); }
.page-header p { color: var(--muted); margin-top: 6px; font-size: 13px; }

/* MARKDOWN CONTENT */
.content h1 { font-size: 22px; color: var(--accent); margin: 32px 0 12px;
  padding-bottom: 8px; border-bottom: 1px solid var(--border); }
.content h2 { font-size: 18px; color: #a78bfa; margin: 28px 0 10px; }
.content h3 { font-size: 15px; color: var(--yellow); margin: 22px 0 8px; }
.content h4 { font-size: 13px; color: var(--green); margin: 16px 0 6px;
  text-transform: uppercase; letter-spacing: .05em; }
.content p { line-height: 1.7; margin: 10px 0; color: var(--text); }
.content ul, .content ol { margin: 10px 0 10px 24px; }
.content li { line-height: 1.7; margin: 4px 0; }
.content strong { color: #fbbf24; font-weight: 600; }
.content em { color: var(--muted); font-style: italic; }
.content code { background: var(--surface2); padding: 2px 6px; border-radius: 4px;
  font-family: 'Fira Code', monospace; font-size: 13px; color: #86efac; }
.content pre { background: var(--surface2); border: 1px solid var(--border);
  border-radius: 8px; padding: 16px; overflow-x: auto; margin: 16px 0; }
.content pre code { background: none; padding: 0; }
.content blockquote { border-left: 3px solid var(--accent2); padding: 10px 16px;
  background: var(--surface2); border-radius: 0 8px 8px 0; margin: 16px 0;
  color: var(--muted); }
.content hr { border: none; border-top: 1px solid var(--border); margin: 28px 0; }
.content a { color: var(--accent); text-decoration: none; }
.content a:hover { text-decoration: underline; }

/* TABLES */
.content table { width: 100%; border-collapse: collapse; margin: 16px 0;
  font-size: 13.5px; }
.content th { background: var(--surface2); padding: 10px 12px; text-align: left;
  color: var(--accent); font-weight: 600; border-bottom: 2px solid var(--border); }
.content td { padding: 9px 12px; border-bottom: 1px solid var(--border); }
.content tr:hover td { background: rgba(79,142,247,.06); }
.content td:first-child { font-weight: 500; }

/* CHECKBOXES */
.content input[type=checkbox] { accent-color: var(--accent); width: 15px;
  height: 15px; margin-right: 6px; cursor: pointer; }

/* SEARCH */
#search-bar { width: 100%; padding: 8px 12px; background: var(--surface2);
  border: 1px solid var(--border); border-radius: 6px; color: var(--text);
  font-size: 13px; margin: 0 20px; width: calc(100% - 40px); margin: 12px 20px; }
#search-bar::placeholder { color: var(--muted); }
#search-bar:focus { outline: none; border-color: var(--accent); }

/* PROGRESS BAR */
#progress-bar { position: fixed; top: 0; left: var(--sidebar-w); right: 0;
  height: 3px; background: var(--border); z-index: 200; }
#progress-fill { height: 100%; background: linear-gradient(90deg, var(--accent), var(--accent2));
  width: 0; transition: width .1s; }

/* MOBILE */
#menu-toggle { display: none; position: fixed; top: 12px; left: 12px;
  z-index: 300; background: var(--surface); border: 1px solid var(--border);
  color: var(--text); padding: 8px 12px; border-radius: 6px; cursor: pointer;
  font-size: 18px; }
@media (max-width: 768px) {
  #menu-toggle { display: block; }
  #sidebar { transform: translateX(-100%); transition: transform .2s; }
  #sidebar.open { transform: translateX(0); }
  #main { margin-left: 0; }
  .page { padding: 60px 20px 32px; }
  #progress-bar { left: 0; }
}
"""

JS = """
const pages = document.querySelectorAll('.page');
const navItems = document.querySelectorAll('.nav-item');

function showPage(id) {
  pages.forEach(p => p.classList.remove('active'));
  navItems.forEach(n => n.classList.remove('active'));
  const page = document.getElementById(id);
  const nav = document.querySelector(`[data-page="${id}"]`);
  if (page) { page.classList.add('active'); window.scrollTo(0,0); }
  if (nav) nav.classList.add('active');
  localStorage.setItem('lastPage', id);
  document.getElementById('sidebar').classList.remove('open');
  updateProgress();
}

function updateProgress() {
  const el = document.scrollingElement;
  const pct = (el.scrollTop / (el.scrollHeight - el.clientHeight)) * 100;
  document.getElementById('progress-fill').style.width = pct + '%';
}

document.addEventListener('scroll', updateProgress);

// Search filter
document.getElementById('search-bar').addEventListener('input', function() {
  const q = this.value.toLowerCase();
  document.querySelectorAll('.nav-item').forEach(item => {
    item.style.display = item.textContent.toLowerCase().includes(q) ? '' : 'none';
  });
});

// Restore last page
const last = localStorage.getItem('lastPage') || 'page-0';
showPage(last);

// Mobile menu
document.getElementById('menu-toggle').onclick = () => {
  document.getElementById('sidebar').classList.toggle('open');
};

// Make checkboxes persistent
document.querySelectorAll('input[type=checkbox]').forEach(cb => {
  const key = 'cb_' + cb.parentElement.textContent.trim().substring(0,40);
  cb.checked = localStorage.getItem(key) === '1';
  cb.addEventListener('change', () => localStorage.setItem(key, cb.checked ? '1' : '0'));
});
"""

def md_to_html(text):
    # Convert [ ] and [x] to proper checkboxes
    text = re.sub(r'- \[ \] ', '- <input type="checkbox"> ', text)
    text = re.sub(r'- \[x\] ', '- <input type="checkbox" checked> ', text)
    return markdown.markdown(
        text,
        extensions=['tables', 'fenced_code', 'nl2br'],
    )

def build():
    os.chdir('/home/user/Czechlanguagecenter')

    nav_html = ''
    nav_html += '<div class="nav-section">Start here</div>'

    pages_html = ''

    for i, (fname, label) in enumerate(MODULES):
        page_id = f'page-{i}'

        # Badge
        if 'B1' in fname:
            badge = '<span class="badge badge-b1">B1</span>'
        elif 'citizenship' in fname or 'roadmap' in fname:
            badge = '<span class="badge badge-both">Both</span>'
        elif fname == 'README.md':
            badge = ''
        else:
            badge = '<span class="badge badge-a2">A2</span>'

        if i == 5:
            nav_html += '<div class="nav-section">B1 Level</div>'
        elif i == 3:
            nav_html += '<div class="nav-section">A2 Exam Prep</div>'
        elif i == 1:
            nav_html += '<div class="nav-section">A2 Foundation</div>'

        nav_html += f'<button class="nav-item" data-page="{page_id}" onclick="showPage(\'{page_id}\')">{label}{badge}</button>\n'

        # Read markdown
        try:
            with open(fname, encoding='utf-8') as f:
                raw = f.read()
            content = md_to_html(raw)
        except FileNotFoundError:
            content = f'<p>File {fname} not found.</p>'

        pages_html += f'<div class="page" id="{page_id}"><div class="content">{content}</div></div>\n'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Czech Study Materials — Prince</title>
<style>{CSS}</style>
</head>
<body>
<button id="menu-toggle">☰</button>
<div id="progress-bar"><div id="progress-fill"></div></div>

<aside id="sidebar">
  <div id="sidebar-header">
    <h1>Czech Study</h1>
    <p>A2 → B1 · Citizenship Exam</p>
  </div>
  <input type="text" id="search-bar" placeholder="Search modules...">
  <nav>
    {nav_html}
  </nav>
</aside>

<main id="main">
{pages_html}
</main>

<script>{JS}</script>
</body>
</html>"""

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print('Done! Open index.html in your browser.')
    print(f'File size: {os.path.getsize("index.html") // 1024} KB')

if __name__ == '__main__':
    build()
