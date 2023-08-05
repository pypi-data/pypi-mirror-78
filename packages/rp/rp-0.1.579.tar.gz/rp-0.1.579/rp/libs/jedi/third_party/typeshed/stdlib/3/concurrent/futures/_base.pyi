from typing import TypeVar, Generic, Any, Iterable, Iterator, Callable, Tuple, Optional, Set, NamedTuple
from types import TracebackType
import sys

FIRST_COMPLETED: str
FIRST_EXCEPTION: str
ALL_COMPLETED: str
PENDING: Any
RUNNING: Any
CANCELLED: Any
CANCELLED_AND_NOTIFIED: Any
FINISHED: Any
LOGGER: Any

class Error(Exception): ...
class CancelledError(Error): ...
class TimeoutError(Error): ...

_T = TypeVar('_T')

class Future(Generic[_T]):
    def __init__(self) -> None: ...
    def cancel(self) -> bool: ...
    def cancelled(self) -> bool: ...
    def running(self) -> bool: ...
    def done(self) -> bool: ...
    def add_done_callback(self, fn: Callable[[Future[_T]], Any]) -> None: ...
    def result(self, timeout: Optional[float] = ...) -> _T: ...
    def set_running_or_notify_cancel(self) -> bool: ...
    def set_result(self, result: _T) -> None: ...

    if sys.version_info >= (3,):
        def exception(self, timeout: Optional[float] = ...) -> Optional[BaseException]: ...
        def set_exception(self, exception: Optional[BaseException]) -> None: ...
    else:
        def exception(self, timeout: Optional[float] = ...) -> Any: ...
        def exception_info(self, timeout: Optional[float] = ...) -> Tuple[Any, Optional[TracebackType]]: ...
        def set_exception(self, exception: Any) -> None: ...
        def set_exception_info(self, exception: Any, traceback: Optional[TracebackType]) -> None: ...


class Executor:
    def submit(self, fn: Callable[..., _T], *args: Any, **kwargs: Any) -> Future[_T]: ...
    if sys.version_info >= (3, 5):
        def map(self, func: Callable[..., _T], *iterables: Iterable[Any], timeout: Optional[float] = ...,
                chunksize: int = ...) -> Iterator[_T]: ...
    else:
        def map(self, func: Callable[..., _T], *iterables: Iterable[Any], timeout: Optional[float] = ...,) -> Iterator[_T]: ...
    def shutdown(self, wait: bool = ...) -> None: ...
    def __enter__(self: _T) -> _T: ...
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool: ...

def as_completed(fs: Iterable[Future[_T]], timeout: Optional[float] = ...) -> Iterator[Future[_T]]: ...

def wait(fs: Iterable[Future[_T]], timeout: Optional[float] = ..., return_when: str = ...) -> Tuple[Set[Future[_T]],
                                                                                                    Set[Future[_T]]]: ...
