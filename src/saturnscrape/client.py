"""Client for SaturnScrape - Scrape schedule data from https://saturn.live to use in your own applications.

Copyright (C) 2023  Parker Wahle

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""  # noqa: E501, B950
from __future__ import annotations

from functools import wraps
from typing import Callable
from typing import ParamSpec
from typing import Self
from typing import TypeVar

from httpx import AsyncClient as AsyncHTTPXClient
from httpx import Client as SyncHTTPXClient


P = ParamSpec("P")
R = TypeVar("R")


class SyncSaturnClient:
    """Interact with the Saturn API synchronously using HTTPX."""

    @staticmethod
    def _require_started(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(self: Self, *args: P.args, **kwargs: P.kwargs) -> R:
            if not self._started:
                raise RuntimeError(f"Client must be started before {func.__name__} can be called.")
            if self._closed:
                raise RuntimeError(f"Client has been closed and cannot be used. A new client must be created.")
            return func(self, *args, **kwargs)

        return wrapper

    def __init__(self) -> None:
        self._started = False
        self._closed = False
        self._client: SyncHTTPXClient | None = None

    def startup(self) -> None:
        """Prepares the client for connections. This method must be called before the client can be used."""
        if self._started:
            raise RuntimeError("Client has already been started.")
        if self._closed:
            raise RuntimeError("Client has been closed and cannot be used. A new client must be created.")
        self._client = SyncHTTPXClient()
        self._started = True

    def close(self) -> None:
        """Shuts down the client and closes all connections. The client cannot be used after this method is called."""
        if not self._started:
            raise RuntimeError("Client has not been started.")
        if self._closed:
            raise RuntimeError("Client has already been closed.")
        self._client.close()
        self._closed = True

    def __enter__(self) -> Self:
        self.startup()
        return self

    def __exit__(self, exc_type: type[BaseException], exc_value: BaseException, traceback: type[BaseException]) -> None:
        self.close()

    # API methods

    @_require_started
    def login(
        self,
        username: str,
        password: str,
    ) -> bool:
        """Login to Saturn and generate credentials from a pair of username and password."""
        pass


class AsyncSaturnClient:
    """Interact with the Saturn API asynchronously using HTTPX."""

    pass


__all__ = ("SyncSaturnClient", "AsyncSaturnClient")
