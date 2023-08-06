"""
    sphinxcontrib.relative-link-corrector
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    A Sphinx extension to correct relative links when using .md as an input.

    :copyright: Copyright 2020 Nokia
    :license: Apache License 2.0, see LICENSE for details.
"""
import os as _os
from . import implementation as _impl
import pbr.version

if False:
    # For type annotations
    from typing import Any, Dict  # noqa
    from sphinx.application import Sphinx  # noqa

__version__ = pbr.version.VersionInfo(
    'relative-link-corrector').version_string()


def setup(app):
    app.connect('build-finished', _impl.relative_link_corrector)

    return {
        'version': '0.0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
