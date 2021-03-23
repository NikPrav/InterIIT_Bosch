import mongoengine as me
from configs import cnf
from mongoengine import Document, EmbeddedDocument, connect
from mongoengine.errors import NotUniqueError, OperationError
from mongoengine.fields import (BaseField, DateTimeField, DictField, IntField,
                                EmailField, ListField, ObjectIdField,
                                StringField)

connect(db=cnf.APP_CONFIG.DB)


class Info(Document):
    _id = ObjectIdField()
    uneditable_workspaces = ListField(StringField())


class Workspace(Document):
    _id = ObjectIdField()
    name = StringField(required=True)
    num = IntField()
    datasets = ListField(StringField())
    added_images = DictField()
    augmentations = DictField()
    model_settings = DictField()
    model_results = DictField()
    user_email = EmailField()
    created_at = DateTimeField()
    updated_at = DateTimeField()


class Dataset(Document):
    _id = ObjectIdField()
    name = StringField(required=True)


class Globals(Document):
    _id = ObjectIdField()
    name = StringField(required=True)
    value = StringField(required=True)


class User(Document):
    _id = ObjectIdField()
    email = EmailField()
    token = StringField()
    num = IntField()
