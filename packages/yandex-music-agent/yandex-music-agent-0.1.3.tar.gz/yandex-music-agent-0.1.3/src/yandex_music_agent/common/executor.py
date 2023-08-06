import asyncio
from typing import Generic, TypeVar, AsyncIterator

T = TypeVar("T")


class QueueExecutor(Generic[T]):
    PARALLEL: int = 8

    def __init__(self, parallel: int = PARALLEL):
        self._parallel = parallel

    async def execute_task(self, task: T):
        raise NotImplementedError

    async def _reader(self, source: AsyncIterator[T], queue: asyncio.Queue):
        async for task in source:
            await queue.put(task)
        for _ in range(self._parallel):
            await queue.put(None)

    async def _executor(self, queue: asyncio.Queue):
        while True:
            task = await queue.get()
            if task is None:
                break
            await self.execute_task(task)
            queue.task_done()

    async def execute(self, source: AsyncIterator[T]):
        queue = asyncio.Queue(self._parallel)
        await asyncio.gather(
            self._reader(source, queue),
            *(self._executor(queue) for _ in range(self._parallel)),
        )
