"""
A pytest plugin to shim pytest commandline options for fowards compatibility
"""
from __future__ import absolute_import, division, print_function, unicode_literals

__version__ = "0.1.0"

import pytest
from packaging import version


def pytest_addoption(parser):
    pytest_version = version.parse(pytest.__version__)
    if pytest_version >= version.parse("6.0.0.rc1"):
        return
    kwargs = {"help": "noop (does nothing)"}
    group = parser.getgroup(
        __name__,
        description=(
            "shim options for pytest fowards compatibility, "
            "see https://pypi.org/project/{}".format(__name__)
        ),
    )
    group.addoption("--no-summary", action="store_true", default=False, **kwargs)
    group.addoption("--strict-config", action="store_true", **kwargs)
    group.addoption("--code-highlight", default="yes", choices=["yes", "no"], **kwargs)
    group.addoption("--no-header", action="store_true", default=False, **kwargs)
    if pytest_version >= version.parse("5.3.0"):
        return
    group.addoption("--log-auto-indent", kwargs)
