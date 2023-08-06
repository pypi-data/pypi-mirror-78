from dataclasses import dataclass

import factory
import pytest
from pytest_assert_utils import assert_model_attrs
from pytest_lambda import static_fixture

import pytest_factory
from pytest_factory import LazyFixture


@dataclass
class Model:
    first_name: str
    last_name: str


@pytest_factory.factory_fixture
class UserFactory(factory.Factory):
    class Meta:
        model = Model

    first_name = LazyFixture('first_name')
    last_name = LazyFixture('last_name')


class DescribeFactoryFixture:
    first_name = static_fixture('FIRST')
    last_name = static_fixture('LAST')

    def it_uses_overridden_values(self, user_factory):
        user = user_factory()

        assert_model_attrs(
            user,
            first_name='FIRST',
            last_name='LAST',
        )


    class CaseOverriddenDecl:
        other_last_name = static_fixture('OTHER LAST')

        def it_uses_overridden_decl_value(self, user_factory):
            user = user_factory(
                last_name=LazyFixture('other_last_name'),
            )

            assert_model_attrs(
                user,
                first_name='FIRST',
                last_name='OTHER LAST',
            )
