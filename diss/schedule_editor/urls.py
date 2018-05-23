from django.urls import path, re_path

from . import views, filters

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),

    path('teacher/', views.teacher_list_page, name='teacher_list'),
    path('teacher/new/', views.teacher_update_page, name='teacher_create'),
    path('teacher/<int:teacher_id>/', views.teacher_update_page, name='teacher_update'),

    path('room/', views.room_list_page, name='room_list'),
    path('room/new/', views.room_update_page, name='room_create'),
    path('room/<int:room_id>/', views.room_update_page, name='room_update'),

    path('semester/', views.semester_list_page, name='semester_list'),
    path('semester/new/', views.semester_update_page, name='semester_create'),
    path('semester/<int:semester_id>/', views.semester_update_page, name='semester_update'),

    path('group/', views.group_list_page, name='group_list'),
    path('group/new/', views.group_update_page, name='group_create'),
    path('group/<int:group_id>/', views.group_update_page, name='group_update'),

    path('group/subject/', views.subject_group_page, name='subject_group'),
    path('group/<int:group_id>/subject/', views.subject_list_page, name='subject_list'),
    path('group/<int:group_id>/subject/new/', views.subject_update_page, name='subject_create'),
    path('group/<int:group_id>/subject/<int:subject_id>/', views.subject_update_page, name='subject_update'),

    path('subject/<int:subject_id>/class/new/', views.subject_class_page, name='class_create'),
    path('subject/<int:subject_id>/class/delete/<int:class_id>/', views.subject_class_delete, name='class_delete'),
    path('subject/<int:subject_id>/class/<int:class_id>/', views.subject_class_page, name='class_update'),

    re_path(r'^w/(?P<year>[0-9]{4})-(?P<month>[0-9]{1,2})-(?P<day>[0-9]{1,2})/$', views.week, name='week'),
]
