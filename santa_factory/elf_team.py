from asyncio import Queue, create_task
from typing import Iterable

from santa_factory.elf import Elf
from santa_factory.garage import Garage
from santa_factory.gift import Gift


class ElfTeam:
    def __init__(self, elves: Iterable[Elf]):
        self.elves = set(elves)
        self._idle_elves: Queue[Elf] = Queue()
        for elf in self.elves:
            self._idle_elves.put_nowait(elf)

    async def handle_gift(self, gift: Gift, garage: Garage):
        elf = await self._idle_elves.get()

        async def handle():
            await elf.handle_gift(gift, garage)
            await self._idle_elves.put(elf)

        create_task(handle())
