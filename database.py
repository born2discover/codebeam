from os import environ
from secrets import token_urlsafe as token
from redis import ConnectionPool, Redis


class Database(object):
    def __init__(self, dburl=environ['REDIS_URL']):
        self.pool = ConnectionPool.from_url(dburl)

    def haskey(self, key, db=None):
        db = Redis(connection_pool=self.pool) if db is None else db
        return db.exists(key)

    def setkey(self, content):
        db = Redis(connection_pool=self.pool)
        uid = token(4)
        while self.haskey(uid, db): uid = token(4)
        db.set(uid, content, ex=86400)
        return uid

    def getkey(self, uid):
        db = Redis(connection_pool=self.pool)
        return db.get(uid).decode()

