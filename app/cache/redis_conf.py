import redis

from app.core.config import settings

r = redis.from_url(settings.CACHE_HOST)


# check connection in debug
if __name__ == '__main__':
    print(r.ping())
    print(r.get('test'))
    print(r.delete('test'))
    print(r.get('test'))
