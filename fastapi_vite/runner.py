
# Standard Library
import asyncio
import logging
from asyncio.futures import Future
from asyncio.streams import StreamReader
from asyncio.subprocess import Process
from typing import Any, ClassVar, Coroutine, Dict, Optional, Set
from urllib.parse import urljoin
import anyio

# Third Party Libraries
from jinja2 import Markup
from pydantic import BaseSettings, validator


class ViteRunner(object):
    """Vite client utility.

    Utility class for handling Redis database connection and operations.

    Attributes:
        redis_client (aioredis.Redis, optional): Redis client object instance.
        log (logging.Logger): Logging handler for this class.

    """

    _instance: Optional["ViteRunner"] = None
    process: ClassVar[Optional[Coroutine[Any, Any, Process]]] = None
    logger: logging.Logger = logging.getLogger(__name__)
    future: ClassVar[Optional[Future]] = None
    tasks: ClassVar[Set[Coroutine]] = ()

    def __new__(cls):
        """Singleton loader"""
        if cls._instance is not None:
            return cls._instance

        cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    async def start(cls):
        """
        Create Vite client session object instance.

        Returns:
            Future

        """
        cls.process = await anyio.open_process("npm run dev")
        # cls.process = await asyncio.create_subprocess_shell(
        #     "npm run dev",
        #     stdout=asyncio.subprocess.PIPE,
        #     stderr=asyncio.subprocess.PIPE,
        #     restore_signals=True,
        # )
        cls.logger.info("⚡ Starting Vite Asset Service for Live Reload functionality")

        cls.future = asyncio.ensure_future(
            asyncio.gather(
                cls.process.wait(),
                cls._read_from_stdout(stream=cls.process.stdout),
                cls._read_from_stderr(stream=cls.process.stderr),
            ),
        )

        return cls

    @classmethod
    async def stop(cls):
        """Close Redis client."""
        # cls.log.debug("Stopping ViteJS Development Server")
        cls.logger.info("⚡ Stopping Vite Asset Service")

        if cls.process:
            try:
                cls.process.terminate()
            except OSError:
                # Ignore 'no such process' error
                cls.logger.debug(
                    "...Process previously terminated. Skipping cleanup.",
                )

    @classmethod
    async def build(cls):
        """
        Create Vite client session object instance.

        Returns:
            Future

        """
        cls.process = await asyncio.create_subprocess_shell(
            "npm run build",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            restore_signals=True,
        )
        cls.logger.info("⚡ Vite is building application assets")

        cls.future = await asyncio.gather(
            await cls.process.wait(),
            cls._read_from_stdout(stream=cls.process.stdout),
            cls._read_from_stderr(stream=cls.process.stderr),
        )
        return cls

    @classmethod
    async def _read_from_stdout(cls, stream: StreamReader):
        while chunk := await stream.readline():
            cls.logger.debug(f"{chunk.decode('utf-8').strip()}")

    @staticmethod
    async def _read_from_stderr(cls, stream: StreamReader):
        while chunk := await stream.readline():
            cls.logger.error(f"{chunk.decode('utf-8').strip()}")