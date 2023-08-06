from redisconnection import logger
from redis import Redis
import os


class RedisConnection:
    def __init__(self):
        logger.debug('Initiating Redis Connection Class')
        self._connection_parameter = None
        self._connection = None

    # Use only if you want to pass the arguments
    def set_connection_parameter(self, **kwargs):
        self._connection_parameter = {
            "user": os.environ.get('REDIS_USER') if not kwargs.get('user') else kwargs.get('user'),
            "password": os.environ.get('REDIS_PASSWORD') if not kwargs.get('password') else kwargs.get('password'),
            "host": os.environ.get('REDIS_HOST') if not kwargs.get('host') else kwargs.get('host'),
            "port": os.environ.get('REDIS_PORT') if not kwargs.get('port') else kwargs.get('port'),
            "database": os.environ.get('REDIS_DATABASE') if not kwargs.get('database') else kwargs.get('database')
        }

    def get_connection_parameter(self):
        return self._connection_parameter

    @property
    def connection(self):
        if self._connection is None:
            self.set_connection()
        return self._connection

    def set_connection(self):
        if self._connection_parameter is None:
            self.set_connection_parameter()

        logger.debug('Creating redis connection')
        conn_pool = Redis(
            password=self._connection_parameter['password'],
            host=self._connection_parameter['host'],
            port=self._connection_parameter['port'],
            db=self._connection_parameter['database'])

        self._connection = conn_pool

        try:
            self._connection.ping()
            logger.info('Redis Connection Successful. Connection={}'.format(str(self._connection)))
        except Exception as ce:
            logger.error('Error in making redis connection with host={}, port={}, database={}'.format(
                self._connection_parameter['host'], self._connection_parameter['port'],
                self._connection_parameter['database']), exc_info=True)
            raise Exception("Connection Error with Redis connection={}".format(str(self._connection)))

    # todo
    def close_connection(self):
        if self._connection is not None:
            self._connection = None
