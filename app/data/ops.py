import logging
import os
from contextlib import contextmanager
from typing import Optional, ContextManager

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session

from app.config.parser import ConfigParser
from app.data.ids import create_id
from app.data.models import Image, Label, Base

logger = logging.getLogger(__name__)


class ImageDataHandler:
    _main_session: Optional[Session] = None
    _engine: Optional[Engine] = None
    _session_class = None

    @classmethod
    def _get_main_session(cls):
        """ The main session should be used for all database reading """
        if cls._main_session is None:
            cls._main_session = cls._create_session()
        return cls._main_session

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
    def reset(cls):
        if cls._main_session:
            cls._main_session.close()
            cls._main_session = None
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
    def add_new_image(cls, file, label_names):
        """
        Adds an image file including its labels to the database.
        :param file: relative path to image file within the image folder
        :param label_names: list of labels describing the image
        """

        with cls.auto_session() as session:
            # Check if image exists
            image = (
                session.query(Image)
                    .filter(Image.file == file)
                    .one_or_none()
            )

            # Get the labels
            labels = []
            for label_name in label_names:
                label = (
                    session.query(Label)
                        .filter(Label.name == label_name)
                        .one_or_none()
                )
                # Do we need to create the label?
                if label is None:
                    label = Label(label_id=create_id(), name=label_name)
                    session.add(label)

                labels.append(label)

            # Create image if it not exists
            if image is None:
                image = Image(image_id=create_id(), file=file)
                session.add(image)

            image.labels += labels

    @classmethod
    def get_labellist_for_image(cls, file):
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
    def filelist(cls):
        """
        Returns a list of all image files.
        """
        with cls.auto_session() as session:
            return [file for (file,) in session.query(Image.file).all()]

    @classmethod
    def all_images(cls):
        return cls._get_main_session().query(Image).all()

    @classmethod
    def all_labels(cls):
        return cls._get_main_session().query(Label).all()
