from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base, as_declarative
from sqlalchemy.pool import NullPool
from sqlalchemy_utils import database_exists, create_database
from contextlib import contextmanager

# postgresql+pg8000://{user}:{password}@{hostname}:{port}/{db}
engine = create_engine('postgresql+pg8000://postgres:postgres@postgres:5432/simple', poolclass=NullPool, echo=True)


@contextmanager
def session_scope():

    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    try:
        yield db_session
        db_session.commit()
    except Exception as es:
        db_session.rollback()
        raise es
    finally:
        db_session.close()



Base = declarative_base()


# @as_declarative()
# class Base:
#     def _asdict(self):
#         return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

# Base = as_declarative()
# Base.metadata.create_all(engine)

with session_scope() as db_session:
    Base.query = db_session.query_property()


if __name__ == "__main__":
    with session_scope() as db_session:
        print(db_session)