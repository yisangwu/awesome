"""
Redis 操作类

Redis是完全开源免费的，遵守BSD协议，是一个高性能的key-value数据库。
Redis支持数据的持久化。
Redis支持简单的key-value类型，还提供list，set，zset，hash等数据结构的存储。
Redis支持数据的备份，即master-slave模式的数据备份。

Redis读的速度是110000次/s,写的速度是81000次/s
Redis的所有操作都是原子性的，同时Redis还支持对几个操作全并后的原子性执行。

"""
import functools
from redis import StrictRedis


def wraps_set_expire(func):
    """
    装饰器， 设置key默认过期时间
    """
    @functools.wraps(func)
    def wrapper_func(self, keyname, *args, **kwargs):
        ret_func = func(self, keyname, *args, **kwargs)
        # 设置key的过期时间
        if ret_func is not None:
            self.set_expire(keyname)
        return ret_func

    return wrapper_func


class LibRedis:

    # 默认所有key的前缀
    key_prefix = 'RAWE_'

    # redis 连接对象
    obj_redis = None

    # 默认的过期时间为3天
    DEFAULT_EXPIRE = 259200;


    def __init__(self, host, port, db, prefix=None, charset='utf-8'):
        """
        初始化
        """
        if not host or not port:
            return None

        if prefix:
           self.key_prefix = prefix.strip()
        # construct
        self.obj_redis = StrictRedis(host=host, port=port, db=db, charset='utf-8')


    def key_make(self, keyname=None):
        """
        处理所有key，增加前缀
        如果实例化时没有设置，则使用默认前缀
        """
        if not keyname:
            return None

        return self.key_prefix + str(keyname).strip()


    def set_expire(self, keyname=None):
        """
        设置key的过期时间，装饰器调用
        """
        if not keyname:
            return None

        return self.obj_redis.expire(self.key_make(keyname), self.DEFAULT_EXPIRE)


    # --------------------------------------------------------
    # String
    # --------------------------------------------------------


    @wraps_set_expire
    def set(self, keyname=None, value=None):
        """
        设置指定 key 的值。
        如果 key 已经存储其他值， SET 就覆写旧值，且无视类型。
        return：
        设置操作成功完成时，才返回 OK
        """
        if not keyname or value is None:
            return None

        keyname = self.key_make(keyname.strip())
        if isinstance(value, str):
            value = value.strip()

        return self.obj_redis.set(keyname, value)


    def get(self, keyname=None):
        """
        获取指定 key 的值。
        return：
        key 的值
        如果 key 不存在，返回 nil。
        如果key 储存的值不是字符串类型，返回一个错误。
        """
        if not keyname:
            return None

        keyname = self.key_make(keyname.strip())
        result = self.obj_redis.get(keyname)

        return None if not result else bytes.decode(result)


    def delete(self, keyname=None):
        """
        删除已存在的键。不存在的 key 会被忽略
        return：
        被删除 key 的数量
        """
        if not keyname:
            return None

        keyname = self.key_make(keyname.strip())
        return self.obj_redis.delete(keyname)


    @wraps_set_expire
    def append(self, keyname=None, value=None):
        """
        为指定的 keyname 追加值
        如果 keyname 已经存在并且是一个字符串，
        APPEND 命令将 value 追加到 keyname 原来的值的末尾。
        如果 keyname 不存在，
        APPEND 就简单地将给定 keyname 设为 value ，就像执行 SET keyname value 一样
        return：
        追加指定值之后， keyname 中字符串的长度
        """
        if not keyname or value is None:
            return None

        keyname = self.key_make(keyname.strip())
        if isinstance(value, str):
            value = value.strip()
        else:
            value = str(value)

        return self.obj_redis.append(keyname, value)


    @wraps_set_expire
    def incr(self, keyname=None, expire=None):
        """
        将 keyname 中储存的数字值增一。
        如果 keyname 不存在，那么 key 的值会先被初始化为 0 ，然后再执行 INCR 操作。
        如果值包含错误的类型，或字符串类型的值不能表示为数字，那么返回一个错误。
        本操作的值限制在 64 位(bit)有符号数字表示之内。
        return：
        执行 INCR 命令之后 key 的值
        """
        if not keyname:
            return None

        keyname = self.key_make(keyname.strip())
        return self.obj_redis.incr(keyname, 1)


    @wraps_set_expire
    def incrBy(self, keyname=None, amount=1):
        """
        将 keyname 中储存的数字加上指定的增量值。
        如果 keyname 不存在，那么 key 的值会先被初始化为 0 ，然后再执行 INCRBY 命令
        如果值包含错误的类型，或字符串类型的值不能表示为数字，那么返回一个错误。
        本操作的值限制在 64 位(bit)有符号数字表示之内。
        return：
        加上指定的增量值之后， key 的值
        """
        if not keyname or not amount:
            return None

        keyname = self.key_make(keyname.strip())

        if isinstance(amount, int):
            amount = max(0, amount)
        else:
            amount = 1

        return self.obj_redis.incrby(keyname, amount)


    @wraps_set_expire
    def decr(self, keyname=None):
        """
        将 key 中储存的数字值减一。
        如果 key 不存在，那么 key 的值会先被初始化为 0 ，然后再执行 DECR 操作。
        如果值包含错误的类型，或字符串类型的值不能表示为数字，那么返回一个错误。
        本操作的值限制在 64 位(bit)有符号数字表示之内。
        return：
        执行命令之后 key 的值
        """
        if not keyname:
            return None

        keyname = self.key_make(keyname.strip())
        return self.obj_redis.decr(keyname, 1)


    @wraps_set_expire
    def decrBy(self, keyname=None, amount=1):
        """
        将 keyname 所储存的值减去指定的减量值。
        如果 keyname 不存在，那么 key 的值会先被初始化为 0 ，然后再执行 DECRBY 操作。
        如果值包含错误的类型，或字符串类型的值不能表示为数字，那么返回一个错误。
        本操作的值限制在 64 位(bit)有符号数字表示之内
        """
        if not keyname or not amount:
            return None

        keyname = self.key_make(keyname.strip())
        amount = int(amount)
        return self.obj_redis.decr(keyname, amount)


    # --------------------------------------------------------
    # Hash 哈希
    # 一个string类型的field和value的映射表，hash特别适合用于存储对象
    # 每个 hash 可以存储 232 - 1 键值对（40多亿）
    # --------------------------------------------------------
    

    @wraps_set_expire
    def hSet(self, keyname=None, key=None, value=None):
        """
        从哈希名为keyname中添加key1->value1 将哈希表key中的域field的值设为value。-ok -ok
        如果key不存在，一个新的哈希表被创建并进行hset操作。
        如果域field已经存在于哈希表中，旧值将被覆盖。
        错误则 返回 FALSE
        如果字段是哈希表中的一个新建字段，并且值设置成功，返回 1 。 
        如果哈希表中域字段已经存在且旧值已被新值覆盖，返回 0 。
        
        """
        if not keyname or not key or value is None:
            return None

        keyname = self.key_make(keyname.strip())
        key = key.strip()
        return self.obj_redis.hset(keyname, key, value)


    @wraps_set_expire
    def hGet(self, keyname=None, key=None):
        """
        获取存储在哈希表中指定字段的值
        返回给定字段的值。如果给定的字段或 key 不存在时，返回 None 
        """
        if not keyname or not key:
            return None

        keyname = self.key_make(keyname.strip())
        key = key.strip()
    
        result = self.obj_redis.hget(keyname, key)
        if not result:
            return None
        
        # bytes to str
        return bytes.decode(result)


    @wraps_set_expire
    def hLen(self, keyname=None):
        """
        获取哈希表中字段的数量
        哈希表中字段的数量。 当 keyname 不存在时，返回 0 
        """
        if not keyname:
            return None

        keyname = self.key_make(keyname.strip())
        return self.obj_redis.hlen(keyname)


    @wraps_set_expire
    def hKeys(self, keyname=None):
        """
        获取哈希表中的所有域（field）
        包含哈希表中所有域（field）列表。 
        当 key 不存在时，返回一个空列表
        """
        if not keyname:
            return None

        keyname = self.key_make(keyname.strip())
        result = self.obj_redis.hkeys(keyname)
        if not result:
            return None

        # bytes to str
        ret_list = list()
        for v in result:
            ret_list.append(bytes.decode(v))

        return ret_list


    @wraps_set_expire
    def hVals(self, keyname=None):
        """
        哈希表所有域(field)的值
        包含哈希表中所有域(field)值的列表。 
        当 key 不存在时，返回一个空表
        """
        if not keyname:
            return None

        keyname = self.key_make(keyname.strip())
        result = self.obj_redis.hvals(keyname)
        if not result:
            return None

        # bytes to str
        ret_list = list()
        for v in result:
            ret_list.append(bytes.decode(v))

        return ret_list


    @wraps_set_expire
    def hGetAll(self, keyname=None):
        """
        获取在哈希表中指定 keyname 的所有字段和值
        返回哈希表中，所有的字段和值
        在返回值里，紧跟每个字段名(field name)之后是字段的值(value)，
        所以返回值的长度是哈希表大小的两倍。
        """
        if not keyname:
            return None

        keyname = self.key_make(keyname.strip())
        result = self.obj_redis.hgetall(keyname)
        if not result:
            return None

        # bytes to str
        ret_dict = dict()
        for k, v in result.items():
            ret_dict[bytes.decode(k)] = bytes.decode(v)
            
        return ret_dict


    def hExists(self, keyname=None, key=None):
        """
        查看哈希表 keyname 中，是否存在键名为key的字段
        ashname含有给定字段key，返回 True。 
        keyname不存在 或 key 不存在，返回 False
        """
        if not keyname or key is None:
            return None

        keyname = self.key_make(keyname.strip())
        return self.obj_redis.hexists(keyname, key)


    def hDel(self, keyname=None, *keys):
        """
        删除哈希表 key 中的一个或多个指定字段，不存在的字段将被忽略
        返回值
        被成功删除字段的数量，不包括被忽略的字段
        keyname 或 key 不存在则返回 0
        """
        if not keyname:
            return None

        keyname = self.key_make(keyname.strip())
        return self.obj_redis.hdel(keyname, *keys)


    # --------------------------------------------------------
    # List 列表, 左(Left)为头部，右(Right)为尾部
    # 一个列表最多可以包含 232 - 1 个元素 (4294967295, 每个列表超过40亿个元素)
    # --------------------------------------------------------
    

    @wraps_set_expire
    def lPush(self, keyname=None, *values):
        """
        将一个或多个值插入到列表头部, 返回操作后列表的长度。
        如果 key 不存在，一个空列表会被创建并执行 LPUSH 操作。 
        当 key 存在但不是列表类型时，返回一个错误。
        注意：在Redis 2.4版本以前的 LPUSH 命令，都只接受单个 value 值
        """
        if not keyname:
            return None
        
        keyname = self.key_make(keyname.strip())
        return self.obj_redis.lpush(keyname, *values)

    
    @wraps_set_expire
    def lPop(self, keyname=None):
        """
        弹出队列头部元素,移除并返回列表的第一个元素。
        返回列表的第一个元素。 当列表 key 不存在时，返回 None 
        """
        if not keyname:
            return None

        keyname = self.key_make(keyname.strip())
        return self.obj_redis.lpop(keyname)


    @wraps_set_expire
    def rPush(self, keyname=None, *values):
        """
        将一个或多个值插入到列表的尾部(最右边), 返回操作后列表的长度。
        如果列表不存在，一个空列表会被创建并执行 RPUSH 操作。 
        当列表存在但不是列表类型时，返回一个错误。
        注意：在 Redis 2.4 版本以前的 RPUSH 命令，都只接受单个 value 值。
        
        """
        if not keyname:
            return None

        keyname = self.key_make(keyname.strip())
        return self.obj_redis.rpush(keyname, *values)

    
    @wraps_set_expire
    def rPop(self, keyname=None):
        """
        移除并获取列表最后一个元素
        返回列表的最后一个元素。 当列表不存在时，返回 None
        """
        if not keyname:
            return None

        keyname = self.key_make(keyname.strip())
        result = self.obj_redis.rpop(keyname)
        if not result:
            return None
        # bytes to str
        return bytes.decode(result)


    @wraps_set_expire
    def lLen(self, keyname=None):
        """
        获取列表长度 
        如果列表 key 不存在，则 key 被解释为一个空列表，返回 0  
        如果 key 不是列表类型，返回一个错误
        """
        if not keyname:
            return None
        
        keyname = self.key_make(keyname.strip())
        return self.obj_redis.llen(keyname)
    
    
    @wraps_set_expire
    def lTrim(self, keyname=None, start=0, end=-1):
        """
        让列表只保留指定区间内的元素，不在指定区间之内的元素都将被删除
        下标 0 表示列表的第一个元素，1 表示列表的第二个元素
        -1 表示列表的最后一个元素，-2 表示列表的倒数第二个元素
        返回 True
        """
        if not keyname:
            return None

        keyname = self.key_make(keyname.strip())
        return self.obj_redis.ltrim(keyname, start, end)


    @wraps_set_expire
    def lGetRange(self, keyname=None, start=0, end=-1):
        """
        返回列表中指定区间内的元素，区间以偏移量 START 和 END 指定
        下标 0 表示列表的第一个元素，以 1 表示列表的第二个元素
        -1 表示列表的最后一个元素， -2 表示列表的倒数第二个元素
        返回一个列表，包含指定区间内的元素
        """
        if not keyname:
            return None

        keyname = self.key_make(keyname.strip())
        result = self.obj_redis.lrange(keyname, start, end)
        if not result:
            return None
        #bytes to str
        ret_list = list()
        for v in result:
            ret_list.append(bytes.decode(v))

        return ret_list
    
    
    @wraps_set_expire
    def lRemove(self, keyname=None, value=None, count=1):
        """
        根据参数 COUNT 的值，移除列表中与参数 VALUE 相等的元素。
        COUNT 的值可以是以下几种：
        count > 0 : 从表头开始向表尾搜索，移除与 VALUE 相等的元素，数量为 COUNT 。
        count < 0 : 从表尾开始向表头搜索，移除与 VALUE 相等的元素，数量为 COUNT 的绝对值。
        count = 0 : 移除表中所有与 VALUE 相等的值。
        返回被移除元素的数量。 列表或元素不存在时返回 0
        """
        if not keyname or value is None:
            return None
        
        keyname = self.key_make(keyname.strip())
        return self.obj_redis.lrem(keyname, count, value)


    # --------------------------------------------------------
    # Set 无序集合
    # Set 是 String 类型的无序集合。集合成员是唯一的。
    # 集合是通过哈希表实现的，所以添加，删除，查找的复杂度都是 O(1)
    # 集合中最大的成员数为 232 - 1 (4294967295, 每个集合可存储40多亿个成员)
    # --------------------------------------------------------
    

    @wraps_set_expire
    def sAdd(self, keyname=None, *values):
        """
        将一个或多个成员元素加入到集合中，已经存在于集合的成员元素将被忽略。
        假如集合 key 不存在，则创建一个只包含添加的元素作成员的集合。
        当集合 key 不是集合类型时，返回一个错误。
        注意：在Redis2.4版本以前， SADD 只接受单个成员值。
        """
        if not keyname:
            return None
        keyname = self.key_make(keyname.strip())
        return self.obj_redis.sadd(keyname, *values)


    @wraps_set_expire
    def sCard(self, keyname=None):
        """
        获取集合key中元素的数量
        集合的数量。 当集合 key 不存在时，返回 0
        """
        if not keyname:
            return None
        keyname = self.key_make(keyname.strip())
        return self.obj_redis.scard(keyname)


    def sDiff(self, keyname=None, *keys):
        """
        差集
        返回所给key列表想减后的集合,相当于求差集
        不存在的集合 key 将视为空集。
        请注意顺序是前面的集合，减去后面的集合，求差集
        返回包含差集成员的列表
        
        """
        if not keyname:
            return None
        
        keyname = self.key_make(keyname.strip())
        
        other_keys = list()
        for k in keys:
            other_keys.append(self.key_make(k))

        result = self.obj_redis.sdiff(keyname, *other_keys)
        if not result:
            return None

        # bytes to str
        ret_set = set()
        for v in result:
            ret_set.add(bytes.decode(v))
 
        return ret_set


    @wraps_set_expire
    def sDiffStore(self, store_key=None, key=None, *keys):
        """
        差集并存储
        给定所有集合的差集并存储在 store_key 中
        将给定集合之间的差集存储在指定的集合中。
        如果指定的集合 key 已存在，则会被覆盖
        返回store_key结果集中的元素数量
        """
        if not store_key or not key:
            return None
        
        store_key = self.key_make(store_key.strip())
        key = self.key_make(key.strip())
        
        other_keys = list()
        for k in keys:
            other_keys.append(self.key_make(k))
        
        return self.obj_redis.sdiffstore(store_key, key, *other_keys)


    def sInter(self, keyname=None, *keys):
        """
        交集
        返回给定所有给定集合的交集。 不存在的集合 key 被视为空集。 
        当给定集合当中有一个空集或key不存在时，结果也为空集(根据集合运算定律)。
        """
        if not keyname:
            return None

        keyname = self.key_make(keyname.strip())

        other_keys = list()
        for k in keys:
            other_keys.append(self.key_make(k))

        result = self.obj_redis.sinter(keyname, *other_keys)
        if not result:
            return None

        # bytes to str
        ret_set = set()
        for v in result:
            ret_set.add(bytes.decode(v))

        return ret_set


    @wraps_set_expire
    def sInterStore(self, store_key=None, key=None, *keys):
        """
        交集并存储
        将给定集合之间的交集存储在指定的集合store_key中。
        如果指定的集合已经存在，则将其覆盖
        返回store_key存储交集的集合的元素数量
        """
        if not store_key or not key:
             return None
         
        store_key = self.key_make(store_key.strip())
        key = self.key_make(key.strip())

        other_keys = list()
        for k in keys:
            other_keys.append(self.key_make(k))

        return self.obj_redis.sinterstore(store_key, key, *other_keys)


    def sUnion(self, keyname=None, *keys):
        """
        并集
        所给key列表所有的值,相当于求并集
        给定集合的并集。不存在的集合 key 被视为空集。
        返回并集成员的列表
        """
        if not keyname:
         return None

        keyname = self.key_make(keyname.strip())

        other_keys = list()
        for k in keys:
            other_keys.append(self.key_make(k))

        result = self.obj_redis.sunion(keyname, *other_keys)
        if not result:
            return None

        # bytes to str
        ret_set = set()
        for v in result:
            ret_set.add(bytes.decode(v))

        return ret_set


    @wraps_set_expire
    def sUnionStore(self, store_key=None, key=None, *keys):
        """
        并集存储
        将给定集合的并集存储在指定的集合 store_key 中。
        如果 store_key 已经存在，则将其覆盖
        返回store_key存储并集的集合的元素数量
        """
        if not store_key or not key:
             return None
         
        store_key = self.key_make(store_key.strip())
        key = self.key_make(key.strip())

        other_keys = list()
        for k in keys:
            other_keys.append(self.key_make(k))

        return self.obj_redis.sunionstore(store_key, key, *other_keys)


    @wraps_set_expire
    def sIsMember(self, keyname=None, value=None):
        """
        判断成员元素是否是集合的成员
        如果成员元素是集合的成员，返回 True 
        如果成员元素不是集合的成员，或 key 不存在，返回 False
        """
        if not keyname or value is None:
            return None

        keyname = self.key_make(keyname.strip())
        return self.obj_redis.sismember(keyname, value)


    @wraps_set_expire
    def sMembers(self, keyname=None):
        """
        返回集合中的所有的成员。 
        不存在的集合 key 被视为空集合
        """
        if not keyname:
            return None
        
        keyname = self.key_make(keyname.strip())
        result = self.obj_redis.smembers(keyname)
        
        if not result:
            return None
        # bytes to str
        ret_set = set()
        for v in result:
            ret_set.add(bytes.decode(v))
            
        return ret_set


    @wraps_set_expire
    def sRem(self, keyname=None, *values):
        """
        删除该数组中对应的值
        移除集合中的一个或多个成员元素，不存在的成员元素会被忽略。
        当 key 不是集合类型，返回一个错误。
        在 Redis 2.4 版本以前， SREM 只接受单个成员值。
        返回被成功移除的元素的数量，不包括被忽略的元素
        """
        if not keyname:
            return None
        
        keyname = self.key_make(keyname.strip())
        return self.obj_redis.srem(keyname, *values)


    @wraps_set_expire
    def sPop(self, keyname=None):
        """
        移除并返回集合中的一个随机元素
        将随机元素从集合中移除并返回
        移除的随机元素。 当集合不存在或是空集时，返回 None
        """
        if not keyname:
            return None
        
        keyname = self.key_make(keyname.strip())
        result = self.obj_redis.spop(keyname)

        # bytes to str
        return None if not result else bytes.decode(result)


    @wraps_set_expire
    def sRandMember(self, keyname=None, count=1):
        """
        返回集合中的随机元素，而不对集合进行任何改动
        从 Redis 2.6 版本开始， Srandmember 命令接受可选的 count 参数：
        如果 count 为正数，且小于集合基数，
            返回一个包含 count 个元素的数组，数组中的元素各不相同。
        如果 count 大于等于集合基数，那么返回整个集合。
        如果 count 为负数，返回一个数组，
            数组中的元素可能会重复出现多次，而数组的长度为 count 的绝对值。
        返回：随机个数的元素列表
        """
        if not keyname:
            return None

        keyname = self.key_make(keyname.strip())
        
        if isinstance(count, int):
            count = max(0, count)
        else:
            count = 1
        
        result = self.obj_redis.srandmember(keyname, count)
        
        if not result:
            return None
        
        # bytes to str
        ret_list = list()
        for v in result:
            ret_list.append(bytes.decode(v))
            
        return ret_list


    # --------------------------------------------------------
    # Zset( sorted set ) 有序集合
    # 有序集合和集合一样也是string类型元素的集合,且不允许重复的成员
    # 有序集合的成员是唯一的,但分数(score)却可以重复
    # 集合是通过哈希表实现的，所以添加，删除，查找的复杂度都是O(1)
    # 集合中最大的成员数为 232 - 1 (4294967295, 每个集合可存储40多亿个成员)
    # --------------------------------------------------------

    @wraps_set_expire
    def zAdd(self, keyname=None, **kwargs):
        """
        将一个或多个成员元素及其分数值加入到有序集当中。
        如果某个成员已经是有序集的成员，那么更新这个成员的分数值，
        并通过重新插入这个成员元素，来保证该成员在正确的位置上。
        如果有序集合 key 不存在，则创建一个空的有序集并执行 ZADD 操作。
        当 key 存在但不是有序集类型时，返回一个错误。
        返回：
            被成功添加的新成员的数量，不包括那些被更新的、已经存在的成员。
        注意： 在 Redis 2.4 版本以前， ZADD 每次只能添加一个元素
        **kwargs： name1=score1, name2=score2
        """
        if not keyname:
            return None
        
        keyname = self.key_make(keyname.strip())
        return self.obj_redis.zadd(keyname, **kwargs)


    def zRangeByScore(self, keyname=None, min=None, max=None, withscores=False):
        """
        分数值正序
        返回有序集中指定分数区间内的所有的成员。
        有序集成员按分数值递减(从大到小)的次序排列。
        具有相同分数值的成员按字典序的逆序(reverse lexicographical order )排列
        返回；
        指定区间内，带有分数值(可选)的有序集成员的列表
        """
        if not keyname:
            return None

        keyname = self.key_make(keyname.strip())
        result = self.obj_redis.zrangebyscore(keyname, min, max, withscores=withscores)
        
        if not result:
            return None
        
        # bytes to str
        if not withscores:
            # return list
            zret = list()
            for field in result:
                zret.append(bytes.decode(field))
        else:
            # return dict
            zret = list()
            for field,score in result:
                zret.append((bytes.decode(field), score))
            zret =dict(zret)
            
        return zret
        

    def zRevRangeByScore(self, keyname=None, max=None, min=None, withscores=False):
        """
        分数值逆序
        返回有序集中指定分数区间内的所有的成员。
        有序集成员按分数值递减(从大到小)的次序排列。
        具有相同分数值的成员按字典序的逆序(reverse lexicographical order )排列。
        返回；
        指定区间内，带有分数值(可选)的有序集成员的列表
        """
        if not keyname:
            return None

        keyname = self.key_make(keyname.strip())
        result = self.obj_redis.zrevrangebyscore(keyname, max, min, withscores=withscores)

        if not result:
            return None

        # bytes to str
        if not withscores:
            # return list
            zret = list()
            for field in result:
                zret.append(bytes.decode(field))
        else:
            # return dict
            zret = list()
            for field,score in result:
                zret.append((bytes.decode(field), score))
            zret =dict(zret)
            
        return zret


    def zRank(self, keyname=None, member=None):
        """
        排名正序
        返回有序集中指定成员的排名。
        其中有序集成员按分数值递增(从小到大)顺序排列
        如果成员是有序集 key 的成员，返回 member 的排名。 
        如果成员不是有序集 key 的成员，返回 None 。
        """
        if not keyname or member is None:
            return None

        keyname = self.key_make(keyname.strip())
        return self.obj_redis.zrank(keyname, member)


    def zRevRank(self, keyname=None, member=None):
        """
        排名逆序
        返回有序集中指定成员的排名。
        其中有序集成员按分数值递减(从大到小)排序
        如果成员是有序集 key 的成员，返回 member 的排名。 
        如果成员不是有序集 key 的成员，返回 None 。
        """
        if not keyname or member is None:
            return None

        keyname = self.key_make(keyname.strip())
        return self.obj_redis.zrevrank(keyname, member)


    def zRange(self, keyname=None, start=None, end=None, withscores=False):
        """
        位置正序
        返回有序集中，指定区间内的成员。
        其中成员的位置按分数值递增(从小到大)来排序。
        具有相同分数值的成员按字典序(lexicographical order )来排列
        返回指定区间内，带有分数值(可选)的有序集成员的列表
        """
        if not keyname:
            return None

        keyname = self.key_make(keyname.strip())
        result = self.obj_redis.zrange(keyname, start, end, withscores=withscores)

        if not result:
            return None

        # bytes to str
        if not withscores:
            # return list
            zret = list()
            for field in result:
                zret.append(bytes.decode(field))
        else:
            # return dict
            zret = list()
            for field,score in result:
                zret.append((bytes.decode(field), score))
            zret =dict(zret)
            
        return zret


    def zRevrange(self, keyname=None, start=None, end=None, withscores=False):
        """
        位置逆序
        返回有序集中，指定区间内的成员。
        其中成员的位置按分数值递减(从大到小)来排列。
        具有相同分数值的成员按字典序的逆序(reverse lexicographical order)排列
        返回指定区间内，带有分数值(可选)的有序集成员的列表
        """
        if not keyname:
            return None

        keyname = self.key_make(keyname.strip())
        result = self.obj_redis.zrevrange(keyname, start, end, withscores=withscores)

        if not result:
            return None

        # bytes to str
        if not withscores:
            # return list
            zret = list()
            for field in result:
                zret.append(bytes.decode(field))
        else:
            # return dict
            zret = list()
            for field,score in result:
                zret.append((bytes.decode(field), score))
            zret =dict(zret)
            
        return zret


    def zRem(self, keyname, *member):
        """
        移除有序集中的一个或多个成员，不存在的成员将被忽略。
        当 key 存在但不是有序集类型时，返回一个错误。
        注意： 在 Redis 2.4 版本以前， ZREM 每次只能删除一个元素。
        返回被成功移除的成员的数量，不包括被忽略的成员0
        """
        if not keyname:
            return None

        keyname = self.key_make(keyname.strip())
        return self.obj_redis.zrem(keyname, *member)


    def zRemRangeByRank(self, keyname=None, min=None, max=None):
        """
        删除正序
        移除有序集中，指定排名(rank)区间内的所有成员
        返回被移除成员的数量
        """
        if not keyname:
            return None

        keyname = self.key_make(keyname.strip())
        return self.obj_redis.zremrangebyrank(keyname, min, max)


    def zRemrangebyscore(self, keyname=None, min=None, max=None):
        """
        删除正序
        移除有序集中，指定分数（score）区间内的所有成员
        返回被移除成员的数量
        """
        if not keyname:
            return None

        keyname = self.key_make(keyname.strip())
        return self.obj_redis.zremrangebyscore(keyname, min, max)


    def zCard(self, keyname=None):
        """
        计算集合中元素的数量
        当 key 存在且是有序集类型时，返回有序集的基数。 
        当 key 不存在时，返回 0
        """
        if not keyname:
            return None

        keyname = self.key_make(keyname.strip())
        return self.obj_redis.zcard(keyname)


    def zCount(self, keyname=None, min=None, max=None):
        """
        计算有序集合中指定分数区间的成员数量
        返回分数值在 min 和 max 之间的成员的数量
        """
        if not keyname:
            return None

        keyname = self.key_make(keyname.strip())
        return self.obj_redis.zcount(keyname, min, max)
