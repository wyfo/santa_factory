import asyncio
from random import randrange
from typing import List

from santa_factory.gift import PackedGift
from santa_factory.monitored import Monitored
from santa_factory.types import Time, Weight


class ReindeerHungry(Exception):
    """Stop animal abuses"""
    pass


class SledgeEmpty(Exception):
    """Why would you send an empty sledge in delivery?"""
    pass


class Sledge(Monitored):
    def __init__(self, max_weight: Weight, fixed_delivery_time: Time):
        super().__init__()
        self.max_weight: Weight = max_weight
        self.gifts: List[PackedGift] = []
        self.fixed_delivery_time = fixed_delivery_time

    @property
    def cur_weight(self) -> Weight:
        return Weight(sum(g.weight for g in self.gifts))

    @property
    def empty(self) -> bool:
        return not self.gifts

    def can_load(self, weight: Weight):
        """If the sledge can accept more weight"""
        return self.cur_weight + weight <= self.max_weight

    def load(self, gift: PackedGift):
        """Loads a packed gift"""
        assert self.can_load(gift.weight)
        self.gifts.append(gift)
        self._do(f"{gift} loaded; {self.cur_weight}/{self.max_weight}kg")

    @property
    def _hungry(self) -> bool:
        """Are the reindeers hungry?"""
        return randrange(0, 5) == 0

    async def deliver(self):
        """The sledge leaves the north pole to deliver the gifts
           and comes back empty"""
        if self.empty:
            self._do("empty!")
            raise SledgeEmpty()
        if self._hungry:
            self._do("hungry! muuuuh...")
            raise ReindeerHungry()
        with self._do_long("delivering gifts"):
            await asyncio.sleep(self.fixed_delivery_time +
                                sum(g.delivering_time for g in self.gifts))
            self.gifts = []
