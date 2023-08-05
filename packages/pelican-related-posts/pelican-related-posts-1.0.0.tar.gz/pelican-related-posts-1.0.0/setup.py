# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pelican', 'pelican.plugins.related_posts']

package_data = \
{'': ['*']}

install_requires = \
['pelican>=4.5,<5.0']

extras_require = \
{'markdown': ['markdown>=3.2.2,<4.0.0']}

setup_kwargs = {
    'name': 'pelican-related-posts',
    'version': '1.0.0',
    'description': 'Pelican plugin that adds a list of related posts to an article.',
    'long_description': 'Related Posts: A Plugin for Pelican\n===================================\n\n[![Build Status](https://img.shields.io/github/workflow/status/pelican-plugins/related-posts/build)](https://github.com/pelican-plugins/related-posts/actions) [![PyPI Version](https://img.shields.io/pypi/v/pelican-related-posts)](https://pypi.org/project/pelican-related-posts/)\n\nRelated Posts is a Pelican plugin that adds a list of related posts to an article by adding a `related_posts` variable to the article’s context.\n\n\nInstallation\n------------\n\nThis plugin can be installed via:\n\n    python -m pip install pelican-related-posts\n\n\nUsage\n-----\n\nBy default, up to five related articles are listed. You can customize this value by defining `RELATED_POSTS_MAX` in your settings file:\n\n    RELATED_POSTS_MAX = 10\n\nYou can then use the `article.related_posts` variable in your templates. For example:\n\n    {% if article.related_posts %}\n        <ul>\n        {% for related_post in article.related_posts %}\n            <li><a href="{{ SITEURL }}/{{ related_post.url }}">{{ related_post.title }}</a></li>\n        {% endfor %}\n        </ul>\n    {% endif %}\n\nYour related posts should share a common tag. You can also use `related_posts:` in your post’s meta-data. The `related_posts:` meta-data works together with your existing slugs:\n\n    related_posts: slug1, slug2, slug3, ... slugN\n\n`N` represents the `RELATED_POSTS_MAX` value.\n\nAdditionally, you can specify the following in your settings file:\n\n    RELATED_POSTS_SKIP_SAME_CATEGORY = True\n\nWith this setting, `article.related_posts` will contain only related posts from categories other than the original article\'s.\n\n\nContributing\n------------\n\nContributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].\n\nTo start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.\n\n[existing issues]: https://github.com/pelican-plugins/related-posts/issues\n[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html\n',
    'author': 'Justin Mayer',
    'author_email': 'entroP@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pelican-plugins/related-posts',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
