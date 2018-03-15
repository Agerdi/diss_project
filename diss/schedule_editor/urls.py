from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),

    path('teacher/list/', views.teacher_list_page, name='teacher_list'),
    path('teacher/create/', views.teacher_update_page, name='teacher_create'),
    path('teacher/update/<int:teacher_id>/', views.teacher_update_page, name='teacher_update'),

    path('room/list/', views.room_list_page, name='room_list'),
    path('room/create/', views.room_update_page, name='room_create'),
    path('room/update/<int:room_id>/', views.room_update_page, name='room_update'),

    path('group/list/', views.group_list_page, name='group_list'),
    path('group/create/', views.group_update_page, name='group_create'),
    path('group/update/<int:group_id>/', views.group_update_page, name='group_update'),

    path('semester/list/', views.semester_list_page, name='semester_list'),
    path('semester/create/', views.semester_update_page, name='semester_create'),
    path('semester/update/<int:semester_id>/', views.semester_update_page, name='semester_update'),

    path('subject/group/', views.subject_group_page, name='subject_group'),
    path('subject/list/<int:group_id>/', views.subject_list_page, name='subject_list'),
    path('subject/create/', views.subject_update_page, name='subject_create'),
    path('subject/update/<int:subject_id>/', views.subject_update_page, name='subject_update'),

    re_path(r'^w/(?P<year>[0-9]{4})-(?P<month>[0-9]{1,2})-(?P<day>[0-9]{1,2})/$', views.week, name='week'),
]
