from django.contrib import admin
from django.urls import path, re_path, register_converter
from . import views, converters

register_converter(converters.IntConverter, 'myint')
register_converter(converters.FourDigitYearConverter, 'yyyy')
urlpatterns = [
    path('', views.index),
    path('<int:year>', views.year),
    path('<int:year>/<str:name>', views.name),
    # re_path('(?P<year>[0-9]{4}).html', views.myyear, name='urlyear'),
    # re_path('(?P<year>[0-9]{4}).html', admin.site.urls, name='urlyear'),
    path('<myint:year>', views.year),  # 自定义过滤器filter
    path('<yyyy:year>', views.year),
    path('films', views.films),
]