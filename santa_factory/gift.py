from dataclasses import dataclass
from random import randrange
from typing import NewType

from santa_factory.types import Time, Weight


@dataclass
class Gift:
    weight: Weight
    packing_time: Time
    delivering_time: Time


PackedGift = NewType("PackedGift", Gift)


class GiftFactory:
    def __aiter__(self):
        return self

    async def __anext__(self) -> Gift:
        """Endlessly makes gift (magic!)"""
        weight = Weight(randrange(1, 4))
        gift = Gift(weight, Time(weight * 2.0), Time(0.1))
        return gift
