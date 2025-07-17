"""Wrap the cucumber expression into a StepParser."""

from __future__ import annotations

from typing import Any, override

import pytest_bdd.parsers
from cucumber_expressions.expression import CucumberExpression
from cucumber_expressions.parameter_type_registry import ParameterTypeRegistry


class CucumberExpressionParser(pytest_bdd.parsers.StepParser):
    """A StepParser for Cucumber Expressions.

    Args:
        name: The step text.
        param_names: A tuple of expression argument names.
    """

    @override
    def __init__(self, name: str, param_names: tuple[str, ...] | None = None) -> None:
        super().__init__(name)
        self.cuexp = CucumberExpression(name, ParameterTypeRegistry())

        self.params: tuple[str, ...] | tuple[()] = ()

        if param_names is not None:
            self.params = param_names

    @override
    def parse_arguments(self, name: str) -> dict[str, Any] | None:
        matches = self.cuexp.match(name)

        if matches is None:
            return None

        if len(self.params) < len(matches):
            self.params += tuple(
                f"_cep{i}" for i in range(len(self.params), len(matches))
            )

        return dict(zip(self.params, [m.value for m in matches], strict=True))

    @override
    def is_matching(self, name: str) -> bool:
        return self.cuexp.match(name) is not None
