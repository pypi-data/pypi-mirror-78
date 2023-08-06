import logging
import os

import aiofiles
import aiohttp

from yandex_music_agent.common.executor import QueueExecutor


class DownloadTask:
    url: str
    filename: str

    async def on_complete(self):
        pass


class Downloader(QueueExecutor[DownloadTask]):
    CHUNK_SIZE = 1024 * 1024
    logger = logging.getLogger("downloader")

    def __init__(self, parallel: int = QueueExecutor.PARALLEL, chunk_size: int = CHUNK_SIZE):
        super().__init__(parallel)
        self._chunk_size = chunk_size

    async def download_file(self, url: str, filename: str):
        self.logger.debug("Download: %s", filename)
        async with aiohttp.ClientSession() as session:
            async with session.request(method="GET", url=url) as response:
                assert response.status == 200
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                tmp_file_name = f"{filename}.download"
                if os.path.exists(tmp_file_name):
                    os.remove(tmp_file_name)
                async with aiofiles.open(tmp_file_name, "ba") as f:
                    async for data in response.content.iter_chunked(self._chunk_size):
                        await f.write(data)
                os.rename(tmp_file_name, filename)

    async def execute_task(self, task: DownloadTask):
        self.logger.debug("Run task %s", task)
        await self.download_file(task.url, task.filename)
        await task.on_complete()
        self.logger.debug("Complete task %s", task)
