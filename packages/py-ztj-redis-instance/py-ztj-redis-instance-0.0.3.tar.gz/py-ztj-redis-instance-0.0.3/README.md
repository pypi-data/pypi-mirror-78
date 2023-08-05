# Redis

## 说明
这是一个 Redis 实例模块。

### 链接
- [GitHub](https://github.com/ztj-package/py-redis-instance)
- [PyPI](https://pypi.org/project/py-ztj-redis-instance)

## 安装
```
pip install py-ztj-redis
```

## 依赖
```
pip install redis>=3.2.1
pip install py-ztj-registry>=0.0.1
```

## 使用
```
from redis_instance import Redis

redis_instance = Redis()
print(redis_instance.ping())
```
