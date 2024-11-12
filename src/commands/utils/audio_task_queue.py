import asyncio
from collections import defaultdict

class AudioTaskQueue(object):
    def __init__(self):
        self.queues = defaultdict(asyncio.Queue)

    async def enqueue(self, guild_id, task):
        await self.queues[guild_id].put(task)

    async def dequeue(self, guild_id):
        q = self.queues[guild_id]
        if not q.empty():
            return await self.queues[guild_id].get()
        else:
            return None

    async def clear(self, guild_id):
        q = self.queues[guild_id]
        while not q.empty():
            await q.get()

    def test(self):
        print()


audio_task_queue = AudioTaskQueue()