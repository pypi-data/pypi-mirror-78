"""
Main score worker class implementation
"""
import asyncio
import json
import logging
import tempfile

import aiofiles
import aioredis
from yarl import URL

from .errors import AudioUndecodableException
from .worker import Worker

logger = logging.getLogger("aiokafkadaemon.AdvancedWorker")


class AdvancedWorker(Worker):
    """
    Worker class runs the main worker for the scoring service
    """

    def __init__(self, testing=False, score_model=None, kafka_opts={}, redis_opts={}):
        """
        Lowering max_poll_interval_ms from 300s to 60s to be more responsive
        to rebalance error, reduce the impact of user timeouts
        Keep default auto_commit (5000ms) but list here for further tuning
        """
        super().__init__(
            kafka_broker_addr=kafka_opts.get("broker"),
            kafka_group_id=kafka_opts.get("group_id"),
            consumer_topic=kafka_opts.get("topic"),
            create_consumer=False if testing else True,
            create_producer=False if testing else True,
            sasl_opts=kafka_opts.get("sasl_opts"),
            consumer_opts={
                "max_poll_interval_ms": 60000,
                "auto_commit_interval_ms": 5000,
            },
        )
        self._testing = testing
        self._audio_path = tempfile.mkdtemp()
        self._score_model = score_model
        self._versions = AdvancedWorker.get_worker_version()

        self._redis_opts = redis_opts
        self._redis = None
        self._redis_retry = 0
        self._redis_reconnecting = False

    async def create_redis(self):
        """
        Keep retrying until succeed every 5 * retry seconds, max 1 minute interval
        """
        self._redis_reconnecting = True
        while True:
            try:
                if self._redis_opts:
                    self._redis = await aioredis.create_redis_pool(
                        self._redis_opts["url"], timeout=5
                    )

                logger.warning("Redis connected")
                break
            except Exception as e:
                # failed to create, just retry
                logger.error(e)
            self._redis_retry += 1
            await asyncio.sleep(min(60, 5 * self._redis_retry))
            logger.warning(f"Retry connecting redis {self._redis_retry}")

        # reset counters and flags after connection
        self._redis_retry = 0
        self._redis_reconnecting = False

    async def destroy_redis(self):
        """
        Don't care if the close fails or timeout
        """
        if self._redis is not None and not self._redis_reconnecting:
            try:
                self._redis.close()
                await asyncio.wait_for(self._redis.wait_closed(), timeout=3)
            except Exception as e:
                logger.error(e)
            finally:
                self._redis = None
                logger.warning("Redis destoryed")

    async def start(self):
        """
        Add additional start logic for redis
        start redis before others, blocks Kafka if redis is required but fails
        this will block the worker from accepting loads
        """
        await self.create_redis()
        await super().start()

    async def clean_up_after_run(self):
        """
        Add additional stop logic for redis
        """
        await super().clean_up_after_run()
        await self.destroy_redis()

    @staticmethod
    def get_worker_version():
        """
        Parses worker metadada and returns it
        :return:
        """
        metadata = None
        try:
            with open("metadata.json", "r") as f:
                data = f.read()
                metadata = json.loads(data)
        except Exception:
            logger.error("metadata does not exist")

        return metadata

    @staticmethod
    def is_binary_audio(audio):
        try:
            # Let's try forcing decode here to check it's ok
            if str(audio, "utf-8"):
                audio = None
        except UnicodeDecodeError:
            # This is ok
            pass
        return audio

    @staticmethod
    async def read_local(path):
        audio = None
        async with aiofiles.open(path, "rb") as f:
            audio = await f.read()

        return audio

    @staticmethod
    async def read_http_audio(url, session):
        audio = None
        encoded_url = URL(url, encoded=True)
        async with session.get(encoded_url, timeout=3) as response:
            audio = await response.read()

        return audio

    @staticmethod
    async def read_redis_audio(url, redis_client):
        audio = None
        if not redis_client:
            raise Exception("Redis not initiated")

        key = url.split("//")[1]
        audio = await asyncio.wait_for(redis_client.get(key), timeout=3)
        return audio

    @staticmethod
    async def fetch_and_write(audio_url, session, redis_client, file_path, retry=2):
        # It assumes the checking for allow local was already done.
        # Let's propagate any exception by the main function
        audio = None
        while retry:
            retry -= 1

            try:
                if audio_url.startswith("http"):
                    audio = await AdvancedWorker.read_http_audio(audio_url, session)
                elif audio_url.startswith("redis"):
                    audio = await AdvancedWorker.read_redis_audio(
                        audio_url, redis_client
                    )
                else:
                    audio = await AdvancedWorker.read_local(audio_url)

                audio = AdvancedWorker.is_binary_audio(audio)

                if audio:
                    break

                raise AudioUndecodableException()
            except Exception as e:
                # catch all kinds of error
                if retry == 0:
                    raise e

            await asyncio.sleep(0.5)

        async with aiofiles.open(file_path, "wb") as f:
            await f.write(audio)
