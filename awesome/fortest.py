
import sys
import os

sys.path.insert(0, '../')


#from awesome.loader import loader_redis

#print(loader_redis.obj_rd_window.set('xx',1))
#
#print(loader_redis.obj_rd_window.append('xx',2))
#
#print(loader_redis.obj_rd_window.get('xx'))

#print(loader_redis.obj_rd_window.incr('xx'))
#
#print(loader_redis.obj_rd_window.get('xx'))
#
#print(loader_redis.obj_rd_window.incrBy('xx',9))
#
#print(loader_redis.obj_rd_window.get('xx'))
#
#print(loader_redis.obj_rd_window.decr('xx'))
#
#print(loader_redis.obj_rd_window.decrBy('xx',9))
##
#print(loader_redis.obj_rd_window.delete('xx'))

#print(loader_redis.obj_rd_window.hSet('xx','a',1))
#print(loader_redis.obj_rd_window.hSet('xx','b',2))
#print(loader_redis.obj_rd_window.hSet('xx','b',33))
#print(loader_redis.obj_rd_window.hGet('xx','a'))
#print(loader_redis.obj_rd_window.hGet('xx','b'))
#print(loader_redis.obj_rd_window.hGet('xx','xx'))
#print(loader_redis.obj_rd_window.hLen('xxss'))
#print(loader_redis.obj_rd_window.hDel('xx','a','b'))

#print(loader_redis.obj_rd_window.hKeys('xx'))
#print(loader_redis.obj_rd_window.hVals('xx'))
#print(loader_redis.obj_rd_window.hGetAll('xx'))
#xx = loader_redis.obj_rd_window.hGetAll('xx')
#print(xx)
##print(xx['a'],xx['b'])
##print(list(xx.keys()))
#print(loader_redis.obj_rd_window.hExists('xx','a'))
#print(loader_redis.obj_rd_window.hExists('xx','xxxx'))

#----------- List -------------------
#print(loader_redis.obj_rd_window.lPush('xx',1,2,3,4,5))
#print(loader_redis.obj_rd_window.rPush('xx','a','b','c'))
#
#print(loader_redis.obj_rd_window.lPop('xx'))
#print(loader_redis.obj_rd_window.lLen('xx'))
#print(loader_redis.obj_rd_window.lTrim('ssassssxx', 1, 4))
#print(loader_redis.obj_rd_window.lGetRange('xx'))
#print(loader_redis.obj_rd_window.lRemove('xx',222,1))

#----------- Set ------------------
#print(loader_redis.obj_rd_window.sAdd('xx',1,2,3))
#print(loader_redis.obj_rd_window.sAdd('yy',1,4,5))
#print(loader_redis.obj_rd_window.sAdd('zz',1,2,6))
#print(loader_redis.obj_rd_window.sCard('xx'))
#print(loader_redis.obj_rd_window.sDiff('xx', 'yy' ,'zz'))
#print(loader_redis.obj_rd_window.sDiffStore('aa', 'xx', 'yy' ,'zz'))
#print(loader_redis.obj_rd_window.sInter('xx', 'yy', 'zz'))
#print(loader_redis.obj_rd_window.sInterStore('aa','xx', 'yy', 'zz'))
#print(loader_redis.obj_rd_window.sUnion('xx', 'yy', 'zz'))
#print(loader_redis.obj_rd_window.sUnionStore('aa','xx', 'yy', 'zz'))
#print(loader_redis.obj_rd_window.sIsMember('xx',1))
#print(loader_redis.obj_rd_window.sIsMember('xx',123))
#print(loader_redis.obj_rd_window.sMembers('xx'))
#print(loader_redis.obj_rd_window.sRem('xx',8,9))
#print(loader_redis.obj_rd_window.sPop('xx'))
#print(loader_redis.obj_rd_window.sRandMember('xx'))
#print(loader_redis.obj_rd_window.sRandMember('xx',2))

#--------- Zset ---------------------
#print(loader_redis.obj_rd_window.zAdd('xx',a=1,b=2,c=3))
#print(loader_redis.obj_rd_window.zRangeByScore('xx', 0, 999))
#print(loader_redis.obj_rd_window.zRangeByScore('xx', 0, 999, True))
#
#print(loader_redis.obj_rd_window.zRevRangeByScore('xx', 999, 0))
#print(loader_redis.obj_rd_window.zRevRangeByScore('xx', 999, 0, True))
#print(loader_redis.obj_rd_window.zRank('xx','a'))
#print(loader_redis.obj_rd_window.zRank('xx','b'))
#print(loader_redis.obj_rd_window.zRank('xx','sss'))
#
#print(loader_redis.obj_rd_window.zRevRank('xx','a'))
#print(loader_redis.obj_rd_window.zRevRank('xx','b'))
#print(loader_redis.obj_rd_window.zRevRank('xx','sss'))

#print(loader_redis.obj_rd_window.zRange('xx',0,-1, True))
##print(loader_redis.obj_rd_window.zRevrange('xx', 0, -1, True))
#print(loader_redis.obj_rd_window.zRem('xx', 'a'))

#print(loader_redis.obj_rd_window.zRemRangeByRank('xx', 0,1))
#print(loader_redis.obj_rd_window.zRemrangebyscore('xx', 22,33))
#print(loader_redis.obj_rd_window.zCard('xx'))
#print(loader_redis.obj_rd_window.zCount('xx',11,99))
#---------- Memcached ---------------

#from awesome.loader import loader_memcached
#
#print(loader_memcached.one.set('xx',1))
#print(loader_memcached.one.get('xx'))
#print(loader_memcached.one.append('xx','23456789'))
#print(loader_memcached.one.get('xx'))
#print(loader_memcached.one.prepend('xx','99'))
#
#print(loader_memcached.one.get('xx'))