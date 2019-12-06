from asyncio import create_task, get_running_loop
from enum import Enum, auto
from typing import AsyncIterator

from santa_factory.garage import Garage
from santa_factory.monitored import Monitor, Monitored


class Command(Enum):
    DELIVER = auto()


class Dashboard:
    def __init__(self, monitor: Monitor, garage: Garage):
        self._monitor = monitor
        self._garage = garage

    def monitor(self, monitored: Monitored):
        """Monitor something from the dashboard"""
        self._monitor.monitor(monitored)

    @staticmethod
    async def _command_stream() -> AsyncIterator[Command]:
        """Stream of user (Santa!) commands"""
        while True:
            await get_running_loop().run_in_executor(None, input)
            yield Command.DELIVER

    async def _handle_commands(self):
        """Handles user commands"""
        async for command in self._command_stream():
            if command == Command.DELIVER:
                await self._garage.deliver()

    def start(self):
        """Starts the dashboard"""
        create_task(self._handle_commands())
