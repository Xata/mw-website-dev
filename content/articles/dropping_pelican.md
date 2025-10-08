Title: I Miss Simple Websites
Author: Maciej
Date: 2025-10-08 14:30
Category: blog
Tags: blog, python, pelican, static-site-generator, web-development, geocities
Summary: Replacing Pelican with a custom static site generator

# I Miss Simple Websites

I rebuilt this website using a custom static site generator I wrote in Python. The whole thing is about 200 lines of code. No plugins, no themes, no config files. Just Python, Make, and Markdown.

## Why?

I originally built this site with [Pelican](https://getpelican.com/). Pelican is great—it's well-designed, actively maintained, and has a solid plugin ecosystem. If you're building a Python blog, you should check it out.

But I kept thinking about geocities. Those janky personal homepages from the late 90s where you'd edit HTML in Notepad, upload it via FTP, and suddenly have a website. I missed that directness.

With Pelican, I had `pelicanconf.py`, `publishconf.py`, theme directories, and plugin folders. For a portfolio with maybe a dozen posts, it felt like overkill. I wanted something simpler.

## Building My Own

What does a static site generator actually need to do for a simple blog?

1. Parse Markdown front matter
2. Convert Markdown to HTML
3. Inject content into a template
4. Copy static files

That's it. So I wrote `build.py`:

```python
#!/usr/bin/env python3
import re
import shutil
from datetime import datetime
from pathlib import Path
import markdown
```

The script:
- Parses metadata from Markdown files (simple `key: value` format)
- Converts `{static}` tags to relative paths
- Renders HTML using Python-Markdown
- Injects content into a single template
- Generates a blog index sorted by date
- Copies images and static files

No configuration files. If I want to change something, I edit `build.py` or the template.

## The Template

One template file: `templates/base.html`. Two placeholders:

```html
<title>{{ title }}</title>
...
<main>{{ content }}</main>
```

CSS is inline. The whole template is about 100 lines. It's responsive, supports dark mode via `prefers-color-scheme`, and uses system fonts. No JavaScript.

## The Makefile

```makefile
build:
    python build.py

serve: build
    cd output && python -m http.server 8000

clean:
    rm -rf output/
```

Three commands.

## What I Lost

- No RSS/Atom feeds
- No tag pages or category pages
- No pagination
- No i18n support
- No plugin ecosystem

For a personal portfolio, none of this matters.

## What I Gained

- **Understanding**: I know exactly how it works
- **Speed**: Build is instant
- **Simplicity**: One Python file, one template, one Makefile
- **Control**: Want to change something? Edit 200 lines of Python
- **Dependencies**: Just `Markdown==3.9` in requirements.txt

When something breaks, I just read `build.py`. No digging through framework docs.

## Conclusion

Use Pelican if you're building a blog. It's genuinely good software.

But this project wasn't about finding a "better" solution. It was pure nostalgia. I wanted that geocities feeling of just making something without learning a framework first.

You can check out the source on my GitHub. The entire generator fits in one file.

Thank you for reading!
