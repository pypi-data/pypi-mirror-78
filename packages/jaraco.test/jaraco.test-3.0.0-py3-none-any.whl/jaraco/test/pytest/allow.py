import toml
from more_itertools import flatten
from jaraco.context import suppress
from jaraco.functools import apply


def none_as_empty(ob):
    """
    >>> none_as_empty({})
    {}
    >>> none_as_empty(None)
    {}
    >>> none_as_empty({'a': 1})
    {'a': 1}
    """
    return ob or {}


@apply(none_as_empty)
@suppress(Exception)
def read_opts(filename):
    with open(filename) as strm:
        defn = toml.load(strm)
    return defn["tool"]["jaraco"]["pytest"]["opts"]


def get_supported_options(parser):
    """
    >>> from jaraco.test.pytest.test_allow import Bunch
    >>> parser = Bunch(
    ...     _groups = [Bunch(
    ...         options = [Bunch(
    ...             _long_opts=['--opt'])])])
    >>> list(get_supported_options(parser))
    ['--opt']
    """
    return flatten(
        opts._long_opts for group in parser._groups for opts in group.options
    )


def pytest_addoption(parser, pluginmanager):
    opts = read_opts('pyproject.toml')
    missing = set(opts) - set(get_supported_options(parser))
    for opt in missing:
        parser.addoption(opt, **opts[opt])
