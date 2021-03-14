import mongoengine as me
from mongoengine import Document, EmbeddedDocument, connect
from mongoengine.errors import NotUniqueError, OperationError
from mongoengine.fields import (BaseField, DateTimeField, DictField, ListField,
                                StringField)


class Dataset(Document):
    name = StringField(required=True)
    original_images = ListField(StringField())
    augmented_images = DictField()
