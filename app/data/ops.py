import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.parser import ConfigParser
from app.data.ids import create_id
from app.data.models import Image, Label, Base


@contextmanager
def auto_session(Session):
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        print("D'oh!", e.__class__, "occurred.")
        session.rollback()
    finally:
        session.close()


class ImageDataHandler:

    def __init__(self):
        config = ConfigParser()

        filepath = os.path.join(os.getcwd(), config.data_file())
        engine = create_engine(f"sqlite:////{filepath}")
        Base.metadata.create_all(bind=engine)

        self.Session = sessionmaker()
        self.Session.configure(bind=engine)

    def add_new_image(self, file, label_names):
        """
        Adds an image file including its labels to the database.
        :param file: relative path to image file within the image folder
        :param label_names: list of labels describing the image
        """

        with auto_session(self.Session) as session:
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

    def get_labellist_for_image(self, file):
        """
        Returns list of labels for one image.
        :param file: relative path to image file within the image folder
        """
        with auto_session(self.Session) as session:
            image = (
                session.query(Image)
                    .filter(Image.file == file)
                    .one_or_none()
            )
            return [label.name for label in image.labels]

    def filelist(self):
        """
        Returns a list of all image files.
        """
        with auto_session(self.Session) as session:
            return [file for (file,) in session.query(Image.file).all()]
