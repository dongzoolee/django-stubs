from collections.abc import Callable, Sequence
from functools import wraps as wraps  # noqa: F401
from typing import Any, Generic, Protocol, TypeVar, overload

from _typeshed import Self
from django.db.models.base import Model
from typing_extensions import SupportsIndex, TypeAlias

_T = TypeVar("_T")

class cached_property(Generic[_T]):
    func: Callable[..., _T]
    name: str
    def __init__(self, func: Callable[..., _T], name: str = ...) -> None: ...
    @overload
    def __get__(self: Self, instance: None, cls: type[Any] = ...) -> Self: ...
    @overload
    def __get__(self, instance: object, cls: type[Any] = ...) -> _T: ...

# Promise is only subclassed by a proxy class defined in the lazy function
# so it makes sense for it to have all the methods available in that proxy class
class Promise:
    def __init__(self, args: Any, kw: Any) -> None: ...
    def __reduce__(self) -> tuple[Any, tuple[Any]]: ...
    def __lt__(self, other: Any) -> bool: ...
    def __mod__(self, rhs: Any) -> Any: ...
    def __add__(self, other: Any) -> Any: ...
    def __radd__(self, other: Any) -> Any: ...
    def __deepcopy__(self: Self, memo: Any) -> Self: ...

class _StrPromise(Promise, Sequence[str]):
    def __add__(self, __s: str) -> str: ...
    # Incompatible with Sequence.__contains__
    def __contains__(self, __o: str) -> bool: ...  # type: ignore[override]
    def __ge__(self, __x: str) -> bool: ...
    def __getitem__(self, __i: SupportsIndex | slice) -> str: ...
    def __gt__(self, __x: str) -> bool: ...
    def __le__(self, __x: str) -> bool: ...
    # __len__ needed here because it defined abstract in Sequence[str]
    def __len__(self) -> int: ...
    def __lt__(self, __x: str) -> bool: ...
    def __mod__(self, __x: Any) -> str: ...
    def __mul__(self, __n: SupportsIndex) -> str: ...
    def __rmul__(self, __n: SupportsIndex) -> str: ...
    # Mypy requires this for the attribute hook to take effect
    def __getattribute__(self, __name: str) -> Any: ...

StrOrPromise: TypeAlias = str | _StrPromise  # noqa: Y047
_C = TypeVar("_C", bound=Callable)

def lazy(func: _C, *resultclasses: Any) -> _C: ...
def lazystr(text: Any) -> _StrPromise: ...
def keep_lazy(*resultclasses: Any) -> Callable: ...
def keep_lazy_text(func: Callable) -> Callable: ...

empty: object

def new_method_proxy(func: Callable[..., _T]) -> Callable[..., _T]: ...

class LazyObject:
    def __init__(self) -> None: ...
    __getattr__: Callable
    def __setattr__(self, name: str, value: Any) -> None: ...
    def __delattr__(self, name: str) -> None: ...
    def __reduce__(self) -> tuple[Callable, tuple[Model]]: ...
    def __copy__(self) -> LazyObject: ...
    __bytes__: Callable
    __bool__: Callable
    __dir__: Callable
    __ne__: Callable
    __hash__: Callable
    __getitem__: Callable
    __setitem__: Callable
    __delitem__: Callable
    __iter__: Callable
    __len__: Callable
    __contains__: Callable

def unpickle_lazyobject(wrapped: Model) -> Model: ...

class SimpleLazyObject(LazyObject):
    def __init__(self, func: Callable[[], Any]) -> None: ...
    def __copy__(self) -> SimpleLazyObject: ...

_PartitionMember = TypeVar("_PartitionMember")

def partition(
    predicate: Callable[[_PartitionMember], int | bool], values: list[_PartitionMember]
) -> tuple[list[_PartitionMember], list[_PartitionMember]]: ...

_Get = TypeVar("_Get", covariant=True)

class classproperty(Generic[_Get]):
    fget: Callable[[Any], _Get] | None
    def __init__(self, method: Callable[[Any], _Get] | None = ...) -> None: ...
    def __get__(self, instance: Any | None, cls: type[Any] = ...) -> _Get: ...
    def getter(self, method: Callable[[Any], _Get]) -> classproperty[_Get]: ...

class _Getter(Protocol[_Get]):
    """Type fake to declare some read-only properties (until `property` builtin is generic)

    We can use something like `Union[_Getter[str], str]` in base class to avoid errors
    when redefining attribute with property or property with attribute.
    """

    @overload
    def __get__(self: Self, __instance: None, __typeobj: type[Any] | None) -> Self: ...
    @overload
    def __get__(self, __instance: Any, __typeobj: type[Any] | None) -> _Get: ...
