from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('subject/list/', views.subject_list_page, name='subject_list'),
    path('subject/create/', views.subject_update_page, name='subject_create'),
    path('subject/remove/<int:subject_id>/', views.subject_remove_page, name='subject_remove'),
    path('subject/update/<int:subject_id>/', views.subject_update_page, name='subject_update'),
    re_path(r'^w/(?P<year>[0-9]{4})-(?P<month>[0-9]{1,2})-(?P<day>[0-9]{1,2})/$', views.week, name='week'),
]
