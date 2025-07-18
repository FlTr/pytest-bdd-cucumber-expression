"""Step decorators to be used as direct replacements of pytest-bdd decorators.

The decorators wrap their corresponding pytest-bdd step decorators to provide native
Cucumber Expression support without the need of explicilty calling a parser.
Additionally there is the possibility to call `ce` as parser.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any, ParamSpec, TypeVar

import pytest_bdd

from .parser import CucumberExpressionParser

if TYPE_CHECKING:
    from collections.abc import Callable

    P = ParamSpec("P")
    T = TypeVar("T")


def ce(
    name: str,
    param_names: tuple[str, ...] | None = None,
) -> CucumberExpressionParser:
    """Cucumber expression parser.

    To be used similiar to pytest-bdd native parsers.

    Args:
        name: The step text.
        param_names: Optional names for step parameters.

    Returns:
        CucumberExpressionParser (StepParser) object.
    """
    return CucumberExpressionParser(name, param_names)


def given(
    name: str,
    *,
    param_names: tuple[str, ...] | None = None,
    **kwargs: Any,  # noqa: ANN401
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Given step decorator with native Cucumber Expression support.

    Args:
        name: Step name.
        param_names: Optional names for step parameters.
        kwargs: Optional further arguments for underlying pytest-bdd step decorator.

    Returns:
        Decorator function for the step.
    """
    return pytest_bdd.given(ce(name, param_names), **kwargs)


def when(
    name: str,
    *,
    param_names: tuple[str, ...] | None = None,
    **kwargs: Any,  # noqa: ANN401
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """When step decorator with native Cucumber Expression support.

    Args:
        name: Step name.
        param_names: Optional names for step parameters.
        kwargs: Optional further arguments for underlying pytest-bdd step decorator.

    Returns:
        Decorator function for the step.
    """
    return pytest_bdd.when(ce(name, param_names), **kwargs)


def then(
    name: str,
    *,
    param_names: tuple[str, ...] | None = None,
    **kwargs: Any,  # noqa: ANN401
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Then step decorator with native Cucumber Expression support.

    Args:
        name: Step name.
        param_names: Optional names for step parameters.
        kwargs: Optional further arguments for underlying pytest-bdd step decorator.

    Returns:
        Decorator function for the step.
    """
    return pytest_bdd.then(ce(name, param_names), **kwargs)
