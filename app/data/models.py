import ast

from sqlalchemy import Column, String, ForeignKey, Integer, Float, Boolean, DateTime, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Image(Base):
    __tablename__ = "image"
    id = Column(Integer, primary_key=True)
    image_id = Column(String, nullable=False)
    file = Column(String, nullable=False, unique=True)
    labels = relationship("Label", secondary="label_assignment", viewonly=True)
    label_assignments = relationship('LabelAssignment', viewonly=True)

    def __repr__(self):
        return f"Image('{self.id}', '{self.image_id}', '{self.file}', '{self.labels}')"

    @hybrid_property
    def url(self):
        return f'/images/{self.file}'

    @hybrid_property
    def thumbnail_url(self):
        from app.controller.thumbnailer import Thumbnailer
        return Thumbnailer.get_thumbnail_url(self)


class Label(Base):
    __tablename__ = "label"
    id = Column(Integer, primary_key=True)
    label_id = Column(String, nullable=False)
    name = Column(String, nullable=False, unique=True)
    images = relationship("Image", secondary="label_assignment", viewonly=True)

    def __repr__(self):
        return f"Label('{self.id}', '{self.label_id}', '{self.name}')"


class LabelAssignment(Base):
    __tablename__ = "label_assignment"
    id = Column(Integer, primary_key=True)
    label_assignment_id = Column(String, nullable=False)

    image_id = Column(String, ForeignKey("image.image_id"))
    label_id = Column(String, ForeignKey("label.label_id"))
    origin_id = Column(String, ForeignKey("origin.origin_id"))
    creation_time = Column(DateTime, default=func.now())
    editable = Column(Boolean, default=False)
    edited = Column(Boolean, default=False)

    confidence = Column(Float)
    bounding_boxes = Column(String)
    """ coordinates of a (single!) bounding box. String representation of a dict
        with normalized (0..1) corners: {'l': left, 't': top, 'b': bottom, 'r', right}
    """

    encoding = Column(String)

    image = relationship("Image", backref=backref("image"))
    label = relationship("Label", backref=backref("label"))
    origin = relationship("Origin")

    def __repr__(self):
        return f"LabelAssignment('{self.id}', '{self.image_id}', '{self.label_id}', '{self.origin_id}', " \
               f"'{self.creation_time}', '{self.confidence}', '{self.bounding_boxes}')"

    @hybrid_property
    def box(self):
        try:
            bounding_box = ast.literal_eval(self.bounding_boxes)
            return dict(
                top=bounding_box['t']*100,
                left=bounding_box['l']*100,
                bottom=100-bounding_box['b']*100,
                right=100-bounding_box['r']*100)
        except (ValueError, TypeError):
            return None


class Origin(Base):
    __tablename__ = "origin"
    id = Column(Integer, primary_key=True)
    origin_id = Column(String, nullable=False)

    name = Column(String, nullable=False)

    def __repr__(self):
        return f"Label('{self.id}', '{self.origin_id}', '{self.name}')"
