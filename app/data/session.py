import logging
import os
import threading
import time
from typing import Optional, Dict, Tuple

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session

from app.config.parser import ConfigParser
from app.data.models import Base

logger = logging.getLogger(__name__)

class SessionWrapper:
    """ Helper class that manages the life-cycle of SQLAlchemy sessions """

    _sessions: Dict[Tuple[str, int, int], 'SessionWrapper'] = {}  # current sessions, indexed by thread
    _sessions_lock = threading.RLock()  # prevents concurrent manipulation of _sessions dict
    _engine: Optional[Engine] = None
    _session_class = None

    MAX_AGE = 60  # maximum session age in seconds

    @classmethod
    def get_session(cls) -> 'SessionWrapper':
        """ Create or get a session that is unique to the current thread. """

        # Try to be as unique as possible, as thread ids (Thread.get_ident()) may be recycled.
        thread_id = (threading.current_thread().getName(),
                     id(threading.current_thread()),
                     threading.get_ident())

        with cls._sessions_lock:
            session_wrapper = cls._sessions.get(thread_id)
            if session_wrapper is None or not session_wrapper.is_valid():
                logger.info(f'Creating database session for {thread_id}')
                session_wrapper = SessionWrapper(cls._create_session())
                cls._sessions[thread_id] = session_wrapper
            cls._close_old_sessions()
            return session_wrapper

    @classmethod
    def _create_session(cls):
        cls._init_engine()
        return cls._session_class()

    @classmethod
    def _close_old_sessions(cls):
        """ Auto-close all sessions that are old """
        with cls._sessions_lock:
            for key, session_wrapper in cls._sessions.copy().items():
                if session_wrapper.close_if_old():
                    logger.info(f'Removing old session for {key}')
                    del cls._sessions[key]

    @classmethod
    def _init_engine(cls):
        """ On first access, the database engine and session class is initialized """
        if cls._engine is None:
            config = ConfigParser()
            filepath = os.path.join(os.getcwd(), config.data_file())
            cls._engine = create_engine(f"sqlite:////{filepath}")
            Base.metadata.create_all(bind=cls._engine)

            cls._session_class = sessionmaker()
            cls._session_class.configure(bind=cls._engine)

    @classmethod
    def reset(cls):
        with cls._sessions_lock:
            for session in cls._sessions.values():
                session.close()
            cls._sessions = {}
        if cls._engine:
            cls._engine.dispose()
            cls._engine = None
        cls._session_class = None

    def __init__(self, session):
        self._session: Session = session
        self._in_use = False
        self._access_time = time.time()

    def _get_session(self):
        assert self._session is not None
        self._access_time = time.time()
        self._in_use = True
        return self._session

    def done(self):
        self._in_use = False

    def close_if_old(self):
        """ Close long running, unused session """
        if self._in_use or time.time() - self._access_time < self.MAX_AGE:
            return False
        self.close()
        return True

    def is_valid(self):
        return self._session is not None

    def commit(self):
        self.done()
        self._session.commit()

    def add(self, element):
        self._get_session().add(element)

    def query(self, *entities, **kwargs):
        return self._get_session().query(*entities, **kwargs)

    def close(self):
        if self._session is None:
            return
        self.done()
        self._get_session().close()
        self._session = None


