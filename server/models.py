import mongoengine as me
from mongoengine import connect, Document, EmbeddedDocument
from mongoengine.fields import BaseField, StringField, DateTimeField, ListField, DictField
from mongoengine.errors import NotUniqueError, OperationError

class Dataset(Document):
    name = StringField(required=True)
    original_images = ListField(StringField())
    augmented_images = DictField()
