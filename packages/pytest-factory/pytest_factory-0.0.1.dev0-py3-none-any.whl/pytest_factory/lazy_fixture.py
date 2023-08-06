from inspect import signature

from _pytest.fixtures import FixtureRequest
from factory.builder import Resolver
from factory.declarations import BaseDeclaration


class LazyFixture(BaseDeclaration):
    def __init__(self, fixture):
        """Lazy pytest fixture wrapper.

        :param fixture: Fixture name or callable with dependencies.
        """
        super(LazyFixture, self).__init__()

        self.fixture = fixture

        if callable(self.fixture):
            params = signature(self.fixture).parameters.values()
            self.requested_fixtures = [
                param.name
                for param in params
                if param.kind == param.POSITIONAL_OR_KEYWORD
            ]
        else:
            self.requested_fixtures = [self.fixture]

    def evaluate(self, instance, step=None, extra=None):
        """Evaluate the lazy fixture.

        :param request: pytest request object.
        :return: evaluated fixture.
        """
        if step is None and extra is None:
            request = instance
        else:
            request = self.search_for_request(instance)

        if callable(self.fixture):
            kwargs = {
                arg: request.getfixturevalue(arg)
                for arg in self.requested_fixtures
            }
            return self.fixture(**kwargs)
        else:
            return request.getfixturevalue(self.fixture)

    def search_for_request(self, instance: Resolver) -> FixtureRequest:
        """Find the pytest FixtureRequest up the factory chain

        Usually, the instance passed to evaluate() directly contains the
        pytest_request Param, which is defined by wrap_factory_class, used in
        factory class fixtures.

        However, if a factory class is used directly (e.g. in a postgen method),
        wrap_factory_class won't have declared pytest_request on it. We must
        instead extract the request from the parent step(s).
        """
        while instance is not None:
            try:
                return instance.pytest_request
            except AttributeError:
                instance = instance.factory_parent
