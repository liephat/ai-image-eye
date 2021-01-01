from sqlalchemy import Column, String, ForeignKey, Table, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.data.ids import create_id

Base = declarative_base()

image_label = Table(
    "image_label",
    Base.metadata,
    Column("image_id", String, ForeignKey("image.image_id")),
    Column("label_id", String, ForeignKey("label.label_id"))
)


class Image(Base):
    __tablename__ = "image"
    image_id = Column(String, primary_key=True)
    file = Column(String, unique=True)
    labels = relationship("Label", secondary=image_label, back_populates="images")


class Label(Base):
    __tablename__ = "label"
    label_id = Column(String, primary_key=True)
    name = Column(String, unique=True)
    images = relationship("Image", secondary=image_label, back_populates="labels")


# main method for test purposes, will be removed afterwards
def main():
    # sqlite_filepath = "image_label.db"
    engine = create_engine(f"sqlite:///:memory:", echo=True)
    Base.metadata.create_all(bind=engine)

    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    add_new_image(
        session,
        file="bird.jpg",
        label_names=["bird", "tree", "leaf"],
    )

    get_images(session)
    get_labels(session)


def add_new_image(session, file, label_names):

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

    # Initialize image relationship
    for label in labels:
        image.labels.append(label)

    # Does the image already exist?
    if image is not None:
        # Check if images has labels - how?
        return

    session.add(image)

    # Commit to the database
    session.commit()


def get_images(session):
    return session.query(Image).all()


def get_labels(session):
    return session.query(Label).all()


main()
