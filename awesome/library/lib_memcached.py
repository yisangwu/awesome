"""
 Memcached是一个自由开源的，高性能，分布式内存对象缓存系统。
 Memcached是一种基于内存的key-value存储，用来存储小块的任意数据（字符串、对象）。
 Memcached是一个简洁的key-value存储系统。
"""
import memcache


class LibMemcached:

    # 默认所有key的前缀
    key_prefix = 'MAWE_'

    # memcached 连接对象
    obj_memcached = None

    # 默认的过期时间为30天
    DEFAULT_EXPIRE = 2592000;


    def __init__(self, host='127.0.0.1', port=11211, prefix=None, debug=False):
        """
        初始化
        """
        if not host or not port:
            return None
        server = '%s:%s'%(host, port)

        if prefix:
           self.key_prefix = prefix.strip()

        self.obj_memcached = memcache.Client([server], debug=debug)


    def key_make(self, key=None):
        """
        处理所有key，增加前缀
        如果实例化时没有设置，则使用默认前缀
        """
        if not str(key).strip():
            return None

        return self.key_prefix + str(key).strip()


    def set(self, key=None, value=None, expire=None):
        """
        向key存储一个元素值为 var
        字符串和数值直接存储，其他类型序列化后存储
        """
        if not key or value is None:
            return None

        key = key.strip()
        if isinstance(value, str):
            value = value.strip()

        # 过期时间
        if expire is None:
            set_expire = self.DEFAULT_EXPIRE
        else:
            expire = int(expire)
            set_expire = expire if expire<self.DEFAULT_EXPIRE else self.DEFAULT_EXPIRE

        return self.obj_memcached.set(self.key_make(key), value, set_expire)


    def get(self, key=None):
        """
        获取以key作为key存储的元素存储的值
        """
        if not key:
            return None

        key = str(key).strip()
        return self.obj_memcached.get(self.key_make(key))


    def delete(self, key=None):
        """
        通过key删除一个元素
        """
        if not key:
            return None

        key = str(key).strip()
        return self.obj_memcached.delete(self.key_make(key))


    def prepend(self, key=None, value=None):
        """
        向已存在的元素前面追加数据
        """
        if not key or value is None:
            return None

        key = str(key).strip()
        if isinstance(value, str):
            value = value.strip()

        return self.obj_memcached.prepend(self.key_make(key), value)


    def append(self, key=None, value=None):
        """
        向已存在元素后追加数据
        """
        if not key or value is None:
            return None

        key = str(key).strip()
        if isinstance(value, str):
            value = value.strip()

        return self.obj_memcached.append(self.key_make(key), value)
