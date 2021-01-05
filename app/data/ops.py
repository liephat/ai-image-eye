import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.parser import ConfigParser
from app.data.ids import create_id
from app.data.models import Image, Label, Base


class ImageDataHandler:

    def __init__(self):
        Config = ConfigParser()

        self.session = create_session(Config.data_file())

    def add_new_image(self, file, label_names):
        """
        Adds an image file including its labels to the database.
        :param file: relative path to image file within the image folder
        :param label_names: list of labels describing the image
        """

        # Check if image exists
        image = (
            self.session.query(Image)
                .filter(Image.file == file)
                .one_or_none()
        )

        # Get the labels
        labels = []
        for label_name in label_names:
            label = (
                self.session.query(Label)
                    .filter(Label.name == label_name)
                    .one_or_none()
            )
            # Do we need to create the label?
            if label is None:
                label = Label(label_id=create_id(), name=label_name)
                self.session.add(label)

            labels.append(label)

        # Create image if it not exists
        if image is None:
            image = Image(image_id=create_id(), file=file)
            self.session.add(image)

        image.labels += labels

        # Commit to the database
        self.session.commit()

    def get_images(self):
        """
        Returns all image objects from database.
        """
        return self.session.query(Image).all()

    def get_labels(self):
        """
        Returns all label objects from database.
        """
        return self.session.query(Label).all()

    def get_labellist_for_image(self, file):
        """
        Returns list of labels for one image.
        :param file: relative path to image file within the image folder
        """
        image = (
            self.session.query(Image)
                .filter(Image.file == file)
                .one_or_none()
        )
        return [label.name for label in image.labels]

    def filelist(self):
        """
        Returns a list of all image files.
        """
        return [file for (file,) in self.session.query(Image.file).all()]


def create_session(file):
    """
    Creates and returns a database session.
    :param file: relative path to sqlite file within working directory
    """
    filepath = os.path.join(os.getcwd(), file)

    engine = create_engine(f"sqlite:////{filepath}")
    Base.metadata.create_all(bind=engine)

    Session = sessionmaker()
    Session.configure(bind=engine)

    return Session()
