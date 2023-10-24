import redis

class RedisManager:
    def __init__(self, host='127.0.0.1', port=6379, db=0):
        self._redis = redis.StrictRedis(host=host, port=port, db=db)
        self._rpc_https_key = 'rpc_https_count'

    def create_https(self):
        current_count = self._redis.incr(self._rpc_https_key)
        if current_count > 3:
            self._redis.decr(self._rpc_https_key)
            return self._rpc_https_key

    def close_https(self):
        self._redis.decr(self._rpc_https_key)
        return self._rpc_https_key

    def publish_update(self, channel, message):
        self._redis.publish(channel, message)

    def subscribe(self, channel):
        pubsub = self._redis.pubsub()
        pubsub.subscribe(channel)
        return pubsub

redis_manager = RedisManager()
