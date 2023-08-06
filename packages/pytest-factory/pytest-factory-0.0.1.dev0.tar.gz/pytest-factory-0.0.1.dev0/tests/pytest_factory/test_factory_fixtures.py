from dataclasses import dataclass

import factory
import pytest
from pytest_assert_utils import assert_model_attrs, util
from pytest_lambda import static_fixture

import pytest_factory


@dataclass
class User:
    username: str
    password: str
    is_active: bool


@pytest_factory.factory_fixture
class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    password = factory.Faker('password')
    is_active = True


class DescribeFactoryFixture:
    def it_exposes_factory_as_fixture(self, user_factory):
        user = user_factory()

        assert_model_attrs(
            user,
            username=util.Any(str),
            password=util.Any(str),
            is_active=True,
        )

    def it_allows_overriding_declarations(self, user_factory):
        user = user_factory(username='alfred')

        assert_model_attrs(
            user,
            username='alfred',
            password=util.Any(str),
            is_active=True,
        )

    class ContextDeclaredInClass:
        @pytest_factory.factory_fixture
        class UserFactory(factory.Factory):
            class Meta:
                model = User

            username = 'nested_user'
            password = 'nested_password'
            is_active = False

        def it_exposes_factory_as_fixture(self, user_factory):
            user = user_factory()

            assert_model_attrs(
                user,
                username='nested_user',
                password='nested_password',
                is_active=False,
            )

        def it_allows_overriding_declarations(self, user_factory):
            user = user_factory(username='alfred')

            assert_model_attrs(
                user,
                username='alfred',
                password='nested_password',
                is_active=False,
            )


class DescribeModelFixtures:

    class CaseDefaultValues:
        def it_creates_user_fixture_with_default_values(self, user):
            expected = {
                'username': util.Any(str),
                'password': util.Any(str),
                'is_active': True,
            }
            actual = {
                'username': user.username,
                'password': user.password,
                'is_active': user.is_active,
            }
            assert expected == actual

    class CaseOverriddenValues:
        user__username = static_fixture('alfred')
        user__password = static_fixture('Myspace123')
        user__is_active = static_fixture(False)

        def it_creates_user_fixture_with_overridden_values(self, user):
            expected = {
                'username': 'alfred',
                'password': 'Myspace123',
                'is_active': False,
            }
            actual = {
                'username': user.username,
                'password': user.password,
                'is_active': user.is_active,
            }
            assert expected == actual

    class CaseParametrizedValues:
        @pytest.mark.parametrize(
            'user__username,user__password,user__is_active',
            [('alfred', 'Myspace123', False)],
        )
        def it_creates_user_fixture_with_parametrized_values(self, user):
            expected = {
                'username': 'alfred',
                'password': 'Myspace123',
                'is_active': False,
            }
            actual = {
                'username': user.username,
                'password': user.password,
                'is_active': user.is_active,
            }
            assert expected == actual
