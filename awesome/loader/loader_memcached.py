"""
Memcached 的实例化
"""
from awesome.config import memcached
from awesome.library.lib_memcached import LibMemcached


one = LibMemcached(
                        host=memcached.mem_one[0],
                        port=memcached.mem_one[1],
                    )