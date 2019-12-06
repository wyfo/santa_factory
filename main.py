from asyncio import run

from santa_factory.dashboard import Dashboard
from santa_factory.elf import Elf
from santa_factory.garage import Garage
from santa_factory.gift import GiftFactory
from santa_factory.monitored import Monitor
from santa_factory.named import named
from santa_factory.santa_factory import SantaFactory
from santa_factory.sledge import Sledge
from santa_factory.types import Time, Weight


async def main():
    sledge = named(Sledge(Weight(100), Time(0)), "Sledge")
    garage = Garage(sledge)
    dashboard = Dashboard(Monitor(), garage)
    elves = (named(Elf(), f"Elf{i}") for i in range(5))
    factory = SantaFactory(GiftFactory(), elves, garage, dashboard)
    await factory.run()


if __name__ == '__main__':
    run(main())
