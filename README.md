# mwal.dev

This repository contains the source code for my portfolio website at [mwal.dev](https://mwal.dev).

![GitHub top language](https://img.shields.io/github/languages/top/Xata/mw-website-dev?style=for-the-badge)
![GitHub repo size](https://img.shields.io/github/repo-size/Xata/mw-website-dev?style=for-the-badge)
![GitHub Last Commit](https://img.shields.io/github/last-commit/Xata/mw-website-dev?style=for-the-badge)
![Build Status](https://img.shields.io/github/actions/workflow/status/Xata/mw-website-dev/deploy.yml?style=for-the-badge)
![Website](https://img.shields.io/website?down_message=offline&style=for-the-badge&up_message=online&url=https%3A%2F%2Fmwal.dev)
![Maintained](https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=for-the-badge)
![IE Incompatible](https://img.shields.io/badge/IE-incompatible-red?style=for-the-badge)

## About

A personal portfolio website showcasing my projects and resume. The site includes:

- **Blog**: Technical guides and posts about technologies I work with
- **Resume**: Professional experience and background

## Development

**Prerequisites:**
- Python 3.13.x

**Setup:**
```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

**Build and serve locally:**
```bash
make build    # Build the site
make serve    # Serve at http://localhost:8000
make clean    # Remove generated files
```

## Structure

```
content/
├── articles/     # Blog posts
├── pages/        # Static pages
├── img/          # Images
├── fonts/        # Fonts included
└── extra/        # Static asset

templates/        # HTML templates
output/           # Generated site
build.py          # Build script
```

## Fonts

This project uses [Inter](https://github.com/rsms/inter) by Rasmus Andersson, licensed under the SIL Open Font License 1.1. See [content/fonts/LICENSE.txt](content/fonts/LICENSE.txt).

## Using This For Your Own Site

So you want to use this for your own website? Cool! Here's how to get started.

The whole thing is about 200 lines of Python. No config files, no plugin directories, just one script that converts Markdown to HTML. If you want to change something, you edit `build.py`. That's it.

### What You'll Need

First, install the only dependency:
```bash
pip install markdown
```

That's literally it. One package.

### Setting Up Your Project

Create this folder structure:
```
your-site/
├── content/
│   ├── articles/     # Your blog posts (.md files)
│   ├── pages/        # Static pages (about.md, resume.md, etc.)
│   ├── img/          # Images
│   └── extra/        # favicon, robots.txt, whatever
├── templates/
│   └── base.html     # Your HTML template
└── build.py          # Copy this from the repo
```

### The Template

Your template file (`templates/base.html`) needs exactly two placeholders:
```html
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    <!-- Your CSS goes here -->
</head>
<body>
    {{ content }}
</body>
</html>
```

That's it. The script replaces `{{ title }}` with your page title and `{{ content }}` with your HTML. No Jinja2, no fancy templating system. Just find-and-replace.

### Writing Content

Articles go in `content/articles/` and look like this:
```markdown
Title: My First Post
Date: 2024-03-24 20:19
Category: blog
Tags: python, web

Your content starts here...
```

Pages go in `content/pages/` and look like this:
```markdown
title: About Me
date: 2024-01-01

Your content starts here...
```

The metadata format is just `key: value`. The script parses everything before the first blank line as metadata. Everything else becomes your content.

### Images

Use `{static}` tags when referencing images:
```markdown
![My photo]({static}/img/photo.jpg)
```

The script converts this to the correct relative path automatically:
- Articles (in subdirectory): `../img/photo.jpg`
- Pages (in root): `./img/photo.jpg`

This way you don't have to remember different paths for different page types.

### Building Your Site

Run this:
```bash
python build.py
```

Your site gets generated in `output/`. That's it. You're done.

The script:
- Cleans the output directory
- Copies your images and static files
- Processes all your Markdown files
- Generates a blog index (sorted by date)
- Creates index.html and 404.html

### What Gets Generated

- Articles: `output/articles/{filename}.html`
- Pages: `output/{filename}.html`
- Blog listing: `output/blog.html`
- Home page: `output/index.html`
- 404 page: `output/404.html`

### Customizing Things

The script is intentionally simple. Want to change how something works? Just edit `build.py`:
- Home page redirect: Check out `build_home_page()`
- 404 page content: Look at `build_404_page()`
- Blog index layout: Edit `build_blog_index()`
- Add more Markdown features: Update the `markdown.Markdown()` calls

All the functions have detailed comments explaining what they do. It's about 200 lines total. You can read the whole thing in like 10 minutes.

### What You're Giving Up

No RSS feeds. No tag pages. No pagination. No plugin ecosystem.

For a personal portfolio site, none of that really matters. If you need those features, use a real static site generator like Pelican or Hugo.

### Why I Built This

I wanted that geocities feeling of just making something without learning a framework first. Sometimes it's nice to just have one Python file that does exactly what you need and nothing else.

Thank you for checking this out!

## License

See [LICENSE](LICENSE) for details.


