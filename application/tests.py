from django.test import TestCase

# Create your tests here.
from awesome.loader import loader_redis

print(loader_redis.obj_rd_window.set('xx',1))

print(loader_redis.obj_rd_window.append('xx',2))

print(loader_redis.obj_rd_window.get('xx'))

print(loader_redis.obj_rd_window.incr('xx'))

print(loader_redis.obj_rd_window.incrby('xx',9))

print(loader_redis.obj_rd_window.decr('xx'))

print(loader_redis.obj_rd_window.decrby('xx',9))

print(loader_redis.obj_rd_window.delete('xx'))
