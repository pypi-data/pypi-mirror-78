from dataclasses import dataclass

import factory

import pytest_factory


@dataclass
class Foo:
    value: int
    expected: int


@dataclass
class Bar:
    foo: Foo


@pytest_factory.factory_fixture
class FooFactory(factory.Factory):
    class Meta:
        model = Foo

    value = 0
    expected = 0

    @factory.post_generation
    def set1(self, created, value, **kwargs):
        self.value = 1


def it_invokes_postgen_set1(foo):
    expected = 1
    actual = foo.value
    assert expected == actual
