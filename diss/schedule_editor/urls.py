from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^w/(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})/$', views.week, name='week'),

]