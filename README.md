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

Personal portfolio site with my blog and a resume page. Built with 200ish lines of Python and no giant bulky frameworks.

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

Your template file (`templates/base.html`) needs two placeholders:
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

The script replaces `{{ title }}` with your page title and `{{ content }}` with your HTML.

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

### Customizing

Edit ```build.py```. The functions are commented and the whole file is readable in about 10 minutes.

### Limitations

There's no RSS, no tag pages, no pagination, and no plugins. For a portfolio site I don't need any of that. If you do, you probably want Pelican or Hugo instead.

### Why

I wanted the geocities feeling of just making a website without learning a framework first.

Thank you for checking this out!

## License

See [LICENSE](LICENSE) for details.
