# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pelican', 'pelican.plugins.thumbnailer']

package_data = \
{'': ['*'],
 'pelican.plugins.thumbnailer': ['test_data/*', 'test_data/subdir/*']}

install_requires = \
['Pillow>=7.2,<8.0', 'pelican>=4.5,<5.0']

extras_require = \
{'markdown': ['markdown>=3.2.2,<4.0.0']}

setup_kwargs = {
    'name': 'pelican-thumbnailer',
    'version': '1.0.0',
    'description': 'Thumbnailer is a Pelican plugin creates smaller versions of images found in a directory',
    'long_description': "Thumbnailer: A Plugin for Pelican\n=================================\n\n[![Build Status](https://img.shields.io/github/workflow/status/pelican-plugins/thumbnailer/build)](https://github.com/pelican-plugins/thumbnailer/actions) [![PyPI Version](https://img.shields.io/pypi/v/pelican-thumbnailer)](https://pypi.org/project/pelican-thumbnailer/)\n\nThumbnailer is a Pelican plugin that creates thumbnails for all of the images found under a specific directory, in various thumbnail sizes.\n\n\nInstallation\n-------------\n\nThis plugin can be installed via:\n\n    python -m pip install pelican-thumbnailer\n\n[Pillow](https://pillow.readthedocs.io/) will be automatically installed in order to resize the images, and the thumbnail will only be re-built if it doesn't already exist (to save processing time). Depending on your local environment and your image types, you may need to also install [external libraries](https://pillow.readthedocs.io/en/stable/installation.html#external-libraries) to add support for certain image file formats.\n\n\nConfiguration\n-------------\n\n* `IMAGE_PATH` is the path to the image directory. It should reside inside your content directory, and defaults to `pictures`.\n* `THUMBNAIL_DIR` is the path to the output sub-directory where the thumbnails are generated.\n* `THUMBNAIL_SIZES` is a dictionary mapping size name to size specifications.\n  The generated filename will be `originalname_thumbnailname.ext` unless `THUMBNAIL_KEEP_NAME` is set.\n* `THUMBNAIL_KEEP_NAME` is a Boolean that, if set, puts the file with the original name in a `thumbnailname` folder, named like the key in `THUMBNAIL_SIZES`.\n* `THUMBNAIL_KEEP_TREE` is a Boolean that, if set, saves the image directory tree.\n* `THUMBNAIL_INCLUDE_REGEX` is an optional string that is used as regular expression to restrict thumbnailing to matching files. By default all files not starting with a dot are respected.\n\nSizes can be specified using any of the following formats:\n\n* `wxh` will resize to exactly `wxh` cropping as necessary to get that size\n* `wx?` will resize so that the width is the specified size, and the height will scale to retain aspect ratio\n* `?xh` same as `wx?` but will height being a set size\n* `s` is a shorthand for `wxh` where `w=h`\n\n\n## Contributing\n\nContributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].\n\nTo start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.\n\n[existing issues]: https://github.com/pelican-plugins/thumbnailer/issues\n[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html\n",
    'author': 'Justin Mayer',
    'author_email': 'entroP@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pelican-plugins/thumbnailer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
