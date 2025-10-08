#!/usr/bin/env python3
"""
Simple static site generator for Maciej's Dev Blog
Converts Markdown files to HTML with a minimal early 2000s aesthetic
"""

import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import markdown


def parse_metadata(content: str) -> tuple[Dict[str, str], str]:
    """Parse metadata from Markdown front matter"""
    lines = content.split('\n')
    metadata = {}
    body_lines = []
    in_metadata = False

    for line in lines:
        # Stop parsing metadata after first empty line
        if in_metadata and not line.strip():
            in_metadata = False
            continue

        # Only parse metadata at the very beginning (simple key: value format)
        if not in_metadata and not metadata and ':' in line and not line.startswith('#') and not line.startswith('**'):
            # Check if it looks like metadata (simple word before colon)
            potential_key = line.split(':', 1)[0].strip()
            if potential_key.isalpha() or potential_key.replace('_', '').isalnum():
                key, value = line.split(':', 1)
                metadata[key.strip().lower()] = value.strip()
                in_metadata = True
                continue

        if in_metadata and ':' in line and not line.startswith('#') and not line.startswith('**'):
            potential_key = line.split(':', 1)[0].strip()
            if potential_key.isalpha() or potential_key.replace('_', '').isalnum():
                key, value = line.split(':', 1)
                metadata[key.strip().lower()] = value.strip()
                continue

        # Everything else is body
        if not in_metadata:
            body_lines.append(line)

    return metadata, '\n'.join(body_lines)


def convert_static_tags(content: str, is_article: bool = False) -> str:
    """Convert {static} tags to relative paths"""
    if is_article:
        return re.sub(r'\{static\}', '..', content)
    else:
        return re.sub(r'\{static\}', '.', content)


def render_template(template_path: str, title: str, content: str) -> str:
    """Render HTML using simple template replacement"""
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    html = template.replace('{{ title }}', title)
    html = html.replace('{{ content }}', content)
    return html


def process_article(md_path: Path, output_dir: Path, template_path: str) -> Dict[str, str]:
    """Process a single article Markdown file"""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    metadata, body = parse_metadata(content)

    # Convert static tags
    body = convert_static_tags(body, is_article=True)

    # Convert Markdown to HTML
    md = markdown.Markdown(extensions=['extra', 'codehilite', 'fenced_code'])
    html_content = md.convert(body)

    # Get article info
    title = metadata.get('title', 'Untitled')
    date_str = metadata.get('date', '')
    date_obj = None

    if date_str:
        try:
            # Parse date like "2024-03-24 20:19"
            date_obj = datetime.strptime(date_str.split()[0], '%Y-%m-%d')
        except:
            pass

    # Add metadata to content
    if date_str:
        formatted_date = date_obj.strftime('%B %d, %Y') if date_obj else date_str
        meta_html = f'<div class="article-meta">Posted on {formatted_date}</div>\n'
        html_content = meta_html + html_content

    # Create output filename
    slug = md_path.stem
    output_file = output_dir / f"{slug}.html"

    # Render final HTML
    full_html = render_template(template_path, title, html_content)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_html)

    return {
        'title': title,
        'date': date_obj,
        'date_str': date_str,
        'slug': slug,
        'filename': f"{slug}.html",
        'tags': metadata.get('tags', ''),
        'category': metadata.get('category', '')
    }


def process_page(md_path: Path, output_dir: Path, template_path: str) -> str:
    """Process a page Markdown file"""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    metadata, body = parse_metadata(content)

    # Convert static tags
    body = convert_static_tags(body, is_article=False)

    # Convert Markdown to HTML
    md = markdown.Markdown(extensions=['extra', 'codehilite', 'fenced_code'])
    html_content = md.convert(body)

    title = metadata.get('title', md_path.stem.replace('_', ' ').title())

    # Create output filename
    output_file = output_dir / f"{md_path.stem}.html"

    # Render final HTML
    full_html = render_template(template_path, title, html_content)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_html)

    return md_path.stem


def build_blog_index(articles: List[Dict], output_dir: Path, template_path: str):
    """Build the blog index page"""
    # Sort articles by date (newest first)
    sorted_articles = sorted(
        [a for a in articles if a['date']],
        key=lambda x: x['date'],
        reverse=True
    )

    content = '<h1>Blog</h1>\n'
    content += '<ul class="article-list">\n'

    for article in sorted_articles:
        date_formatted = article['date'].strftime('%Y-%m-%d') if article['date'] else ''
        content += f'''    <li>
        <span class="article-date">{date_formatted}</span>
        <a href="articles/{article['filename']}" class="article-title">{article['title']}</a>
    </li>\n'''

    content += '</ul>\n'

    html = render_template(template_path, 'Blog', content)

    with open(output_dir / 'blog.html', 'w', encoding='utf-8') as f:
        f.write(html)


def build_home_page(output_dir: Path, template_path: str):
    """Build the home page - redirect to resume"""
    content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0; url=/resume.html">
    <title>Redirecting...</title>
</head>
<body>
    <p>Redirecting to <a href="/resume.html">resume</a>...</p>
</body>
</html>'''

    with open(output_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(content)


def build_404_page(output_dir: Path, template_path: str):
    """Build the 404 error page"""
    content = '''<h1>404 - Page Not Found</h1>
<p>The page you're looking for doesn't exist. I probably deleted it for some reason.</p>
<p><a href="/index.html">Go home</a> or check out the <a href="/blog.html">blog</a>.</p>'''

    html = render_template(template_path, '404 - Page Not Found', content)

    with open(output_dir / '404.html', 'w', encoding='utf-8') as f:
        f.write(html)


def main():
    """Main build process"""
    base_dir = Path(__file__).parent
    content_dir = base_dir / 'content'
    output_dir = base_dir / 'output'
    template_path = base_dir / 'templates' / 'base.html'

    # Clean and create output directory
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir()

    # Create articles directory
    articles_dir = output_dir / 'articles'
    articles_dir.mkdir()

    # Copy images and static files
    if (content_dir / 'img').exists():
        shutil.copytree(content_dir / 'img', output_dir / 'img')

    if (content_dir / 'extra').exists():
        for item in (content_dir / 'extra').iterdir():
            # Handle security.txt specially - goes to .well-known/
            if item.name == 'security.txt':
                well_known_dir = output_dir / '.well-known'
                well_known_dir.mkdir(exist_ok=True)
                shutil.copy(item, well_known_dir / 'security.txt')
            else:
                shutil.copy(item, output_dir / item.name)

    # Copy CSS file
    css_file = base_dir / 'templates' / 'styles.css'
    if css_file.exists():
        shutil.copy(css_file, output_dir / 'styles.css')

    # Copy .nojekyll for GitHub Pages
    nojekyll_file = base_dir / '.nojekyll'
    if nojekyll_file.exists():
        shutil.copy(nojekyll_file, output_dir / '.nojekyll')

    # Process all articles
    articles = []
    articles_path = content_dir / 'articles'
    if articles_path.exists():
        for md_file in sorted(articles_path.glob('*.md')):
            print(f'Processing article: {md_file.name}')
            article_info = process_article(md_file, articles_dir, template_path)
            articles.append(article_info)

    # Process pages
    pages_path = content_dir / 'pages'
    if pages_path.exists():
        for md_file in pages_path.glob('*.md'):
            print(f'Processing page: {md_file.name}')
            process_page(md_file, output_dir, template_path)

    # Build index pages
    print('Building blog index...')
    build_blog_index(articles, output_dir, template_path)

    print('Building home page...')
    build_home_page(output_dir, template_path)

    print('Building 404 page...')
    build_404_page(output_dir, template_path)

    print(f'\nSite built successfully in {output_dir}/')
    print(f'Total articles: {len(articles)}')


if __name__ == '__main__':
    main()
