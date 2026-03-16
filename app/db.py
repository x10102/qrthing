from peewee import SqliteDatabase, Model, TextField, BooleanField, AutoField, BlobField, UUIDField, ForeignKeyField, IntegerField, CharField, Check

database = SqliteDatabase('data/qrthing.db')

class BaseModel(Model):
    class Meta:
        database = database

class UserRole(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField(20, unique=True)

# type: ignore
class User(BaseModel):
    id = AutoField()
    username = TextField(unique=True)
    password = BlobField()
    is_active = BooleanField(default=True)
    role = ForeignKeyField(UserRole, null=False, backref='users')
    language = CharField(5, default='en')
    
    # Flask-Login stuff
    is_anonymous = False
    is_authenticated = True

class DynamicCode(BaseModel):
    id = UUIDField(primary_key=True)
    name = TextField()
    description = TextField(null=True)
    redirect_code = TextField()
    target = TextField()
    is_active = BooleanField(null=False, default=True)
    owner = ForeignKeyField(User, backref='codes')
    ecc_level = IntegerField(null=False, constraints=[Check('ecc_level >= 0 AND ecc_level <= 3')])