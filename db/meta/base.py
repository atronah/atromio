from configparser import ConfigParser
from contextlib import contextmanager

from sqlalchemy import engine_from_config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DatabaseModel = declarative_base()

engine = None
Session = sessionmaker()


def setup(config, prefix=None):
    prefix = prefix or 'dev'
    global engine
    engine = engine_from_config(config, prefix=prefix)
    Session.configure(bind=engine)
    return engine


def setup_from_file(filename, prefix=None):
    config = ConfigParser()
    config.read(filename)
    return setup(dict(config.items('db')), prefix)


@contextmanager
def start_session(session_class):
    session = session_class()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()