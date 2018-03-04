from django.contrib import admin

from schedule_editor import models

admin.site.register(models.Discipline)
admin.site.register(models.Group)
admin.site.register(models.Student)
admin.site.register(models.Room)
admin.site.register(models.Teacher)
admin.site.register(models.Event)

