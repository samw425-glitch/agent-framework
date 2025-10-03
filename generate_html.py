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

def clean_filename(s):
    """
    Clean string to be safe as filename:
    - Replace spaces with underscores
    - Remove special chars
    - Keep letters, numbers, underscores only
    """
    s = s.strip().replace(' ', '_')
    s = re.sub(r'[^\w\-]', '', s)
    return s

def wrap_paragraphs(text):
    """
    Converts plain text / Markdown-like text into HTML paragraphs.
    """
    paragraphs = text.split('\n')
    paragraphs = [f"<p>{html.escape(p.strip())}</p>" for p in paragraphs if p.strip()]
    return '\n'.join(paragraphs)

for index, row in df.iterrows():
    topic = row['topic']
    language = row['language']
    content = row['post']

    filename = f"{clean_filename(topic)}_{language}.html"
    filepath = os.path.join(output_dir, filename)

    html_content = f"""
    <!DOCTYPE html>
    <html lang="{language[:2].lower()}">
    <head>
        <meta charset="utf-8">
        <title>{html.escape(topic)} ({language})</title>
    </head>
    <body>
        <h1>{html.escape(topic)}</h1>
        {wrap_paragraphs(content)}
    </body>
    </html>
    """

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)

print(f"✅ HTML files generated in '{output_dir}' ({len(df)} posts)")
