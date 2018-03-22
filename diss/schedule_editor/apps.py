from django.apps import AppConfig
from django.db.models.signals import post_save


def create_events_for_subject_class(sender, instance, created, raw, update_fields, **kwargs):
    from . import models
    already_created = models.Event.objects.filter()


class ScheduleEditorConfig(AppConfig):
    name = 'schedule_editor'

    def ready(self):
        post_save.connect(create_events_for_subject_class, sender='schedule_editor.SubjectClass')
