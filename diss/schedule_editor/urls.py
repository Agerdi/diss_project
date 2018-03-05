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

    path('room/list/', views.room_list_page, name='room_list'),
    path('room/create/', views.room_update_page, name='room_create'),
    path('room/update/<int:room_id>/', views.room_update_page, name='room_update'),

    path('student_group/list/', views.student_group_list_page, name='student_group_list'),
    path('student_group/create/', views.student_group_update_page, name='student_group_create'),
    path('student_group/update/<int:student_group_id>/', views.student_group_update_page, name='student_group_update'),

    path('semester/list/', views.semester_list_page, name='semester_list'),
    path('semester/create/', views.semester_update_page, name='semester_create'),
    path('semester/update/<int:semester_id>/', views.semester_update_page, name='semester_update'),

    re_path(r'^w/(?P<year>[0-9]{4})-(?P<month>[0-9]{1,2})-(?P<day>[0-9]{1,2})/$', views.week, name='week'),
]
