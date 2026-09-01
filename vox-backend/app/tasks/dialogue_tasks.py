import asyncio

from celery import Task
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from app.core.config import settings
from app.models.dialogue import (
    Dialogue,
    DialogueStatus,
)
from app.tasks.celery_app import celery_app


async def process_dialogue_async(
    dialogue_id: int,
) -> None:
    engine = create_async_engine(
        settings.DATABASE_URL,
        poolclass=NullPool,
    )

    session_factory = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
    )

    try:
        async with session_factory() as db:
            dialogue = await db.get(
                Dialogue,
                dialogue_id,
            )

            if dialogue is None:
                return

            if dialogue.status == DialogueStatus.COMPLETED:
                return

            # TEMPORARY MOCK.
            #
            # Later this block will call the real AI pipeline:
            #
            # S3 file
            #   -> STT
            #   -> Qwen
            #   -> structured result
            #
            # For now we only verify that:
            # FastAPI -> Redis -> Celery -> PostgreSQL
            # works correctly.

            await asyncio.sleep(3)

            dialogue.status = DialogueStatus.COMPLETED
            dialogue.error_message = None

            await db.commit()

    finally:
        await engine.dispose()


async def mark_dialogue_as_error(
    dialogue_id: int,
    error_message: str,
) -> None:
    engine = create_async_engine(
        settings.DATABASE_URL,
        poolclass=NullPool,
    )

    session_factory = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
    )

    try:
        async with session_factory() as db:
            dialogue = await db.get(
                Dialogue,
                dialogue_id,
            )

            if dialogue is None:
                return

            dialogue.status = DialogueStatus.ERROR
            dialogue.error_message = error_message[:2000]

            await db.commit()

    finally:
        await engine.dispose()


@celery_app.task(
    bind=True,
    name="dialogues.process",
    max_retries=3,
)
def process_dialogue(
    self: Task,
    dialogue_id: int,
) -> None:
    try:
        asyncio.run(
            process_dialogue_async(
                dialogue_id
            )
        )

    except Exception as exc:
        if self.request.retries < self.max_retries:
            countdown = 2 ** self.request.retries

            raise self.retry(
                exc=exc,
                countdown=countdown,
            )

        asyncio.run(
            mark_dialogue_as_error(
                dialogue_id=dialogue_id,
                error_message=str(exc),
            )
        )

        raise