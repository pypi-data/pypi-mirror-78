import textwrap
import pathlib
import unittest.mock

import pytest
import jaraco.collections
from jaraco.test.pytest import allow


class Bunch(dict, jaraco.collections.ItemsAsAttributes):
    pass


@pytest.fixture
def tmpdir_cur(tmpdir):
    with tmpdir.as_cwd():
        yield tmpdir


def test_pytest_addoption(tmpdir_cur):
    parser = Bunch(_groups=[])
    parser.addoption = unittest.mock.MagicMock()
    pathlib.Path('pyproject.toml').write_text(
        textwrap.dedent(
            """
            [tool.jaraco.pytest.opts.--opt]
            bar = "baz"
            """
        )
    )
    allow.pytest_addoption(parser, None)
    parser.addoption.assert_called_with('--opt', bar="baz")
