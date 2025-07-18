"""Pytest plugin entry point.

Publish own hooks, and provide hook implementations.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .parser import CucumberExpressionParser

if TYPE_CHECKING:

    import pytest


def pytest_addhooks(pluginmanager: pytest.PytestPluginManager) -> None:  # noqa: D103
    from . import hooks  # noqa: PLC0415

    pluginmanager.add_hookspecs(hooks)


def pytest_configure(config: pytest.Config) -> None:  # noqa: D103
    result = config.hook.pytest_bdd_cucumber_expression_param_types()

    for r in result:
        CucumberExpressionParser.extra_param_types.union(r)
