from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.app.models import MemoryItem

class MemoryStore:
    def __init__(self):
        # In-memory working scratchpad: task_id -> dict
        self._working_memory: Dict[str, Dict[str, Any]] = {}

    def get_working_memory(self, task_id: str) -> Dict[str, Any]:
        if task_id not in self._working_memory:
            self._working_memory[task_id] = {
                "evidence": [],
                "assumptions": [],
                "financial_data": {},
                "matrix_data": {},
                "analysis": {},
                "validation": {}
            }
        return self._working_memory[task_id]

    def update_working_memory(self, task_id: str, key: str, value: Any):
        mem = self.get_working_memory(task_id)
        mem[key] = value

    async def persist_memory_item(
        self,
        db: AsyncSession,
        task_id: str,
        memory_type: str,
        key: str,
        content: str,
        source_url: Optional[str] = None,
        confidence: float = 1.0
    ) -> MemoryItem:
        item = MemoryItem(
            task_id=task_id,
            memory_type=memory_type,
            key=key,
            content=content,
            source_url=source_url,
            confidence=confidence
        )
        db.add(item)
        await db.commit()
        await db.refresh(item)
        return item

    async def get_persisted_memories(self, db: AsyncSession, task_id: str) -> List[MemoryItem]:
        result = await db.execute(select(MemoryItem).where(MemoryItem.task_id == task_id))
        return list(result.scalars().all())

    def clear_working_memory(self, task_id: str):
        if task_id in self._working_memory:
            del self._working_memory[task_id]

memory_store = MemoryStore()
