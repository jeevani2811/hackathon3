import asyncio
from backend.app.core.logging import logger
from backend.app.orchestration.engine import orchestrator

class BackgroundWorkerRunner:
    def __init__(self):
        self._is_running = False

    async def start(self):
        self._is_running = True
        logger.info("OmniAgent background worker engine initialized.")

    async def stop(self):
        self._is_running = False
        logger.info("OmniAgent background worker engine stopped.")

worker_runner = BackgroundWorkerRunner()
