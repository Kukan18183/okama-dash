import os
import platform

from flask_caching import Cache

plt = platform.system()
if plt == "Linux":
    print("caching in redis")
    cache = Cache(
        config={
            "CACHE_TYPE": "RedisCache",
            "CACHE_REDIS_URL": os.environ.get("CONFIG_REDIS_URL"),
            "CACHE_DEFAULT_TIMEOUT": 500,
        },

    )
else:
    print("caching in filesystem")
    cache = Cache(
        config={
            "CACHE_TYPE": "filesystem",
            "CACHE_DIR": "cache-directory",
            "CACHE_DEFAULT_TIMEOUT": 500,
        },
    )
