Title: I Miss Simple Websites
Author: Maciej
Date: 2025-10-08 14:30
Category: blog
Tags: blog, python, pelican, static-site-generator, web-development, geocities
Summary: Replacing Pelican with a custom static site generator

# I Miss Simple Websites

I ended up rebuilding this website to use a custom static site generator that I wrote in Python. The whole project ended up being about 280-300ish lines of code. Just pure Python, Make, and Markdown.

## Why?

I originally built this website with [Pelican](https://getpelican.com/). At the time I was obsessed with using Python for everything. I wanted to avoid the popular static website generators and ended up finding Pelican. Pelican is great and actively maintained.

Do you remember those old geocities websites? Those super janky personal homepages from the late 90's where you'd edit HTML in Notepad (because you didn't know anything else existed)? I really miss having that directness.

Anyway, with Pelican, I had to have `pelicanconf.py`, `publishconf.py`, theme directories, and plugin folders. For a portfolio website that sometimes sees a post, Pelican felt like complete overkill. I wanted to have something way simpler.

## Building My Own

I wanted my static website generator to do the following:

1. Parse Markdown front matter
2. Convert Markdown to HTML
3. Inject content into a template
4. Copy static files

So I wrote `build.py`:

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

CSS is lives in ```content/templates/styles.css```. The whole template is about 100 lines. No JavaScript (I don't like JavaScript but I can't seem to avoid it).

## The Makefile

This was the first time that I wrote my own Makefile. I actually enjoyed learning about this. I didn't know you could use Makefiles like this. 

```makefile
build:
    python build.py

serve: build
    cd output && python -m http.server 8000

clean:
    rm -rf output/
```

Now you just have three commands to use when developing or previewing pages:
```zsh
make build
make serve
make clean
```

## Articles

I kept the format that Pelican was using for articles. Maybe at some point I will add more functionality to parse through the other fields. Until then though, they exist. Why not? I don't feel like going back through them all. Maybe I can make an LLM do it? 

## What I lost

- No RSS/Atom feeds
- No tag pages or category pages
- No pagination
- No i18n support
- No plugin ecosystem
- No community support

For my personal website, I don't think any of this really matters too much. It would be nice to have RSS/Atoms feeds but that would mean modifying my ```robots.txt```. Which ehhh, I don't want to do. 

## What I Gained

- **Understanding**: I know exactly how it works
- **Speed**: Build is almost instant
- **Simplicity**: One Python file, one template, one Makefile
- **Control**: Want to change something? Edit 200 lines of Python
- **Dependencies**: Just `Markdown==3.9` in requirements.txt

When something breaks, I can just read `build.py`. No digging through any framework docs or using an LLM as a crutch. 

## Conclusion

Use Pelican if you're building a blog. It's a really cool Python static site generator.

But this project wasn't about finding a "better" solution. It was pure nostalgia. I wanted that geocities feeling of just making something without learning a framework first. I want the internet to be fun and owned by individuals again (ironic since I'm hosting this on GitHub Pages).

Thank you so much for reading!
