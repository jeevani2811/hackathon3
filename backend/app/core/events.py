import asyncio
import json
from typing import Dict, Set, AsyncGenerator
from datetime import datetime

class EventBus:
    def __init__(self):
        # task_id -> Set of asyncio.Queue
        self._subscribers: Dict[str, Set[asyncio.Queue]] = {}
        # global subscribers for all tasks
        self._global_subscribers: Set[asyncio.Queue] = set()
        self._lock = asyncio.Lock()

    async def subscribe(self, task_id: str) -> asyncio.Queue:
        queue = asyncio.Queue()
        async with self._lock:
            if task_id not in self._subscribers:
                self._subscribers[task_id] = set()
            self._subscribers[task_id].add(queue)
        return queue

    async def unsubscribe(self, task_id: str, queue: asyncio.Queue):
        async with self._lock:
            if task_id in self._subscribers:
                self._subscribers[task_id].discard(queue)
                if not self._subscribers[task_id]:
                    del self._subscribers[task_id]

    async def subscribe_global(self) -> asyncio.Queue:
        queue = asyncio.Queue()
        async with self._lock:
            self._global_subscribers.add(queue)
        return queue

    async def unsubscribe_global(self, queue: asyncio.Queue):
        async with self._lock:
            self._global_subscribers.discard(queue)

    async def publish(self, task_id: str, event_type: str, data: dict):
        payload = {
            "task_id": task_id,
            "event_type": event_type,
            "timestamp": datetime.utcnow().isoformat(),
            "data": data
        }
        raw_msg = f"event: {event_type}\ndata: {json.dumps(payload)}\n\n"

        async with self._lock:
            queues_to_notify = list(self._subscribers.get(task_id, set())) + list(self._global_subscribers)

        for q in queues_to_notify:
            try:
                q.put_nowait(raw_msg)
            except asyncio.QueueFull:
                pass

    async def event_generator(self, task_id: str) -> AsyncGenerator[str, None]:
        queue = await self.subscribe(task_id)
        try:
            # Yield initial connection heartbeat
            yield f"event: ping\ndata: {json.dumps({'status': 'connected', 'task_id': task_id})}\n\n"
            while True:
                msg = await queue.get()
                yield msg
        finally:
            await self.unsubscribe(task_id, queue)

event_bus = EventBus()
