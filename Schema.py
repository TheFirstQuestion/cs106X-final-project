from marshmallow_sqlalchemy import ModelSchema
from marshmallow_sqlalchemy.fields import Nested
from File import *
from marshmallow import post_load


# Basically, this tells marshmallow-sqlalchemy how to serialize the objects, including the link table
# We need to convert the Python objects / SQLite rows into JSON so that the JavaScript can dynamically do everything

class FolderSchema(ModelSchema):
    #children = Nested(lambda: FileSchema(many=True, exclude=("id", "contents")))
    #parent = Nested(lambda: FolderSchema(exclude=("parent",)))

    @post_load
    def make_folder(self, data, **kwargs):
        return Folder(**data)

    class Meta:
        model = Folder

class KeywordSchema(ModelSchema):
    files = Nested(lambda: FileSchema(many=True, exclude=("id", "contents", "keywords")))

    @post_load
    def make_keyword(self, data, **kwargs):
        return Keyword(**data)

    class Meta:
        model = Keyword


class FileSchema(ModelSchema):
    keywords = Nested(KeywordSchema, many=True, exclude=("files", "id"))
    folder = Nested(FolderSchema)

    @post_load
    def make_file(self, data, **kwargs):
        return File(**data)

    class Meta:
        model = File
