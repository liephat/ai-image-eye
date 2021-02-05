from sqlalchemy import Column, String, ForeignKey, Integer, Float, DateTime, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Image(Base):
    __tablename__ = "image"
    id = Column(Integer, primary_key=True)
    image_id = Column(String, nullable=False)
    file = Column(String, nullable=False, unique=True)
    labels = relationship("Label", secondary="label_assignment")

    def __repr__(self):
        return f"Image('{self.id}', '{self.image_id}', '{self.file}', '{self.labels}')"

    @hybrid_property
    def url(self):
        return f'images/{self.file}'

    @hybrid_property
    def thumbnail_url(self):
        from app.controller.thumbnailer import Thumbnailer
        return Thumbnailer.get_thumbnail_url(self)


class Label(Base):
    __tablename__ = "label"
    id = Column(Integer, primary_key=True)
    label_id = Column(String, nullable=False)
    name = Column(String, nullable=False, unique=True)
    images = relationship("Image", secondary="label_assignment")

    def __repr__(self):
        return f"Label('{self.id}', '{self.label_id}', '{self.name}')"


class LabelAssignment(Base):
    __tablename__ = "label_assignment"
    id = Column(Integer, primary_key=True)
    image_id = Column(String, ForeignKey("image.image_id"))
    label_id = Column(String, ForeignKey("label.label_id"))
    origin = Column(String(256), nullable=False)
    creation_time = Column(DateTime, default=func.now())
    confidence = Column(Float)
    bounding_boxes = Column(String)

    image = relationship("Image", backref=backref("image_assoc"))
    label = relationship("Label", backref=backref("label_assoc"))

    def __repr__(self):
        return f"Label('{self.id}', '{self.image_id}', '{self.label_id}', '{self.origin}', '{self.creation_time}', " \
               f"'{self.confidence}', '{self.bounding_boxes}')"
