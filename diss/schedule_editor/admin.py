from django.contrib import admin

from schedule_editor import models

admin.site.register(models.Subject)
admin.site.register(models.SubjectClass)
admin.site.register(models.StudentGroup)
admin.site.register(models.Room)
admin.site.register(models.Teacher)
admin.site.register(models.Event)
admin.site.register(models.Semester)
