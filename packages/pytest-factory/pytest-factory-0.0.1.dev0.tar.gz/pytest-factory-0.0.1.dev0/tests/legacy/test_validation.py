"""Test factory registration validation."""

import factory
import pytest
from pytest_factory import factory_fixture


class NoModelFactory(factory.Factory):
    """A factory without model."""


class AbstractFactory(factory.Factory):
    """Abstract factory."""

    class Meta:
        abstract = True
        model = dict


def test_without_model():
    """Test that factory without model can't be registered."""
    with pytest.raises(AssertionError):
        factory_fixture(NoModelFactory)


def test_abstract():
    with pytest.raises(AssertionError):
        factory_fixture(AbstractFactory)
