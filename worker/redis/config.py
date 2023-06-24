import os
from dotenv import load_dotenv
import aioredis

load_dotenv()

class Redis():
    def __init__(self):
        self.REDIS_URL = os.environ.get("REDIS_URL", "localhost")
        self.REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", None)
        self.REDIS_USER = os.environ.get("REDIS_USER", None)
        self.connection_url = f"redis://{self.REDIS_USER}:{self.REDIS_PASSWORD}@{self.REDIS_URL}"

    async def create_connection(self):
        self.connection = aioredis.from_url(
                self.connection_url, db=0)
        # return a connection pool
        return self.connection
