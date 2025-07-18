"""Declaration of plugin hooks."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cucumber_expressions.parameter_type import ParameterType


def pytest_bdd_cucumber_expression_param_types() -> set[ParameterType]:
    """Define additional custom Cucumber Expression parameter types.

    Returns:
        A set of custom parameter types.
    """
