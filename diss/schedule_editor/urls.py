from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('subject/list/', views.subject_list_page, name='subject_list'),
    path('subject/create/', views.subject_update_page, name='subject_create'),
    path('subject/update/<int:subject_id>/', views.subject_update_page, name='subject_update'),

    path('teacher/list/', views.teacher_list_page, name='teacher_list'),
    path('teacher/create/', views.teacher_update_page, name='teacher_create'),
    path('teacher/update/<int:teacher_id>/', views.teacher_update_page, name='teacher_update'),

    re_path(r'^w/(?P<year>[0-9]{4})-(?P<month>[0-9]{1,2})-(?P<day>[0-9]{1,2})/$', views.week, name='week'),
]
