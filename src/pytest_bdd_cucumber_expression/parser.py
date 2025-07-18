"""Wrap the cucumber expression into a StepParser."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Any, ClassVar, override

import pytest_bdd.parsers
from cucumber_expressions.expression import CucumberExpression
from cucumber_expressions.parameter_type import ParameterType
from cucumber_expressions.parameter_type_registry import ParameterTypeRegistry

if TYPE_CHECKING:
    from cucumber_expressions.parameter_type import ParameterType

class CucumberExpressionParser(pytest_bdd.parsers.StepParser):
    """A StepParser for Cucumber Expressions.

    Args:
        name: The step text.
        param_names: A tuple of expression argument names.
    """

    extra_param_types: ClassVar[set[ParameterType]] = set()

    @override
    def __init__(self, name: str, param_names: tuple[str, ...] | None = None) -> None:
        super().__init__(name)
        self.cuexp = CucumberExpression(name, self._param_type_registry)

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

    @cached_property
    def _param_type_registry(self) -> ParameterTypeRegistry:
        registry = ParameterTypeRegistry()

        for param_type in CucumberExpressionParser.extra_param_types:
            registry.define_parameter_type(param_type)

        return registry
