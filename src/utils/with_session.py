from functools import wraps

from settings.database import async_session_maker


def with_session(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        session = kwargs.get("session")
        if session is None:
            async with async_session_maker() as session:
                return await func(self, *args, session=session, **kwargs)
        return await func(self, *args, **kwargs)

    return wrapper
