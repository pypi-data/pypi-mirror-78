# <h2 id="title">LRU Cache</h2>
Thư viện caching của MOBIO. Hỗ trợ cache trên memory hoặc Redis.

#### Cài đặt:
`pip3 install m-caching`

#### Sử dụng:
```
__store_type = StoreType.REDIS # for redis cache
__store_type = StoreType.LOCAL # for memory cache
__file_config = 'config-file-path'

lru_redis_cache = LruCache(store_type=__store_type, config_file_name=__file_config,
                           redis_uri='redis://redis:6379/0')

```
Ignore empty values from cache
```
__store_type = StoreType.REDIS
__file_config = 'config-file-path'
lru_cache = LruCache(store_type=__store_type, config_file_name=__file_config)
lru_cache.accept_none(False) # => ignore none values
``` 

#### Usage
cache for class's function
```
class TestCache:
    @lru_cache.add_for_class()
    def test(self, x):
        print("TestCache::test param %s" % x)
        return x + 1

    @staticmethod
    @lru_cache.add()
    def test_static(x):
        print("TestCache::test_static test param %s" % x)
        return x + 1
```

cache for normal function
```
@lru_cache.add()
def some_expensive_method(x):
    print("Calling some_expensive_method(" + str(x) + ")")
    return x + 200
```

#### Example config
```
[REDIS]
host=redis-server
port=6379
cache_prefix=test_cache
```
