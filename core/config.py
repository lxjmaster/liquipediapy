import configparser
import sys
import os


class Config(object):

    def __init__(self, config_file_name="config.ini"):

        self.__root_path__ = sys.path[1]
        self.config_file = self.get_config_file(config_file_name)
        self.config = self.parse_config()

    def get_config_file(self, config_file_name):

        config_file_path = os.path.join(self.__root_path__, config_file_name)

        if os.path.exists(config_file_path):
            return config_file_path

        return None

    def parse_config(self):

        parser = self.parser(self.config_file)
        if parser.has_section("REDIS"):
            redis_host = parser.get("REDIS", "host") if parser.has_option("REDIS", "host") else "localhost"
            redis_port = parser.get("REDIS", "port") if parser.has_option("REDIS", "port") else 6379
            redis_db = parser.get("REDIS", "db") if parser.has_option("REDIS", "db") else 0
            redis_caches = parser.get("REDIS", "caches") if parser.has_option("REDIS", "cache") else True

            setattr(self, "redis_host", redis_host)
            setattr(self, "redis_port", redis_port)
            setattr(self, "redis_db", redis_db)
            setattr(self, "redis_caches", redis_caches)

        if parser.has_section("MONGODB"):
            mongo_host = parser.get("MONGODB", "host") if parser.has_option("MONGODB", "host") else "localhost"
            mongo_port = parser.get("MONGODB", "port") if parser.has_option("MONGODB", "port") else 27017
            mongo_db = parser.get("MONGODB", "db") if parser.has_option("MONGODB", "db") else "liquipedia"

            setattr(self, "mongo_host", mongo_host)
            setattr(self, "mongo_port", mongo_port)
            setattr(self, "mongo_db", mongo_db)

        if parser.has_section("DELAY"):
            delay_time = parser.get("DELAY", "delay_time") if parser.has_option("DELAY", "delay_time") else 30
            setattr(self, "delay_time", int(delay_time))

        if parser.has_section("DEBUG"):
            debug = parser.get("DEBUG", "debug") if parser.has_option("DEBUG", "debug") else "False"
            setattr(self, "debug", debug)

        return parser

    @staticmethod
    def parser(config_file):

        parser = configparser.ConfigParser()

        if os.path.exists(config_file):
            with open(config_file, "r", encoding="utf-8") as f:
                parser.read_file(f)

        return parser


if __name__ == '__main__':
    config = Config()
    print(getattr(config, "redis_cache"))

