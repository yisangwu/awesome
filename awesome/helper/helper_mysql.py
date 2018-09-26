"""
awesome.helper
Mysql 帮助类
"""
import sys


def gen_multi_model(cls):
    """
    Mysql自动分表,
    自动在cls所在的module里面生成cls.table_piece_number个model
    :param cls:
    :return:
    """
    module = sys.modules[cls.__module__]
    if not cls.table_piece_number:
        return None

    tpl_module = cls.__module__
    tpl_class_name = cls.__name__
    tpl_table_name = None
    tpl_tb_desc = None

    # 遍历创建多表
    for piece in range(cls.table_piece_number):
        # 类名
        if not tpl_class_name:
            tpl_class_name = cls.__name__
        cls_name = tpl_class_name + str(piece)
        # 模板表的表名
        if not tpl_table_name:
            tpl_table_name = cls._meta.db_table
        # 模板表的描述名
        if not tpl_tb_desc:
            tpl_tb_desc = cls._meta.verbose_name

        class MetaNew:
            """
            重定义多表的Mata
            """
            abstract = False  # 非抽象类，要创建表
            db_table = '%s%s' % (tpl_table_name, piece)  # 表名，加后缀
            verbose_name = verbose_name_plural = u"%s(%s)" % (tpl_tb_desc, piece)  # 表描述名，加后缀

        attrs = {
            '__module__': tpl_module,
            'Meta': MetaNew,
        }
        cls_obj = type(cls_name, (cls, ), attrs)
        setattr(module, cls_obj.__name__, cls_obj)

    return cls


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    from collections import namedtuple
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]
