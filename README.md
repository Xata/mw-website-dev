# mwal.dev

This repository contains the source code for my portfolio website at [mwal.dev](https://mwal.dev).

![GitHub top language](https://img.shields.io/github/languages/top/Xata/mw-website-dev?style=for-the-badge)
![GitHub Last Commit](https://img.shields.io/github/last-commit/Xata/mw-website-dev?style=for-the-badge)
![GitHub repo size](https://img.shields.io/github/repo-size/Xata/mw-website-dev?style=for-the-badge)

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

## License

See [LICENSE](LICENSE) for details.


