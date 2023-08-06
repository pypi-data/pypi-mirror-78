from pathlib import Path

from eppy.modeleditor import IDDAlreadySetError
import pytest

from besos import config
from besos import eplus_funcs
from besos import eppy_funcs as ef


@pytest.fixture
def idd_default():
    _, ep_directory = eplus_funcs.get_ep_path(config.energy_plus_version)
    return Path(ep_directory, "Energy+.idd").resolve()


@pytest.fixture
def clean_idd_name():
    # reset the iddname
    # this kind of monkeypatch should not be used in production
    # it may mess with how idfs are processed

    # clear name before test
    old_name = ef.IDF.iddname
    ef.IDF.iddname = None
    yield
    # restore name after test
    ef.IDF.iddname = old_name


@pytest.fixture
def idd_other(clean_idd_name):
    return Path(config.data_dir, "Custom_Long_Fields.idd")


def test_idd_no_conflict_defaults(clean_idd_name):
    ef.get_idf()
    ef.get_idf()


def test_idd_no_conflict_explicit_default(idd_default, clean_idd_name):
    ef.get_idf()
    ef.get_idf(idd_file=idd_default)


def test_idd_no_conflict_same(idd_other, clean_idd_name):
    ef.get_idf(idd_file=idd_other)
    ef.get_idf(idd_file=idd_other)


def test_idd_conflict(idd_other, clean_idd_name):
    with pytest.raises(IDDAlreadySetError):
        ef.get_idf()
        ef.get_idf(idd_file=idd_other)


def test_idd_warns(idd_other, clean_idd_name):
    ef.get_idf(idd_file=idd_other)
    with pytest.warns(UserWarning, match="idd is already set to: "):
        ef.get_idf()
