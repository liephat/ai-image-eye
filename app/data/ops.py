import logging
import os
import threading
import time
from contextlib import contextmanager
from typing import Optional, ContextManager, List, Dict, Tuple

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session

from app.config.parser import ConfigParser
from app.data.ids import create_id
from app.data.models import Image, Label, Base, LabelAssignment, Origin

logger = logging.getLogger(__name__)


class SessionWrapper:
    """ Helper class that manages the life-cycle of an SQLAlchemy session """

    MAX_AGE = 60  # maximum session age in seconds

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


class ImageDataHandler:
    _sessions: Dict[Tuple[str, int, int], SessionWrapper] = {}
    _sessions_lock = threading.RLock()
    _engine: Optional[Engine] = None
    _session_class = None

    @classmethod
    def _get_session(cls) -> SessionWrapper:
        """ Create a session that is unique to the current thread. """

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
    def _create_session(cls):
        cls._init_engine()
        return cls._session_class()

    @classmethod
    def _commit_session(cls):
        cls._get_session().commit()

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

    @classmethod
    @contextmanager
    def auto_session(cls) -> ContextManager[Session]:
        """ Yields a new session and commits and closes it afterwards """
        session = cls._create_session()
        try:
            yield session
            session.commit()
        except Exception:  # pylint: disable=broad-except
            logger.exception('Session will be rolled back')
            session.rollback()
        finally:
            session.close()

    @classmethod
    def get_or_add_image(cls, file: str):
        # Does image already exist?
        image = cls.get_image(file)
        # Create image if it not exists
        if image is None:
            session = cls._get_session()
            image = Image(image_id=create_id(), file=file)
            session.add(image)
            session.commit()

        return image

    @classmethod
    def get_or_add_label(cls, label_name: str):
        # Does label already exist?
        label = cls.get_label(label_name)
        # Create label if it not exists
        if label is None:
            session = cls._get_session()
            label = Label(label_id=create_id(), name=label_name)
            session.add(label)
            session.commit()

        return label

    @classmethod
    def get_or_add_origin(cls, origin_name: str):
        # Does origin already exist?
        origin = cls.get_origin(origin_name)
        # Create label if it not exists
        if origin is None:
            session = cls._get_session()
            origin = Origin(origin_id=create_id(), name=origin_name)
            session.add(origin)
            session.commit()

        return origin

    @classmethod
    def add_label_assignment(cls, file: str, label_name: str, origin_name: str, confidence=None, bounding_boxes=None,
                             encoding=None, editable=None):
        """
        Adds a label assignment for an image file to the database.
        :param file: relative path to image file within the image folder
        :param label_name: label describing the image
        :param origin_name: origin of label
        :param confidence: confidence that label is true
        :param bounding_boxes: coordinates of a (single!) bounding box as a dict
                               with normalized (0..1) corners: {'l': left, 't': top, 'b': bottom, 'r', right}
        :param editable: specifies whether label should be editable by user or not
        :param encoding: encoding of detected object
        """
        assert bounding_boxes is None or isinstance(bounding_boxes, dict)
        image = cls.get_or_add_image(file)
        label = cls.get_or_add_label(label_name)
        origin = cls.get_or_add_origin(origin_name)
        session = cls._get_session()
        label_assignment = LabelAssignment(image=image, label=label, origin=origin, confidence=confidence,
                                           bounding_boxes=repr(bounding_boxes), encoding=encoding,
                                           editable=editable, label_assignment_id=create_id())
        session.add(label_assignment)
        session.commit()

    @classmethod
    def get_image_by_id(cls, image_id: str):
        return cls._get_session().query(Image).filter(Image.image_id == image_id).one_or_none()

    @classmethod
    def get_image(cls, file: str):
        return cls._get_session().query(Image).filter(Image.file == file).one_or_none()

    @classmethod
    def get_label(cls, label_name: str):
        return cls._get_session().query(Label).filter(Label.name == label_name).one_or_none()

    @classmethod
    def get_label_by_id(cls, label_id: str):
        return cls._get_session().query(Label).filter(Label.label_id == label_id).one_or_none()

    @classmethod
    def get_origin(cls, origin_name: str):
        return cls._get_session().query(Origin).filter(Origin.name == origin_name).one_or_none()

    @classmethod
    def get_labels_of_image(cls, file) -> List[str]:
        """
        Returns list of labels for one image.
        :param file: relative path to image file within the image folder
        """
        with cls.auto_session() as session:
            image = (
                session.query(Image)
                    .filter(Image.file == file)
                    .one_or_none()
            )
            return [label.name for label in image.labels]

    @classmethod
    def get_assignments_from_origin(cls, file: str, origin_name: str) -> List[LabelAssignment]:
        """
        Returns a list of label assignments of an image that originate from a defined source.
        :param origin_name: origin of label assignment
        :param file: relative path to image file within the image folder
        """
        image = cls.get_image(file)
        origin = cls.get_origin(origin_name)

        if image is None or origin is None:
            return []

        session = cls._get_session()
        label_assignments = (
            session.query(LabelAssignment)
                .filter(LabelAssignment.image == image, LabelAssignment.origin == origin)
                .all()
        )
        return label_assignments

    @classmethod
    def update_label_assignment_label_name(cls, label_assignment_id: str, label_name: str) -> LabelAssignment:
        # Update the label
        assignment = cls.get_label_assignment_by_id(label_assignment_id)
        if assignment is None:
            return None
        label = cls.get_or_add_label(label_name)
        assignment.label = label
        cls._commit_session()
        return assignment

    @classmethod
    def filelist(cls) -> List[str]:
        """
        Returns a list of all image files.
        """
        with cls.auto_session() as session:
            return [file for (file,) in session.query(Image.file).all()]

    @classmethod
    def all_images(cls) -> List[Image]:
        return cls._get_session().query(Image).all()

    @classmethod
    def all_labels(cls) -> List[Label]:
        return cls._get_session().query(Label).all()

    @classmethod
    def all_label_assignments(cls) -> List[LabelAssignment]:
        return cls._get_session().query(LabelAssignment).all()

    @classmethod
    def get_label_assignment_by_id(cls, label_assignment_id: str) -> LabelAssignment:
        return cls._get_session().query(LabelAssignment)\
            .filter(LabelAssignment.label_assignment_id == label_assignment_id).one_or_none()

    @classmethod
    def filtered_images(cls, query_string: str) -> List[Image]:
        if '*' in query_string:
            like_string = query_string.replace('*', '%')
            labels = cls._get_session().query(Label).filter(Label.name.like(like_string)).all()
        else:
            labels = cls._get_session().query(Label).filter(Label.name == query_string).all()

        return list(set(image for label in labels for image in label.images))

