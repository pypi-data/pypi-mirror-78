import pytest

import eppy_funcs as ef
import sampling
from evaluator import EvaluatorEP
from objectives import MeterReader
from optimizer import NSGAII
from parameters import expand_plist
from problem import EPProblem


@pytest.fixture
def building():
    # returns the basic building
    building = ef.get_building()
    return building


@pytest.fixture
def parameters():
    # The parameters for the problem/evaluator
    parameters = expand_plist(
        {
            "NonRes Fixed Assembly Window": {
                "U-Factor": (0.1, 5),
                "Solar Heat Gain Coefficient": (0.01, 0.99),
            },
            "Mass NonRes Wall Insulation": {"Thickness": (0.01, 0.09)},
        }
    )
    return parameters


@pytest.mark.slow
def test_objectives(building, parameters, regtest):
    """Testing custom functions and basic objective creation"""

    def variance(result):
        return result.data["Value"].var()

    objectives = [
        MeterReader("Electricity:Facility", name="Electricity Usage"),
        MeterReader("Electricity:Facility", func=variance, name="Electricity Variance"),
    ]
    problem = EPProblem(inputs=parameters, outputs=objectives)

    evaluator = EvaluatorEP(problem, building)
    samples = sampling.dist_sampler(sampling.seeded_sampler, problem, 10)
    results = evaluator.df_apply(samples, keep_input=True)

    value = results.iloc[0]["Electricity Variance"]

    with regtest:
        print(f"{value:.5E}")


@pytest.mark.slow
def test_constraints(building, parameters):
    """Testing for expected output with certain constraints, also acts as a test for using NSGAII"""

    objectives = ["Electricity:Facility", "Gas:Facility"]
    problem = EPProblem(
        inputs=parameters,
        outputs=objectives,
        constraints=["CO2:Facility"],
        constraint_bounds=[">=750"],
    )

    evaluator = EvaluatorEP(problem, building)

    results = NSGAII(evaluator, evaluations=10, population_size=2)

    value = results.iloc[0]["CO2:Facility"] + results.iloc[0]["violation"]
    assert (
        value >= 750
    ), f"Constraint did not effect output, value should be above 750 but was: {value}"

    # Check to make sure the output changes with different constraints
    problem = EPProblem(
        inputs=parameters,
        outputs=objectives,
        constraints=["CO2:Facility"],
        constraint_bounds=["<=750"],
    )

    evaluator = EvaluatorEP(problem, building)

    results = NSGAII(evaluator, evaluations=10, population_size=2)

    value = results.iloc[0]["CO2:Facility"] - results.iloc[0]["violation"]
    assert (
        value <= 750
    ), f"Constraint did not effect output, value should be below 750 but was: {value}"
