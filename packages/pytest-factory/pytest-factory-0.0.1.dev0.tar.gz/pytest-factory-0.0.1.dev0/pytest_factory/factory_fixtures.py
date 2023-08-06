import inspect
from functools import partial
from linecache import cache
from types import ModuleType
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Type, TYPE_CHECKING, Union

import factory
import factory.builder
import inflection
import pytest
from _pytest.compat import getfuncargnames
from _pytest.fixtures import FixtureRequest
from factory import Factory
from factory.declarations import BaseDeclaration

from .lazy_fixture import LazyFixture

if TYPE_CHECKING:
    from .plugin import PytestFactoryRequest

NOTSET = object()
FROM_ASSIGNMENT = object()

FACTORY_FIXTURE_MARK_ATTR = '_pytest_factory_fixture'


def factory_fixture(factory_cls: Type[Factory] = None, *,
                    name: Optional[str] = NOTSET,
                    factory_name: Optional[str] = NOTSET,
                    decls: Dict[str, Any] = None,
                    ):
    if factory_cls is None:
        return partial(factory_fixture, name=name, factory_name=factory_name)
    else:
        assert not factory_cls._meta.abstract, \
            'Cannot create factory fixtures from abstract factories'

        assert factory_cls._meta.model, \
            'Cannot create factory fixtures from factories without models'

        if name is NOTSET:
            name = extract_model_name(factory_cls)

        if factory_name is NOTSET and isinstance(name, str):
            factory_name = f'{name}_factory'

        if decls is None:
            decls = {}

        class NewFactoryFixture(factory_cls):
            _pytest_factory_model_name = name
            _pytest_factory_factory_name = factory_name
            _pytest_factory_model_fixture_defaults = decls
        NewFactoryFixture.__name__ = factory_cls.__name__

        if not issubclass(factory_cls, FactoryFixtureMixin):
            factory_cls.__bases__ += (FactoryFixtureMixin,)

        return NewFactoryFixture


def extract_model_name(factory_cls: Type[Factory]) -> str:
    """Determine the model name from a factory class

    The model name is snake_cased. This method prefers to extract the name from
    the factory class itself — i.e. "user" if the class is named "UserFactory".
    If the factory class is not in the format XyzFactory, the name will be taken
    from factory_cls.Meta.model.__name__ — i.e. the name of the model as declared
    in the Factory's Meta.model.

    >>> class UserFactory(Factory):
    ...     class Meta:
    ...         model = object
    ...
    >>> extract_model_name(UserFactory)
    'user'
    >>> class SuperUserFactory(UserFactory): pass
    >>> extract_model_name(SuperUserFactory)
    'super_user'
    >>> class WeirdName(Factory):
    ...     class Meta:
    ...         model = tuple
    ...
    >>> extract_model_name(WeirdName)
    'tuple'
    """
    factory_name = factory_cls.__name__
    if factory_name.endswith('Factory'):
        camel_name = factory_name[:-len('Factory')]
    else:
        model = factory_cls._meta.model
        camel_name = model.__name__

    return inflection.underscore(camel_name)


def is_factory_fixture(obj) -> bool:
    """Return whether an object is a factory fixture
    """
    return inspect.isclass(obj) and issubclass(obj, FactoryFixtureMixin)


def wrap_factory_class(request, factory_cls) -> Type[Factory]:
    Params = getattr(factory_cls, 'Params', None)
    params_bases = (Params,) if Params else ()

    class FactoryClass(factory_cls):
        # Expose pytest request to simplify LazyFixture resolution
        class Params(*params_bases):
            pytest_request = request

    FactoryClass.__name__ = factory_cls.__name__
    return FactoryClass


def get_model_fixture_name(factory_cls: Type['FactoryFixtureMixin']) -> str:
    return factory_cls._pytest_factory_model_name


class FactoryFixtureMixin:
    _pytest_factory_fixture = True
    _pytest_factory_model_name = None
    _pytest_factory_factory_name = None
    _pytest_factory_model_attr_sep = '__'
    _pytest_factory_model_fixture_defaults = None

    @classmethod
    def as_fixture(cls, with_factory: Union[str, bool] = True, **decls):
        if with_factory is True:
            factory_name = NOTSET
        elif isinstance(with_factory, str):
            factory_name = with_factory
        else:
            factory_name = False

        return factory_fixture(cls, name=FROM_ASSIGNMENT, factory_name=factory_name, decls=decls)

    @classmethod
    def _pytest_factory_contribute_to_parent(cls, parent: Union[type, ModuleType], name: str):
        """Setup the factory_fixture for the given class/module

        This method is called during collection, when a @factory_fixture-decorated
        Factory class is encountered in a module or class. This method is responsible
        for creating any model/factory fixtures and setting them as attributes on
        the parent
        """
        if cls._pytest_factory_model_name is FROM_ASSIGNMENT:
            cls._pytest_factory_model_name = name

            if cls._pytest_factory_factory_name is NOTSET:
                cls._pytest_factory_factory_name = f'{name}_factory'

        cls._pytest_factory_contribute_factory_fixture(parent)
        cls._pytest_factory_contribute_model_fixtures(parent)

    @classmethod
    def _pytest_factory_contribute_fixture(
        cls, parent: Union[type, ModuleType], name: str, fixture_impl: Callable
    ):
        is_in_class = isinstance(parent, type)

        if is_in_class:
            fixture_impl = with_self(fixture_impl)

        fixture_impl = pytest.fixture(fixture_impl)
        fixture_impl.__name__ = name
        fixture_impl.__module__ = parent.__module__ if is_in_class else parent.__name__
        setattr(parent, fixture_impl.__name__, fixture_impl)

    @classmethod
    def _pytest_factory_contribute_factory_fixture(cls, parent: Union[type, ModuleType]) -> None:
        ###
        # Users may forego the creation of a factory class fixture by passing
        # factory_name=None to @factory_fixture
        #
        if cls._pytest_factory_factory_name is None:
            return

        def factory_fixture(request):
            return wrap_factory_class(request, cls)

        cls._pytest_factory_contribute_fixture(
            parent, cls._pytest_factory_factory_name, factory_fixture)

    @classmethod
    def _pytest_factory_get_model_fixture_deps(
        cls, parent_factory_cls: Type['FactoryFixtureMixin'] = None
    ) -> Dict[str, Any]:
        """Return the fixture names (and their decls) our model fixture depends on

        :param parent_factory_cls:
            If passed, this method will omit SubFactory declarations corresponding
            to parent_factory_cls.

        """

        def is_dep(value: Union[Any, BaseDeclaration]) -> bool:
            if isinstance(value, factory.RelatedFactory):
                return False

            elif isinstance(value, factory.SubFactory):
                if issubclass(value.get_factory(), parent_factory_cls):
                    return False

            else:
                return True

        model_name = cls._pytest_factory_model_name
        sep = cls._pytest_factory_model_attr_sep
        return {
            sep.join((model_name, attr)): value
            for attr, value in cls._meta.declarations.items()
            if is_dep(value)
        }

    @classmethod
    def _pytest_factory_contribute_model_fixtures(cls, parent: Union[type, ModuleType]) -> None:
        model_name = cls._pytest_factory_model_name
        fixtures: Dict[str, Callable] = {}
        model_fixture_deps = []
        model_fixture_args = {}

        for attr, value in cls._meta.declarations.items():
            attr_fixture_deps = []
            attr_name = cls._pytest_factory_model_attr_sep.join((model_name, attr))
            fixture_impl = None

            # TODO: postgen

            if isinstance(value, (factory.SubFactory, factory.RelatedFactory)):
                subfactory_class: Type[FactoryFixtureMixin] = value.get_factory()
                # TODO: case where subfactory is not @factory_fixture
                subfactory_deps = subfactory_class._pytest_factory_get_model_fixture_deps(
                    parent_factory_cls=cls)
                subfactory_model_name = subfactory_class._pytest_factory_model_name

                attr_fixture_deps = [
                    *subfactory_deps,
                    subfactory_model_name,
                ]

                if isinstance(value, factory.RelatedFactory):
                    model_fixture_deps += [
                        subfactory_model_name,
                        attr_name,
                        *subfactory_deps,
                    ]

                argnames = {
                    dep: '_subfactory_model_value' if dep == subfactory_model_name else None
                    for dep in attr_fixture_deps
                }

                fixture_impl = build_wrapped_method(
                    name=attr_name,
                    argnames=list(argnames.items()),
                    impl=lambda _subfactory_model_value: _subfactory_model_value,
                )

            else:
                default = None if isinstance(value, factory.declarations.PostGenerationDeclaration) else value
                value = cls._pytest_factory_model_fixture_defaults.get(attr, default)

                if isinstance(value, LazyFixture):
                    attr_fixture_deps = value.requested_fixtures

                fixture_impl = build_wrapped_method(
                    name=attr_name,
                    argnames=[(dep, None) for dep in attr_fixture_deps],
                    impl=lambda value: value,
                    value=value,
                )

            fixtures[attr_name] = fixture_impl
            model_fixture_args[attr_name] = attr

        model_fixture = cls._pytest_factory_model_fixture_impl
        argnames = [
            'request',
            'factory_request',
            *model_fixture_args.items()
        ]

        ###
        # If the user prefers not to expose the factory as a fixture, we must
        # craft one in the model fixture.
        #
        if cls._pytest_factory_factory_name is None:
            model_fixture_impl = model_fixture

            def model_fixture(request, factory_request, **decls):
                factory_cls = wrap_factory_class(request, cls)
                return model_fixture_impl(request, factory_request, factory_cls, **decls)

        ###
        # Otherwise, we will use the factory class from the factory fixture,
        # allowing the user to override the factory, if so desired.
        #
        else:
            argnames.append((cls._pytest_factory_factory_name, 'factory_cls'))

        model_fixture = build_wrapped_method(
            name=model_name,
            argnames=argnames,
            impl=model_fixture,
        )
        fixtures[model_name] = model_fixture

        for name, fixture in fixtures.items():
            cls._pytest_factory_contribute_fixture(parent, name, fixture)

    @staticmethod
    def _pytest_factory_model_fixture_impl(
        request: FixtureRequest,
        factory_request: 'PytestFactoryRequest',
        factory_cls: Type[Union[Factory, 'FactoryFixtureMixin']],
        **decls,
    ):
        class ModelFactory(factory_cls):
            """New subclass of the factory, so we may modify its declarations"""

        # Remove all the postgen declarations, as we'll handle them separately later
        ModelFactory._meta.base_declarations = {
            name: decl
            for name, decl in ModelFactory._meta.base_declarations.items()
            if not isinstance(decl, factory.declarations.PostGenerationDeclaration)
        }
        ModelFactory._meta.post_declarations = factory.builder.DeclarationSet()

        # Only pass along the non-postgen declarations to the factory
        kwargs = {
            name: decl
            for name, decl in decls.items()
            if name in factory_cls._meta.pre_declarations
        }

        strategy = ModelFactory._meta.strategy
        builder = factory.builder.StepBuilder(ModelFactory._meta, kwargs, strategy)
        step = factory.builder.BuildStep(builder=builder,
                                         sequence=ModelFactory._meta.next_sequence())

        instance = ModelFactory(**kwargs)

        deferred = []
        post_declarations = factory_cls._meta.post_declarations
        for attr in post_declarations.sorted():
            decl = post_declarations.declarations[attr]

            if isinstance(decl, factory.RelatedFactory):
                # TODO
                raise NotImplementedError('TODO')
            else:
                extra = {}
                for k, v in post_declarations.contexts[attr].items():
                    if k == '':
                        continue
                    extra[k] = decls[k] if k in decls else v

                postgen_context = factory.builder.PostGenerationContext(
                    value_provided=True,
                    value=decls[attr],
                    extra=extra,
                )
                deferred.append(
                    partial(decl.call, instance, step, postgen_context)
                )

        factory_request.defer(deferred)
        return instance


_WRAPPED_FIXTURE_FORMAT = '''
def {name}({argnames}):
    return {impl_name}({kwargs})
'''


def build_wrapped_method(
    name: str,
    argnames: Iterable[Union[str, Tuple[str, Optional[str]]]],
    impl: Callable, *,
    with_self: bool = False,
    **extra_kwargs
) -> Callable:
    impl_name = '___extension_impl'
    argnames = tuple(
        t if isinstance(t, tuple) else (t, t)
        for t in argnames
    )

    declared_argnames = tuple(
        t[0]
        for t in argnames
    )
    if with_self:
        declared_argnames = ('self',) + declared_argnames

    kwargs = ', '.join(
        f'{kwarg}={arg}'
        for arg, kwarg in argnames
        if kwarg is not None
    )
    if kwargs:
        kwargs += ', '
    kwargs += '**___extra_kwargs'

    source = _WRAPPED_FIXTURE_FORMAT.format(
        name=name,
        argnames=', '.join(declared_argnames),
        kwargs=kwargs,
        impl_name=impl_name,
    )
    context = {
        impl_name: impl,
        '___extra_kwargs': extra_kwargs,
    }
    path = f'{__file__}::{name}'
    co = compile(source, path, 'exec', dont_inherit=True)
    exec(co, context)
    wrapped_method = context[name]

    # Seed the line cache, so tracebacks can show source code
    def getsource():
        return source
    cache[path] = (getsource,)

    return wrapped_method


def with_self(fn: Callable) -> Callable:
    """Add 'self' as the first arg to fn, retaining signature
    """
    return build_wrapped_method(
        name=fn.__name__,
        argnames=getfuncargnames(fn),
        impl=fn,
        with_self=True,
    )
