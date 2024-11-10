import pytest
from magalu_notification.models.notification import Notification, NotificationStatus
from magalu_notification.repositories.notification_repository import PostgresNotificationRepository
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from magalu_notification import settings


@pytest.mark.asyncio
async def test_create_notification(send_notification_data, create_test_database):
    connection_string = (
        f'postgresql+psycopg://{settings.DB_USER}:{settings.DB_PASSWORD}'
        f'@{settings.DB_HOST}:{settings.DB_PORT}/test_db'
    )

    async_engine = create_async_engine(
        connection_string,
    )

    async with async_engine.begin() as conn:
        await conn.run_sync(Notification.metadata.create_all)

    session_factory = async_sessionmaker(async_engine, expire_on_commit=False)

    repository = PostgresNotificationRepository(session_factory)

    notification = await repository.create_notification(send_notification_data)

    async with session_factory() as session:
        db_notification = await session.get(
            Notification, notification.id
        )
    
    assert notification.id == db_notification.id
    assert notification.recipient == db_notification.recipient
    assert notification.message == db_notification.message
    assert notification.send_time == db_notification.send_time
    assert notification.channel == db_notification.channel
    assert notification.status == db_notification.status

    await async_engine.dispose()


@pytest.mark.asyncio
async def test_get_notification(send_notification_data, create_test_database):
    connection_string = (
        f'postgresql+psycopg://{settings.DB_USER}:{settings.DB_PASSWORD}'
        f'@{settings.DB_HOST}:{settings.DB_PORT}/test_db'
    )

    async_engine = create_async_engine(
        connection_string,
    )

    async with async_engine.begin() as conn:
        await conn.run_sync(Notification.metadata.create_all)

    session_factory = async_sessionmaker(async_engine, expire_on_commit=False)

    repository = PostgresNotificationRepository(session_factory)

    notification = Notification(**send_notification_data)

    async with session_factory() as session:
        async with session.begin():
            session.add(notification)
            await session.commit()
        await session.refresh(notification)

    db_notification = await repository.get_notification(notification.id)

    assert notification.id == db_notification.id
    assert notification.recipient == db_notification.recipient
    assert notification.message == db_notification.message
    assert notification.send_time == db_notification.send_time
    assert notification.channel == db_notification.channel
    assert notification.status == db_notification.status

    await async_engine.dispose()


@pytest.mark.asyncio
async def test_update_notification(send_notification_data, create_test_database):
    connection_string = (
        f'postgresql+psycopg://{settings.DB_USER}:{settings.DB_PASSWORD}'
        f'@{settings.DB_HOST}:{settings.DB_PORT}/test_db'
    )

    async_engine = create_async_engine(
        connection_string,
    )

    async with async_engine.begin() as conn:
        await conn.run_sync(Notification.metadata.create_all)

    session_factory = async_sessionmaker(async_engine, expire_on_commit=False)

    repository = PostgresNotificationRepository(session_factory)

    notification = Notification(**send_notification_data)

    async with session_factory() as session:
        async with session.begin():
            session.add(notification)
            await session.commit()
        await session.refresh(notification)

    # Update notification status
    notification.status = NotificationStatus.CANCELED
    updated_notification = await repository.update_notification(notification)

    async with session_factory() as session:
        db_notification = await session.get(
            Notification, updated_notification.id
        )

    assert updated_notification.id == db_notification.id
    assert updated_notification.recipient == db_notification.recipient
    assert updated_notification.message == db_notification.message
    assert updated_notification.send_time == db_notification.send_time
    assert updated_notification.channel == db_notification.channel
    assert updated_notification.status == NotificationStatus.CANCELED

    await async_engine.dispose()
