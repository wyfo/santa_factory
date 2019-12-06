from asyncio import Event, Lock
from contextlib import asynccontextmanager
from typing import AsyncIterator, Iterable

from santa_factory.sledge import ReindeerHungry, Sledge, SledgeEmpty


class Garage:
    def __init__(self, sledge: Sledge):
        self._sledge = sledge
        self._lock = Lock()
        self._new_sledge = Event()

    @property
    def sledges(self) -> Iterable[Sledge]:
        """All sledges of the garage"""
        yield self._sledge

    async def wait_new_sledge(self):
        """Wait for a "new" sledge coming back from delivery"""
        await self._new_sledge.wait()

    @asynccontextmanager
    async def use_sledge(self) -> AsyncIterator[Sledge]:
        """Use a sledge of the garage"""
        async with self._lock:
            yield self._sledge

    async def deliver(self):
        """Send a sledge in delivery"""
        async with self.use_sledge() as sledge:
            try:
                await sledge.deliver()
                self._new_sledge.set()
                self._new_sledge.clear()
            except (ReindeerHungry, SledgeEmpty):
                pass
