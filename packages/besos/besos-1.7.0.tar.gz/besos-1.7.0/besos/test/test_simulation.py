from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from sklearn import linear_model, pipeline
from sklearn.preprocessing import StandardScaler

import config
import eplus_funcs
import eppy_funcs as ef
import sampling
from evaluator import EvaluatorEP
from parameters import FieldSelector, Parameter, RangeParameter
from problem import EPProblem


# Some code taken and adapted from example notebooks, made to work through pytest


@pytest.fixture
def building():
    return ef.get_building()


@pytest.fixture
def unexpanded():
    return ef.get_building(str(Path(config.data_dir, "unexpanded.idf").resolve()))


@pytest.fixture
def parameters():
    parameters = [
        Parameter(
            FieldSelector(
                object_name="NonRes Fixed Assembly Window",
                field_name="Solar Heat Gain Coefficient",
            ),
            value_descriptor=RangeParameter(0.01, 0.99),
        ),
        Parameter(
            FieldSelector("Lights", "*", "Watts per Zone Floor Area"),
            value_descriptor=RangeParameter(8, 12),
            name="Lights Watts/Area",
        ),
    ]
    return parameters


@pytest.fixture
def problem(parameters):
    objectives = ["Electricity:Facility"]
    problem = EPProblem(parameters, objectives)
    return problem


@pytest.fixture
def samples(problem):
    samples = sampling.dist_sampler(sampling.seeded_sampler, problem, 10)
    return samples


@pytest.mark.slow
def test_expected_values(building, problem, samples, regtest):
    """check that the obtained results are consistent when using the same inputs"""

    def get_plot_data(model, density):
        # helper function from the example notebook
        p1 = problem.inputs[0].value_descriptor
        a = np.linspace(p1.min, p1.max, density)
        p2 = problem.inputs[1].value_descriptor
        b = np.linspace(p2.min, p2.max, density)
        plot_data = pd.DataFrame(
            np.transpose([np.tile(a, len(b)), np.repeat(b, len(a))]),
            columns=problem.names("inputs"),
        )
        return pd.concat([plot_data, pd.Series(model.predict(plot_data))], axis=1)

    evaluator = EvaluatorEP(problem, building, error_mode="Silent")
    train = evaluator.df_apply(samples, keep_input=True)
    print(problem.names())
    x, y, c = problem.names()

    # train and get the values
    model = pipeline.make_pipeline(StandardScaler(), linear_model.Ridge())
    model.fit(train[[x, y]].values, train[c].values)
    density = 30
    df = get_plot_data(model, int(density * 1.5))

    # check to see if the extremes and the midpoint are the expected values
    with regtest:
        for index in [0, 1012, 2024]:
            print(f"{df.iloc[index][0]:.5E}")


@pytest.mark.slow
def test_expand_objects_run(unexpanded):
    eplus_funcs.run_building(unexpanded, err_dir=config.err_dir / "BESOS_Errors")
