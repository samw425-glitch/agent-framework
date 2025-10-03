import pandas as pd
import os
import re
import html

csv_file = 'generated_posts.csv'

if not os.path.exists(csv_file):
    raise FileNotFoundError(f"{csv_file} not found. Make sure your CSV exists.")

df = pd.read_csv(csv_file)
output_dir = 'output_html'
os.makedirs(output_dir, exist_ok=True)
css_file = 'style.css'

def clean_filename(s):
    s = s.strip().replace(' ', '_')
    s = re.sub(r'[^\w\-]', '', s)
    return s

def wrap_paragraphs(text):
    paragraphs = text.split('\n')
    paragraphs = [f"<p>{html.escape(p.strip())}</p>" for p in paragraphs if p.strip()]
    return '\n'.join(paragraphs)

def insert_affiliate_links(content, url):
    paragraphs = [p for p in content.split('\n') if p.strip()]
    if not paragraphs:
        return content
    mid_index = len(paragraphs) // 2
    link_html = f'<a href="{url}" target="_blank" class="btn btn-success my-3 btn-lg">Check it out!</a>'
    paragraphs.insert(mid_index, link_html)
    paragraphs.append(link_html)
    return '\n'.join(paragraphs)

nav_items = ""
for idx, row in df.iterrows():
    filename = f"{clean_filename(row['topic'])}_{row['language']}.html"
    nav_items += f'<li class="nav-item"><a class="nav-link" href="{filename}">{html.escape(row["topic"])}</a></li>\n'

nav_html = f"""
<nav class="navbar navbar-expand-lg navbar-dark bg-primary sticky-top shadow">
  <div class="container-fluid">
    <a class="navbar-brand" href="#">Tech Blog</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav ms-auto">
        {nav_items}
      </ul>
      <button class="btn btn-outline-light ms-3" id="theme-toggle">Dark Mode</button>
    </div>
  </div>
</nav>
"""

for index, row in df.iterrows():
    topic = row['topic']
    language = row['language']
    content = row['post']
    affiliate_url = row.get('affiliate_url', 'https://affiliate-link.com')
    content_with_links = insert_affiliate_links(content, affiliate_url)
    filename = f"{clean_filename(topic)}_{language}.html"
    filepath = os.path.join(output_dir, filename)

    html_content = f"""
<!DOCTYPE html>
<html lang="{language[:2].lower()}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(topic)} ({language})</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&family=Montserrat:wght@700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{css_file}">
<style>
body {{ font-family: 'Roboto', sans-serif; transition: background-color 0.3s, color 0.3s; }}
h1, h2, h3 {{ font-family: 'Montserrat', sans-serif; }}
.btn-success:hover {{ background-color: #28a745; transform: scale(1.05); transition: 0.2s; }}
footer {{ text-align: center; padding: 2rem 0; font-size: 0.9rem; color: #666; }}
</style>
</head>
<body class="bg-light text-dark">

{nav_html}

<div class="container my-5" style="max-width: 900px;">
    <div class="card shadow-sm p-5 mb-5 bg-white rounded">
        <h1 class="card-title mb-4">{html.escape(topic)}</h1>
        <div class="card-body">
            {wrap_paragraphs(content_with_links)}
        </div>
    </div>
</div>

<footer>
    &copy; 2025 Tech Blog | <a href="https://github.com/samw425-glitch" target="_blank">GitHub</a>
</footer>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
<script>
const toggle = document.getElementById('theme-toggle');
toggle.addEventListener('click', () => {{
    document.body.classList.toggle('bg-dark');
    document.body.classList.toggle('text-light');
}});
</script>
</body>
</html>
"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)

print(f"✅ HTML files generated in '{output_dir}' ({len(df)} posts) with full modern blog finesse!")
