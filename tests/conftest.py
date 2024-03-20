import os
import pytest


def dir_fixture(name):
    @pytest.fixture
    def _dir_fixture():
        return os.path.join(os.path.dirname(__file__), "data", name)

    return _dir_fixture


python_data = dir_fixture("python")
cpp_data = dir_fixture("cpp")
generic_data = dir_fixture("generic")
