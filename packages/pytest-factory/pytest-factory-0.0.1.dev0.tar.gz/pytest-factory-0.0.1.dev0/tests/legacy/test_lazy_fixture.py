"""Test LazyFixture related features."""

import factory
import pytest

from pytest_factory import factory_fixture, LazyFixture


class User(object):
    """User account."""

    def __init__(self, username, password, is_active):
        self.username = username
        self.password = password
        self.is_active = is_active


@factory_fixture
class UserFactory(factory.Factory):
    """User factory."""

    class Meta:
        model = User

    username = factory.faker.Faker("user_name")
    password = factory.faker.Faker("password")
    is_active = factory.LazyAttribute(lambda f: f.password == "ok")


partial_user = UserFactory.as_fixture(
    password=LazyFixture('ok_password'),
)


@pytest.fixture
def ok_password():
    return "ok"


@pytest.mark.parametrize("user__password", [LazyFixture("ok_password")])
def test_lazy_attribute(user):
    """Test LazyFixture value is extracted before the LazyAttribute is called."""
    assert user.is_active


def test_lazy_attribute_partial(partial_user):
    """Test LazyFixture value is extracted before the LazyAttribute is called. Partial."""
    assert partial_user.is_active


def test_lazy_attribute_partial_factory(partial_user_factory):
    """Test LazyFixture works when called from factory fixture"""
    # XXX: This test fails in the pytest-factoryboy codebase — partial_user_factory
    #      isn't even defined. I'm honestly not sure how overriding declarations
    #      should work here. Yes, we could simply create a factory subclass that
    #      overrides password with LazyFixture('ok_password'), but this would conflict
    #      with behaviour elsewhere, like being able to provide LazyFixtures as values
    #      for postgen methods.
    partial_user = partial_user_factory()
    assert partial_user.password == 'ok'
