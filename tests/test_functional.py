import textwrap


def test_functional(pytester):
    pytester.makefile(
        ".feature",
        textwrap.dedent(
            """\
            Feature: Cucumber Expressions
                Scenario: Simple
                    Given a simple foo
                    When the user executes bar 5 times
                    And another thing without parameter
                    Then there should be 0.3 liter of baz
            """,
        ),
    )
    pytester.makepyfile(
        textwrap.dedent(
            """\
                from pytest_bdd import scenarios
                from pytest_bdd_cucumber_expression import given, when, then

                scenarios("test_functional.feature")

                @given("a simple {word}")
                def _():
                    pass

                @when("the user executes {word} {int} times", param_names=("what", "times"))
                def _(what, times):
                    assert what == "bar"
                    assert times == 5

                @when("another thing without parameter")
                def _():
                    pass

                @then("there should be {float} liter of {word}", param_names=("amount", "what"))
                def _(amount, what):
                    assert amount == 0.3
                    assert what == "baz"
            """,  # noqa: E501
        ),
    )

    result = pytester.runpytest("-s")
    result.assert_outcomes(passed=1)
