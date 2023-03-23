import peewee
from datetime import datetime
import pytz
from playhouse.sqlite_ext import JSONField
from playhouse.migrate import migrate,SqliteMigrator
''' Class for communication with database.db here '''
db = peewee.SqliteDatabase('database.db')


class User(peewee.Model):
    id = peewee.AutoField()
    chat_id = peewee.BigIntegerField(unique=True)
    balance = peewee.FloatField(default=0)
    language = peewee.TextField(null=True)
    ref = peewee.TextField(null=True)
    reg_date = peewee.DateTimeField(default=datetime.now(pytz.timezone('Europe/Kiev')))

    class Meta:
        database = db
        db_table = 'users'


class Username(peewee.Model):
    id = peewee.AutoField()
    first_name = peewee.TextField(null=True)
    username = peewee.TextField(null=True)
    is_active = peewee.BooleanField(default=True)

    class Meta:
        database = db
        db_table = 'usernames'

class Group(peewee.Model):
    id = peewee.AutoField()
    username = peewee.TextField(null=True)
    users = JSONField(default=[])

    class Meta:
        database = db
        db_table = 'groups'

class Task(peewee.Model):
    id = peewee.AutoField()
    chat_id = peewee.BigIntegerField()
    usernames = JSONField(default=[])
    type = peewee.TextField(default="SEND")
    text = peewee.TextField(null=True)
    is_done = peewee.BooleanField(default=False)
    is_moderating = peewee.BooleanField(default=False)

    class Meta:
        database = db
        db_table = 'tasks'


class Config(peewee.Model):
    id = peewee.AutoField()
    key = peewee.TextField(null=True)
    value = peewee.TextField(null=True)
    values = JSONField(default=[])
    # is_done = peewee.BooleanField(default=False)

    class Meta:
        database = db
        db_table = 'config'

User.create_table()
Username.create_table()
Task.create_table()
Config.create_table()
Group.create_table()


# migrator = SqliteMigrator(db)
# migrate(
#     # migrator.add_column('searches', 'category', Search.category),
#     migrator.add_column('tasks', 'type', Task.type),
# )

text = Config.get_or_none(Config.key == "TEXT")
if not text:
    Config(key="TEXT",value="TEST").save()

price = Config.get_or_none(Config.key == "PRICE")
if not price:
    Config(key="PRICE",value="1").save()
price = Config.get_or_none(Config.key == "PRICE2")
if not price:
    Config(key="PRICE2",value="1").save()