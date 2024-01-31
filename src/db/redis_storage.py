import redis

from core.config import RedisConfig

conf = RedisConfig()

jwt_redis_blocklist = redis.StrictRedis(
    host=conf.host,
    port=conf.port,
    decode_responses=True
)