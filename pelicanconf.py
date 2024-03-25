AUTHOR = 'Maciej Wal'
SITENAME = "Maciej's Dev Blog"
SITEURL = ""

THEME = "theme"

# Plugin settings
PLUGIN_PATHS = ['plugins/', ]
PLUGINS = ['i18n_subsites', ]

JINJA_ENVIRONMENT = {
    'extensions': ['jinja2.ext.i18n'],
}

BOOTSTRAP_THEME = 'simplex'
PYGMENTS_STYLE = 'monokai'

PATH = "content"

TIMEZONE = 'America/Denver'

DEFAULT_LANG = 'en'

# Article Settings
ARTICLE_PATHS = ['articles']
ARTICLE_URL = 'articles/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = 'articles/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'

# Page settings
PAGE_PATHS = ['pages']
PAGE_URL = 'pages/{slug}/'
PAGE_SAVE_AS = 'pages/{slug}/index.html'

# Category settings
CATEGORY_URL = 'category/{slug}'
CATEGORY_SAVE_AS = 'category/{slug}/index.html'

# Tag settings
TAG_URL = 'tag/{slug}'
TAG_SAVE_AS = 'tag/{slug}/index.html'

# Static content settings
STATIC_PATHS = ['img', 'extra',]

EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/favicon.ico': {'path': 'favicon.ico'},
}

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Links for Pelican site and plugins
SOCIAL = (('Github', 'https://github.com/Xata'),
          ('LinkedIn', 'https://www.linkedin.com/in/maciejwal/'),
          )

GITHUB_URL = 'https://github.com/Xata'

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True