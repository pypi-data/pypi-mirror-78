from redisconnection import logger, redis_connection


def test_connection():
    rd = redis_connection.RedisConnection()
    conn = rd.connection
    rd.close_connection()


if __name__ == '__main__':
    logger.warning(f'Executing {__file__}')
    test_connection()




