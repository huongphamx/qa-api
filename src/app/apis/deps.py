from app.db.session import async_session


def get_async_db():
    try:
        db = async_session()
        yield db
    finally:
        db.close()
