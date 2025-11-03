#!/usr/bin/env python3
"""
Simple static site generator for Maciej's Dev Blog
Converts Markdown files to HTML with a minimal early aesthetic

HOW TO USE THIS FOR YOUR OWN SITE:
1. Install dependencies: pip install markdown
2. Create this folder structure:
   - content/articles/    (your blog posts as .md files)
   - content/pages/       (static pages like about.md, resume.md)
   - content/img/         (images referenced in your content)
   - content/extra/       (favicon, robots.txt, etc.)
   - templates/base.html  (your HTML template with {{ title }} and {{ content }} placeholders)
3. Run: python build.py
4. Your site will be generated in output/
"""

import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import markdown


def parse_metadata(content: str) -> tuple[Dict[str, str], str]:
    """
    Parse metadata from the top of a Markdown file.

    Expected format at the start of your .md files:
        Title: Your Article Title
        Date: 2024-03-24 20:19
        Category: blog
        Tags: python, web, tutorial

        Your actual content starts here...

    Rules:
    - Metadata must be at the very beginning (no blank lines before it)
    - Format is "Key: Value" (colon-separated)
    - Keys can only contain letters/numbers/underscores
    - Metadata section ends at the first blank line
    - Keys are converted to lowercase in the returned dict
    - Lines starting with # or ** are not treated as metadata

    Args:
        content: The full text content of the Markdown file

    Returns:
        tuple of (metadata_dict, body_content)
        - metadata_dict: Dict with keys like 'title', 'date', 'tags'
        - body_content: The rest of the file (actual Markdown content)
    """
    lines = content.split('\n')
    metadata = {}
    body_lines = []
    in_metadata = False

    for line in lines:
        # Stop parsing metadata after first empty line
        # This lets you have "Key: Value" elsewhere in your content
        if in_metadata and not line.strip():
            in_metadata = False
            continue

        # Check if this line looks like metadata (at the very beginning only)
        if not in_metadata and not metadata and ':' in line and not line.startswith('#') and not line.startswith('**'):
            # Extract the part before the colon
            potential_key = line.split(':', 1)[0].strip()
            # Only treat it as metadata if it's a simple word (no spaces, special chars)
            if potential_key.isalpha() or potential_key.replace('_', '').isalnum():
                key, value = line.split(':', 1)
                metadata[key.strip().lower()] = value.strip()
                in_metadata = True
                continue

        # Continue parsing metadata lines
        if in_metadata and ':' in line and not line.startswith('#') and not line.startswith('**'):
            potential_key = line.split(':', 1)[0].strip()
            if potential_key.isalpha() or potential_key.replace('_', '').isalnum():
                key, value = line.split(':', 1)
                metadata[key.strip().lower()] = value.strip()
                continue

        # Everything else goes into the body
        if not in_metadata:
            body_lines.append(line)

    return metadata, '\n'.join(body_lines)


def convert_static_tags(content: str, is_article: bool = False) -> str:
    """
    Convert {static} tags to relative paths for images and assets.

    This lets you write image references like:
        ![My image]({static}/img/photo.jpg)

    And they get converted to the correct relative path depending on the page type:
    - For articles (in articles/ subdirectory): {static} becomes ".."
      Result: ../img/photo.jpg
    - For pages (in root directory): {static} becomes "."
      Result: ./img/photo.jpg

    This way you don't have to remember different paths for articles vs pages.

    Args:
        content: The Markdown content to process
        is_article: True if this is a blog article, False if it's a regular page

    Returns:
        Content with {static} replaced by the appropriate relative path
    """
    if is_article:
        # Articles are one level deep (output/articles/post.html)
        # so they need to go up one directory to reach img/
        return re.sub(r'\{static\}', '..', content)
    else:
        # Pages are at the root (output/about.html)
        # so they can reference img/ directly
        return re.sub(r'\{static\}', '.', content)


def render_template(template_path: str, title: str, content: str) -> str:
    """
    Render HTML using simple template replacement.

    Your template file (templates/base.html) should have these placeholders:
    - {{ title }}: Gets replaced with the page title (for <title> and <h1>)
    - {{ content }}: Gets replaced with the actual HTML content

    Example template:
        <!DOCTYPE html>
        <html>
        <head>
            <title>{{ title }}</title>
        </head>
        <body>
            {{ content }}
        </body>
        </html>

    This is a dead-simple templating system - no Jinja2 or other dependencies.
    If you need more complex templating, consider upgrading to a real template engine.

    Args:
        template_path: Path to your HTML template file
        title: The page title to insert
        content: The HTML content to insert

    Returns:
        Complete HTML page with placeholders replaced
    """
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    # Replace the two placeholders
    html = template.replace('{{ title }}', title)
    html = html.replace('{{ content }}', content)
    return html


def process_article(md_path: Path, output_dir: Path, template_path: str) -> Dict[str, str]:
    """
    Process a single blog article from Markdown to HTML.

    This function:
    1. Reads the .md file
    2. Extracts metadata (title, date, tags, etc.)
    3. Converts {static} tags to proper relative paths
    4. Converts Markdown to HTML
    5. Adds a "Posted on [date]" line at the top
    6. Wraps it in your HTML template
    7. Writes the final HTML file

    Example input file (content/articles/my-post.md):
        Title: My First Post
        Date: 2024-03-24 20:19
        Tags: python, web

        This is my **first** blog post!

    Example output (output/articles/my-post.html):
        Full HTML page with "Posted on March 24, 2024" and the converted content.

    Args:
        md_path: Path to the Markdown file to process
        output_dir: Directory to write the HTML file to (usually output/articles/)
        template_path: Path to the HTML template

    Returns:
        Dictionary with article metadata (used for generating the blog index):
        - title: Article title
        - date: Parsed datetime object
        - date_str: Original date string
        - slug: Filename without extension (e.g., "my-post")
        - filename: Output filename (e.g., "my-post.html")
        - tags: Comma-separated tags
        - category: Article category
    """
    # Read the Markdown file
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split into metadata and body
    metadata, body = parse_metadata(content)

    # Convert {static} tags to relative paths (articles need ../)
    body = convert_static_tags(body, is_article=True)

    # Convert Markdown to HTML using Python-Markdown library
    # Extensions used:
    # - 'extra': Tables, footnotes, and other nice features
    # - 'codehilite': Syntax highlighting for code blocks
    # - 'fenced_code': Support for ```code``` blocks
    md = markdown.Markdown(extensions=['extra', 'codehilite', 'fenced_code'])
    html_content = md.convert(body)

    # Extract and parse the article metadata
    title = metadata.get('title', 'Untitled')
    date_str = metadata.get('date', '')
    date_obj = None

    # Parse the date if present
    # Expected format: "2024-03-24 20:19" or "2024-03-24"
    if date_str:
        try:
            # Just grab the YYYY-MM-DD part (ignore time if present)
            date_obj = datetime.strptime(date_str.split()[0], '%Y-%m-%d')
        except:
            # If date parsing fails, continue without a date object
            pass

    # Add "Posted on [date]" metadata to the top of the article
    if date_str:
        # Format as "March 24, 2024"
        formatted_date = date_obj.strftime('%B %d, %Y') if date_obj else date_str
        meta_html = f'<div class="article-meta">Posted on {formatted_date}</div>\n'
        html_content = meta_html + html_content

    # Determine output filename (same as input, but .html instead of .md)
    slug = md_path.stem  # Filename without extension
    output_file = output_dir / f"{slug}.html"

    # Wrap content in template and write to file
    full_html = render_template(template_path, title, html_content)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_html)

    # Return metadata for use in building the blog index
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
    """
    Process a static page from Markdown to HTML.

    Similar to process_article(), but for non-blog pages like:
    - About page
    - Resume/CV
    - Contact page
    - Any other standalone page

    Key differences from articles:
    - No "Posted on [date]" metadata added
    - {static} tags convert to "./" instead of "../"
    - Output goes to root (output/) instead of output/articles/
    - No return of metadata (pages don't appear in blog index)

    Example input file (content/pages/about.md):
        title: About Me
        date: 2024-01-01

        Hi, I'm a developer who loves **Python**!

    Example output (output/about.html):
        Full HTML page with title "About Me" and the converted content.

    Args:
        md_path: Path to the Markdown file to process
        output_dir: Directory to write the HTML file to (usually output/)
        template_path: Path to the HTML template

    Returns:
        The slug (filename without extension) of the processed page
    """
    # Read the Markdown file
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split into metadata and body
    metadata, body = parse_metadata(content)

    # Convert {static} tags to relative paths (pages use ./)
    body = convert_static_tags(body, is_article=False)

    # Convert Markdown to HTML
    md = markdown.Markdown(extensions=['extra', 'codehilite', 'fenced_code'])
    html_content = md.convert(body)

    # Get title from metadata, or generate from filename if not provided
    # e.g., "my_page.md" becomes "My Page" if no title is set
    title = metadata.get('title', md_path.stem.replace('_', ' ').title())

    # Output file goes to root directory (not articles/)
    output_file = output_dir / f"{md_path.stem}.html"

    # Wrap content in template and write to file
    full_html = render_template(template_path, title, html_content)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_html)

    return md_path.stem


def build_blog_index(articles: List[Dict], output_dir: Path, template_path: str):
    """
    Build the blog index page (listing of all articles).

    This creates a page at output/blog.html that lists all your blog posts
    in reverse chronological order (newest first).

    The page includes:
    - A "Blog" heading
    - List of articles with dates and titles
    - Links to each article

    Example output structure:
        <h1>Blog</h1>
        <ul class="article-list">
            <li>
                <span class="article-date">2024-03-24</span>
                <a href="articles/my-post.html">My First Post</a>
            </li>
            ...
        </ul>

    You can style this with CSS classes:
    - .article-list: The <ul> containing all articles
    - .article-date: The date span
    - .article-title: The article link

    Args:
        articles: List of article metadata dicts (from process_article())
        output_dir: Directory to write blog.html to (usually output/)
        template_path: Path to the HTML template
    """
    # Sort articles by date (newest first)
    # Only include articles that have a valid date
    sorted_articles = sorted(
        [a for a in articles if a['date']],
        key=lambda x: x['date'],
        reverse=True
    )

    # Build the HTML content for the blog index
    content = '<h1>Blog</h1>\n'
    content += '<ul class="article-list">\n'

    for article in sorted_articles:
        # Format date as YYYY-MM-DD
        date_formatted = article['date'].strftime('%Y-%m-%d') if article['date'] else ''
        content += f'''    <li>
        <span class="article-date">{date_formatted}</span>
        <a href="articles/{article['filename']}" class="article-title">{article['title']}</a>
    </li>\n'''

    content += '</ul>\n'

    # Wrap in template and write to file
    html = render_template(template_path, 'Blog', content)

    with open(output_dir / 'blog.html', 'w', encoding='utf-8') as f:
        f.write(html)


def build_home_page(output_dir: Path, template_path: str):
    """
    Build the home page (index.html).

    This implementation creates a redirect to /resume.html, but you can customize
    this to do whatever you want:
    - Show a landing page
    - Display recent blog posts
    - Show your portfolio
    - Redirect to your blog (change url=/blog.html)

    Current behavior: Instant redirect to resume.html using meta refresh tag.

    Args:
        output_dir: Directory to write index.html to (usually output/)
        template_path: Path to the HTML template (not used for redirect, but kept for consistency)
    """
    # Simple HTML with meta refresh for instant redirect
    # The "0" means redirect immediately (0 seconds delay)
    # Change the url= value to redirect somewhere else
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
    """
    Build the 404 error page.

    This page is shown when someone tries to visit a URL that doesn't exist.
    Most web servers and hosting platforms (like GitHub Pages, Netlify, etc.)
    will automatically serve 404.html when a page is not found.

    Customize the content variable below to change what's shown on your 404 page.

    Args:
        output_dir: Directory to write 404.html to (usually output/)
        template_path: Path to the HTML template
    """
    # HTML content for the 404 page
    # Customize this to match your site's personality
    content = '''<h1>404 - Page Not Found</h1>
<p>The page you're looking for doesn't exist. I probably deleted it for some reason.</p>
<p><a href="/index.html">Go home</a> or check out the <a href="/blog.html">blog</a>.</p>'''

    # Wrap in template and write to file
    html = render_template(template_path, '404 - Page Not Found', content)

    with open(output_dir / '404.html', 'w', encoding='utf-8') as f:
        f.write(html)


def main():
    """
    Main build process - orchestrates the entire site generation.

    This is what gets called when you run: python build.py

    Build steps:
    1. Set up paths
    2. Clean and recreate output directory
    3. Copy static assets (images, fonts, CSS, etc.)
    4. Process all blog articles
    5. Process all static pages
    6. Generate blog index
    7. Generate home page
    8. Generate 404 page

    Directory structure expected:
        build.py                    (this file)
        content/
            articles/               (blog posts)
                post1.md
                post2.md
            pages/                  (static pages)
                about.md
                resume.md
            img/                    (images)
            fonts/                  (web fonts, optional)
            extra/                  (favicon, robots.txt, etc.)
        templates/
            base.html               (HTML template)
            styles.css              (CSS file)
        output/                     (generated site - this gets created)

    After running, your site will be in output/ ready to deploy.
    """
    # Set up paths relative to this script's location
    base_dir = Path(__file__).parent  # Directory containing build.py
    content_dir = base_dir / 'content'
    output_dir = base_dir / 'output'
    template_path = base_dir / 'templates' / 'base.html'

    # Clean and create output directory
    # WARNING: This deletes everything in output/!
    # Make sure you never edit files directly in output/ - they'll be lost on rebuild
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir()

    # Create articles directory for blog posts
    articles_dir = output_dir / 'articles'
    articles_dir.mkdir()

    # Copy images to output
    # All images from content/img/ go to output/img/
    if (content_dir / 'img').exists():
        shutil.copytree(content_dir / 'img', output_dir / 'img')

    # Copy fonts (if you use web fonts)
    # Optional - delete this block if you don't use custom fonts
    if (content_dir / 'fonts').exists():
        shutil.copytree(content_dir / 'fonts', output_dir / 'fonts')

    # Copy extra files (favicon, robots.txt, etc.)
    # Files in content/extra/ get copied to output/
    if (content_dir / 'extra').exists():
        for item in (content_dir / 'extra').iterdir():
            # Special handling for security.txt (goes in .well-known/ directory)
            # See: https://securitytxt.org/
            if item.name == 'security.txt':
                well_known_dir = output_dir / '.well-known'
                well_known_dir.mkdir(exist_ok=True)
                shutil.copy(item, well_known_dir / 'security.txt')
            else:
                # Everything else goes to root
                shutil.copy(item, output_dir / item.name)

    # Copy CSS file from templates to output
    css_file = base_dir / 'templates' / 'styles.css'
    if css_file.exists():
        shutil.copy(css_file, output_dir / 'styles.css')

    # Copy .nojekyll file (tells GitHub Pages not to use Jekyll)
    # Only needed if you deploy to GitHub Pages
    nojekyll_file = base_dir / '.nojekyll'
    if nojekyll_file.exists():
        shutil.copy(nojekyll_file, output_dir / '.nojekyll')

    # Process all blog articles
    articles = []  # Will hold metadata for building the blog index
    articles_path = content_dir / 'articles'
    if articles_path.exists():
        for md_file in sorted(articles_path.glob('*.md')):
            print(f'Processing article: {md_file.name}')
            article_info = process_article(md_file, articles_dir, template_path)
            articles.append(article_info)

    # Process all static pages
    pages_path = content_dir / 'pages'
    if pages_path.exists():
        for md_file in pages_path.glob('*.md'):
            print(f'Processing page: {md_file.name}')
            process_page(md_file, output_dir, template_path)

    # Build the blog index page (list of all articles)
    print('Building blog index...')
    build_blog_index(articles, output_dir, template_path)

    # Build the home page
    print('Building home page...')
    build_home_page(output_dir, template_path)

    # Build the 404 error page
    print('Building 404 page...')
    build_404_page(output_dir, template_path)

    # Print summary
    print(f'\nSite built successfully in {output_dir}/')
    print(f'Total articles: {len(articles)}')


if __name__ == '__main__':
    # This block runs when you execute: python build.py
    # It doesn't run if you import this file as a module
    main()
