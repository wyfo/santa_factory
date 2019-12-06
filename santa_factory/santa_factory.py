from typing import Iterable

from santa_factory.dashboard import Dashboard
from santa_factory.elf import Elf
from santa_factory.elf_team import ElfTeam
from santa_factory.garage import Garage
from santa_factory.gift import GiftFactory


class SantaFactory:
    def __init__(self, gift_factory: GiftFactory, elves: Iterable[Elf],
                 garage: Garage, dashboard: Dashboard):
        self.gift_factory = gift_factory
        self.garage = garage
        self.dashboard = dashboard
        self.elf_team = ElfTeam(elves)
        # Monitoring
        for elf in self.elf_team.elves:
            self.dashboard.monitor(elf)
        for sledge in self.garage.sledges:
            self.dashboard.monitor(sledge)

    async def run(self):
        """Brings to life this little world"""
        self.dashboard.start()
        async for gift in self.gift_factory:
            await self.elf_team.handle_gift(gift, self.garage)
