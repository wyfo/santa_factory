import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator

from santa_factory.garage import Garage
from santa_factory.gift import Gift, PackedGift
from santa_factory.monitored import Monitored
from santa_factory.sledge import Sledge
from santa_factory.types import Weight


class Elf(Monitored):
    @asynccontextmanager
    async def sledge_can_be_loaded(self, weight: Weight, garage: Garage
                                   ) -> AsyncIterator[Sledge]:
        """Checks the sledge waiting in the garage"""
        while True:
            async with garage.use_sledge() as sledge:
                if sledge.can_load(weight):
                    yield sledge
                    break
                else:
                    self._do(f"gift is too heavy for {sledge}")
            await garage.wait_new_sledge()

    async def pack(self, gift: Gift) -> PackedGift:
        """Packs a gift"""
        with self._do_long(f"packing {gift}"):
            await asyncio.sleep(gift.packing_time)
            return PackedGift(gift)

    def load(self, packed_gift: PackedGift, sledge: Sledge):
        """Loads a packed gift in a sledge"""
        self._do(f"loading {packed_gift} to {sledge}")
        sledge.load(packed_gift)

    async def handle_gift(self, gift: Gift, garage: Garage):
        """Packs and loads a gift into a sledge of the garage"""
        async with self.sledge_can_be_loaded(gift.weight, garage):
            pass  # checks the sledge before packing the gift
        packed_gift = await self.pack(gift)
        async with self.sledge_can_be_loaded(gift.weight, garage) as sledge:
            self.load(packed_gift, sledge)
