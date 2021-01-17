from sqlalchemy import Column, String, ForeignKey, Table, Integer
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

image_label = Table(
    "image_label",
    Base.metadata,
    Column("image_id", String, ForeignKey("image.image_id")),
    Column("label_id", String, ForeignKey("label.label_id"))
)


class Image(Base):
    __tablename__ = "image"
    id = Column(Integer, primary_key=True)
    image_id = Column(String, nullable=False)
    file = Column(String, nullable=False, unique=True)
    labels = relationship("Label", secondary=image_label, back_populates="images")

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
    images = relationship("Image", secondary=image_label, back_populates="labels")

    def __repr__(self):
        return f"Label('{self.id}', '{self.label_id}', '{self.name}')"
