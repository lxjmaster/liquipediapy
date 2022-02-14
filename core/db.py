import redis
import pymongo
from .config import Config


class RedisObject(object):

    def __init__(self, host=None, port=None, db=None):

        self.config = Config()
        self.client = self.redis_client(host, port, db)

    def redis_client(self, host=None, port=None, db=None):

        try:
            _host = host if host else getattr(self.config, "redis_host")
            _port = port if port else getattr(self.config, "redis_port")
            _db = db if db else getattr(self.config, "redis_db")
            client = redis.StrictRedis(host=_host, port=_port, db=_db)
        except Exception:
            client = None
            assert f"Redis连接失败: {client}"

        return client

    def change_db(self, db):

        self.client = self.redis_client(db=db)


class MongoObject(object):

    def __init__(self, host=None, port=None, db=None):

        self.config = Config()
        self.client = self.mongo_client(host, port)
        self.db = self.change_db(db)

    def mongo_client(self, host=None, port=None, db=None):

        try:
            _host = host if host else getattr(self.config, "mongo_host")
            _port = port if port else getattr(self.config, "mongo_port")
            _db = db if db else getattr(self.config, "mongo_db")
            client = pymongo.MongoClient(host=_host, port=_port)
        except Exception:
            client = None
            assert f"MongoDB连接失败: {client}"

        return client

    def change_db(self, db=None):

        if type(self.client) == pymongo.MongoClient:
            _db = db if db else getattr(self.config, "mongo_db")
            db = self.client[_db]

            return db
        else:
            assert f"MongoDB未连接"
            return None


if __name__ == '__main__':
    mongo = MongoObject()
    print(type(mongo.client) == pymongo.MongoClient)
