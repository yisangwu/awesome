"""
redis 的实例化
"""
from awesome.library.lib_redis import LibRedis
from awesome.config import redis


obj_rd_window = LibRedis(
                            host=redis.rd_window[0],
                            port=redis.rd_window[1],
                            db=redis.rd_window[2],
                            prefix = 'window_'
                        )

obj_rd_one = LibRedis(
                            host=redis.rd_one[0],
                            port=redis.rd_one[1],
                            db=redis.rd_one[2]
                        )

obj_rd_two = LibRedis(
                            host=redis.rd_two[0],
                            port=redis.rd_two[1],
                            db=redis.rd_two[2]
                        )

obj_rd_three = LibRedis(
                            host=redis.rd_three[0],
                            port=redis.rd_three[1],
                            db=redis.rd_three[2]
                        )


