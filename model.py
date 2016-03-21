from peewee import *
from logging import log

class _Proxy(Proxy):
    """
    """

    def initialize_by_uri(self, uri, check=True):
        import re
        URI_PATTERN = r'(?P<driver>\w+)://((?P<username>[\w|\d]+):(?P<password>[\w|\d]+)@' \
                      r'(?P<host>[\w|\d]+)(:(?P<port>\d+))?)?/(?P<db_name>.+)'
        result = re.match(URI_PATTERN, uri)
        if result is None:
            raise RuntimeError()

        results = result.groupdict()
        driver = results['driver']
        username = results['username']
        password = results['password']
        host = results['host']
        port = results['port']
        db_name = results['db_name']

        if driver != 'mysql':
            raise RuntimeError()

        assert username is not None and password is not None
        assert host is not None and db_name is not None
        port = int(port) if port else 3306
        self.initialize(MySQLDatabase(db_name, host=host, port=port, user=username, passwd=password))

        if check is True:
            try:
                db.connect()
            except:
                raise RuntimeError()

db = _Proxy()


class BaseModel(Model):
    class Meta:
        database = db


class Artist(BaseModel):
    pixiv_id = IntegerField(unique=True)
    name = CharField()


class Illust(BaseModel):
    illust_id = IntegerField(unique=True)
    title = CharField()
    url = CharField()
    artist = ForeignKeyField(Artist, related_name='illustration')
    upload_timestamp = IntegerField()
    page_count = IntegerField()




