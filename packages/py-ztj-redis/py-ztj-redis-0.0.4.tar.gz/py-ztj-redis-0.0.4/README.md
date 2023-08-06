# Redis

## 说明
这是一个 Redis 实例模块。

### 链接
- [GitHub](https://github.com/ztj-package/py-redis)
- [PyPI](https://pypi.org/project/py-ztj-redis)

## 安装
```
pip install py-ztj-redis
```

## 依赖
```
pip install redis
pip install py-ztj-registry==0.0.4
```

## 使用
```
from ZtjRedis import Redis

redis = Redis()
print(redis.ping())
```
