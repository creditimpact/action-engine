"""Simple scheduler placeholder.

This module contains a minimal in-memory scheduler used for documentation and
future expansion. The idea is that timed actions will enqueue tasks for later
processing by a worker.  For now the logic merely stores actions in a queue
and executes them when ``run`` is called.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any

from executor import execute


@dataclass
class ScheduledAction:
    action: Any
    execute_at: float  # Unix timestamp indicating when to run


class Scheduler:
    """In-memory scheduler used as a placeholder for future implementations."""

    def __init__(self) -> None:
        self._queue: asyncio.Queue[ScheduledAction] = asyncio.Queue()

    async def schedule(self, action: Any, execute_at: float) -> None:
        """Add an action to be executed at ``execute_at``.

        In a real deployment this method would enqueue tasks into a persistent
        job queue (e.g. Celery or RQ) so a background worker can pick them up
        at the desired time.  Here we simply store them locally.
        """

        await self._queue.put(ScheduledAction(action=action, execute_at=execute_at))

    async def run(self) -> None:
        """Continuously process scheduled actions."""

        while True:
            scheduled = await self._queue.get()
            # Wait until the scheduled time and then execute.
            delay = max(0, scheduled.execute_at - asyncio.get_event_loop().time())
            if delay:
                await asyncio.sleep(delay)
            await execute(scheduled.action)
            self._queue.task_done()
