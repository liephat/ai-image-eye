import logging
import os
from contextlib import contextmanager
from typing import Optional, ContextManager

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session

from app.config.parser import ConfigParser
from app.data.ids import create_id
from app.data.models import Image, Label, Base, LabelAssignment, Origin

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
    def add_image(cls, file):
        # Does image already exist?
        image = cls.get_image(file)
        # Create image if it not exists
        if image is None:
            session = cls._get_main_session()
            image = Image(image_id=create_id(), file=file)
            session.add(image)
            session.commit()

        return image

    @classmethod
    def add_label(cls, label_name):
        # Does label already exist?
        label = cls.get_label(label_name)
        # Create label if it not exists
        if label is None:
            session = cls._get_main_session()
            label = Label(label_id=create_id(), name=label_name)
            session.add(label)
            session.commit()

        return label

    @classmethod
    def add_origin(cls, origin_name):
        # Does origin already exist?
        origin = cls.get_origin(origin_name)
        # Create label if it not exists
        if origin is None:
            session = cls._get_main_session()
            origin = Origin(origin_id=create_id(), name=origin_name)
            session.add(origin)
            session.commit()

        return origin

    @classmethod
    def add_label_assignment(cls, file, label_name, origin_name, confidence=None, bounding_boxes=None):
        """
        Adds a label assignment for an image file to the database.
        :param file: relative path to image file within the image folder
        :param label_name: label describing the image
        :param origin_name: origin of label
        :param confidence: confidence that label is true
        :param bounding_boxes: coordinates of bounding box
        """
        image = cls.add_image(file)
        label = cls.add_label(label_name)
        origin = cls.add_origin(origin_name)
        session = cls._get_main_session()
        label_assignment = LabelAssignment(image=image, label=label, origin=origin,
                                           confidence=confidence, bounding_boxes=bounding_boxes,
                                           label_assignment_id=create_id())
        session.add(label_assignment)
        session.commit()

    @classmethod
    def get_image_by_id(cls, image_id):
        return cls._get_main_session().query(Image).filter(Image.image_id == image_id).one_or_none()
    
    @classmethod
    def get_image(cls, file):
        return cls._get_main_session().query(Image).filter(Image.file == file).one_or_none()

    @classmethod
    def get_label(cls, label_name):
        return cls._get_main_session().query(Label).filter(Label.name == label_name).one_or_none()

    @classmethod
    def get_origin(cls, origin_name):
        return cls._get_main_session().query(Origin).filter(Origin.name == origin_name).one_or_none()

    @classmethod
    def get_labels_of_image(cls, file):
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

    @classmethod
    def all_label_assignments(cls):
        return cls._get_main_session().query(LabelAssignment).all()

    @classmethod
    def filtered_images(cls, queryString):
        if '*' in queryString:
            likeString = queryString.replace('*', '%')
            labels = cls._get_main_session().query(Label).filter(Label.name.like(likeString)).all()
        else:
            labels = cls._get_main_session().query(Label).filter(Label.name == queryString).all()

        return list(set(image for label in labels for image in label.images))

