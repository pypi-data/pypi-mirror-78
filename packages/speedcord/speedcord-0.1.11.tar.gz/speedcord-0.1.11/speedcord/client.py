"""
Created by Epic at 9/1/20
"""
import asyncio
import logging
from aiohttp import ClientWebSocketResponse, WSMessage, WSMsgType

from . import exceptions, packets, wsratelimits
from .http import HttpClient, Route
from .dispatcher import OpcodeDispatcher, EventDispatcher
from .gateway import DefaultGatewayHandler
from .shard import DefaultShard

__all__ = ("Client",)


class Client:
    def __init__(self, intents: int, token=None, *, use_mobile_status=False, shard_count: int = None):
        # Configurable stuff
        self.intents = int(intents)
        self.token = token
        self.use_mobile_status = use_mobile_status

        # Things used by the lib, usually doesn't need to get changed but can if you want to.
        self.shard_count: int = shard_count
        self.shards = []
        self.loop = asyncio.get_event_loop()
        self.logger = logging.getLogger("speedcord")
        self.http: HttpClient = None
        self.opcode_dispatcher = OpcodeDispatcher(self.loop)
        self.event_dispatcher = EventDispatcher(self.loop)
        self.gateway_handler = DefaultGatewayHandler(self)
        self.connected = asyncio.Event()
        self.heartbeat_interval = None
        self.heartbeat_count = None
        self.received_heartbeat_ack = True
        self.error_exit_event = asyncio.Event(loop=self.loop)

        # Default event handlers
        self.opcode_dispatcher.register(0, self.handle_dispatch)

    def run(self):
        try:
            self.loop.run_until_complete(self.start())
        except KeyboardInterrupt:
            self.loop.run_until_complete(self.close())

    async def get_gateway(self):
        route = Route("GET", "/gateway/bot")
        try:
            r = await self.http.request(route)
        except exceptions.Unauthorized:
            await self.close()
            raise
        data = await r.json()

        shards = data["shards"]
        remaining_connections = data["session_start_limit"]["remaining"]
        connections_reset_after = data["session_start_limit"]["reset_after"]
        gateway_url = data["url"]

        if remaining_connections == 0:
            raise exceptions.ConnectionsExceeded

        self.logger.debug(f"{remaining_connections} gateway connections left!")

        return gateway_url, shards, remaining_connections, connections_reset_after

    async def connect(self):
        if self.token is None:
            raise exceptions.InvalidToken

        try:
            gateway_url, shard_count, remaining_connections, connections_reset_after = await self.get_gateway()
        except exceptions.Unauthorized:
            self.error_exit_event.clear()
            raise exceptions.InvalidToken

        if self.shard_count is None or self.shard_count < shard_count:
            self.shard_count = shard_count

        for shard_id in range(self.shard_count):
            shard = DefaultShard(shard_id, self, loop=self.loop)
            await shard.connect(gateway_url)
            self.shards.append(shard)
            remaining_connections -= 1
            if remaining_connections == 0:
                self.logger.info("Max connections reached!")
                await asyncio.sleep(connections_reset_after / 1000)
                gateway_url, shard_count, remaining_connections, connections_reset_after = await self.get_gateway()
        self.logger.info("All shards connected!")

    async def start(self):
        if self.token is None:
            raise exceptions.InvalidToken
        self.http = HttpClient(self.token, loop=self.loop)

        await self.connect()

        await self.error_exit_event.wait()
        await self.close()

    async def close(self):
        await self.http.close()
        for shard in self.shards:
            await shard.close()

    # Handle events
    async def handle_dispatch(self, data, shard):
        self.event_dispatcher.dispatch(data["t"], data["d"], shard)
