from django.shortcuts import render
from django.http import HttpResponse
from application.app_models.models_golbaluid import AppGlobalId


def index(request):
    """
    index
    :param request:
    :return:
    """
    resp_str = list()
    tpl_string = 'new uid is:{uu}, create time:{tt}\r\n'
    for i in range(20):
        uid = AppGlobalId.get_new_uid()
        resp_str.append(tpl_string.format(uu=uid, tt='xxxoss'))

    return HttpResponse(resp_str)
