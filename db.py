from peewee import SqliteDatabase, Model, TextField, BooleanField, AutoField, BlobField

database = SqliteDatabase('data/qrthing.db')

class BaseModel(Model):
    class Meta:
        database = database

# type: ignore
class User(BaseModel):
    id = AutoField()
    username = TextField(unique=True)
    password = BlobField(null=True)
    
    # Flask-Login stuff
    is_anonymous = False
    is_active = True

    class Meta:
        table_name = 'User'