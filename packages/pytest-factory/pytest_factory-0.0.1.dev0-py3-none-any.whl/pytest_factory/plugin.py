"""
This pytest plugin inspects all test modules and classes found during
collection and converts factory_fixture-decorated factory classes into
actual pytest fixtures.

This conversion is done during collection, rather than at decoration time, so
as to avoid using call frame information to determine where to place generated
fixtures
"""
import inspect
from typing import List, Tuple, Type

import pytest
from _pytest.fixtures import call_fixture_func, FixtureRequest
from _pytest.python import Module

from .factory_fixtures import FactoryFixtureMixin, is_factory_fixture


@pytest.hookimpl(hookwrapper=True)
def pytest_pycollect_makemodule(path, parent):
    outcome = yield
    module: Module = outcome.get_result()  # will raise if outcome was exception

    process_factory_fixtures(module.module)


def pytest_pycollect_makeitem(collector, name, obj):
    if inspect.isclass(obj):
        process_factory_fixtures(obj)


def process_factory_fixtures(parent):
    """Turn all factory_fixtures in a class/module into actual pytest fixtures
    """
    factory_fixtures: List[Tuple[str, Type[FactoryFixtureMixin]]] = (
        inspect.getmembers(parent, is_factory_fixture))

    for name, attr in factory_fixtures:
        attr._pytest_factory_contribute_to_parent(parent, name)

    return parent


@pytest.fixture
def factory_request(request):
    return PytestFactoryRequest(request)


class PytestFactoryRequest:
    def __init__(self, request: FixtureRequest):
        self.request = request
        self.deferred = []

    def defer(self, methods):
        self.deferred.append(set(methods))

    def evaluate(self):
        while self.deferred:
            methods = self.deferred[-1]
            for method in tuple(methods):
                call_fixture_func(method, self.request, {})
                methods.remove(method)

            if not methods:
                del self.deferred[-1]


@pytest.mark.tryfirst
def pytest_runtest_call(item):
    """Before the test item is called."""
    try:
        request = item._request
    except AttributeError:
        return
    factory_request = request.getfixturevalue('factory_request')
    factory_request.evaluate()
    assert not factory_request.deferred
