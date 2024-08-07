from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from magalu_notification import settings


class PostgresConnection:
    CONNECTION = None

    @classmethod
    def get_connection(cls):
        if cls.CONNECTION is None:
            connection_string = (
                f'postgresql+psycopg://{settings.DB_USER}:{settings.DB_PASSWORD}'
                f'@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}'
            )
            cls.CONNECTION = create_async_engine(connection_string)
        return cls.CONNECTION
    
    @classmethod
    def get_session(cls):
        return async_sessionmaker(cls.get_connection(), expire_on_commit=False)
