# tracker/apps.py
from django.apps import AppConfig


class TrackerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tracker"

    def ready(self):
        # This import is required to register the signal handlers
        # The pylance warning can be safely ignored
        from . import signals  # pylint: disable=import-outside-toplevel, unused-import
