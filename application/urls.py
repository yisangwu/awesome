from django.urls import include, path
from . import views, view_uid

urlpatterns = [
    path('', views.index),
    # ex: /application/
    path('', views.index, name='index'),
    # ex: /application/first/
    path('first', views.first, name='first'),
    # ex: /application/first/
    path('first', views.first, name='first'),
    
    # ex: /application/get_one
    path('get_one', views.get_one, name='get_one'),
    # ex: /application/get_all
    path('get_all', views.get_all, name='get_all'),
    # ex: /application/insert_one
    path('insert_one', views.insert_one, name='insert_one'),
    # ex: /application/insert_all
    path('insert_all', views.insert_all, name='insert_all'),


    # ex: /application/5/
    path('<int:id>/', views.detail, name='detail'),
    # ex: /application/5/results/
    path('<int:id>/results/', views.results, name='results'),
    # ex: /application/5/vote/
    path('<int:id>/vote/', views.vote, name='vote'),
    #
    path('uid', view_uid.index, name='do_uid')
]
