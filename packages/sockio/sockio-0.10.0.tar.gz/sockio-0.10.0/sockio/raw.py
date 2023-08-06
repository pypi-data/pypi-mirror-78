import socket
import asyncio
import logging
import functools

from .aio import IPTOS_LOWDELAY, ConnectionTimeoutError

log = logging.getLogger("sockio.raw")


def _loop(loop):
    return loop or asyncio.get_event_loop()


async def _connect(sock, address, loop=None):
    return await _loop(loop).sock_connect(sock, address)


async def create_connection(
        host,
        port,
        no_delay=True,
        tos=IPTOS_LOWDELAY,
        keep_alive=None,
        loop=None
):
    sock = socket.socket()
    sock.setblocking(False)
    if hasattr(socket, "TCP_NODELAY") and no_delay:
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    if hasattr(socket, "IP_TOS"):
        sock.setsockopt(socket.SOL_IP, socket.IP_TOS, tos)
    if keep_alive is not None and hasattr(socket, "SO_KEEPALIVE"):
        if isinstance(keep_alive, (int, bool)):
            keep_alive = 1 if keep_alive in {1, True} else False
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, keep_alive)
        else:
            active = keep_alive.get('active')
            idle = keep_alive.get('idle')  # aka keepalive_time
            interval = keep_alive.get('interval')  # aka keepalive_intvl
            retry = keep_alive.get('retry')  # aka keepalive_probes
            if active is not None:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, active)
            if idle is not None:
                sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPIDLE, idle)
            if interval is not None:
                sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPINTVL, interval)
            if retry is not None:
                sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPCNT, retry)

    await _connect(sock, (host, port), loop=loop)
    return sock


def ensure_connection(f):
    assert asyncio.iscoroutinefunction(f)
    name = f.__name__

    @functools.wraps(f)
    async def wrapper(self, *args, **kwargs):
        if self.auto_reconnect and not self.connected():
            await self.open()
        timeout = kwargs.pop("timeout", self.timeout)
        coro = f(self, *args, **kwargs)
        if timeout is not None:
            coro = asyncio.wait_for(coro, timeout)
        try:
            return await coro
        except asyncio.TimeoutError as error:
            msg = "{} call timeout on '{}:{}'".format(name, self.host, self.port)
            raise ConnectionTimeoutError(msg) from error

    return wrapper


class TCP:

    def __init__(
        self,
        host: str,
        port: int,
        eol: bytes = b"\n",
        auto_reconnect: bool = True,
        no_delay:bool = True,
        tos=IPTOS_LOWDELAY,
        keep_alive=None,
        connection_timeout=None,
        timeout=None,
        loop=None
    ):
        self.host = host
        self.port = port
        self.eol = eol
        self.auto_reconnect = auto_reconnect
        self.no_delay = no_delay
        self.tos = tos
        self.keep_alive = keep_alive
        self.connection_timeout = connection_timeout
        self.timeout = timeout
        self.loop = _loop(loop)
        self._sock = None
        self._log = log.getChild("TCP({}:{})".format(host, port))

    def connected(self):
        return self._sock is not None

    is_open = property(connected)

    async def open(self, **kwargs):
        connection_timeout = kwargs.get("timeout", self.connection_timeout)
        if self.connected():
            raise ConnectionError("socket already open")
        coro = create_connection(
            self.host,
            self.port,
            no_delay=self.no_delay,
            tos=self.tos,
            keep_alive=self.keep_alive,
            loop=self.loop
        )
        if connection_timeout is not None:
            coro = asyncio.wait_for(coro, connection_timeout)
        try:
            self._sock = await coro
        except asyncio.TimeoutError:
            addr = self.host, self.port
            raise ConnectionTimeoutError("Connect call timeout on {}".format(addr))

    def close(self):
        if self._sock:
            self._sock.close()
            self._sock = None

    async def _write(self, data):
        return await self.loop.sock_sendall(self._sock, data)

    async def _read(self, n):
        return await self.loop.sock_recv(self._sock, n)

    @ensure_connection
    async def write_read(self, data, n):
        await self._write(data)
        return await self._read(n)
