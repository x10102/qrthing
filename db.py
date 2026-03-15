from peewee import SqliteDatabase, Model, TextField, BooleanField, AutoField, BlobField

database = SqliteDatabase('data/qrthing.db')

class BaseModel(Model):
    class Meta:
        database = database

# type: ignore
class User(BaseModel):
    id = AutoField()
    discord = TextField(null=True)
    display_name = TextField(null=True)
    nickname = TextField(unique=True)
    password = BlobField(null=True)
    temp_pw = BooleanField(default=True, null=True)
    wikidot = TextField(unique=True)
    avatar_hash = TextField(default=True, null=True)

    @property
    def can_login(self) -> bool:
        return self.password != None
    
    # Flask-Login stuff
    is_anonymous = False
    is_active = True
    
    @property
    def is_authenticated(self) -> bool:
        return len(self.password) > 0

    def to_dict(self) -> dict:
        return {
        'id': self.id,
        'nickname': self.nickname,
        'wikidot': self.wikidot,
        'discord': self.discord,
        'displayName': self.display_name
    }

    class Meta:
        table_name = 'User'