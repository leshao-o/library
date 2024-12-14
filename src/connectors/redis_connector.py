import redis.asyncio as redis


class RedisManager:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.redis = None

    async def connect(self):
        self.redis = await redis.Redis(host=self.host, port=self.port)

    async def close(self):
        if self.redis:
            await self.redis.close()
 