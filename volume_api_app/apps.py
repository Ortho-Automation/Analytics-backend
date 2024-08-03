from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.contrib.auth import get_user_model
from django.conf import settings


class VolumeApiAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "volume_api_app"  # Ensure this matches the directory name
    label = "volume_api_app"

    def ready(self):
        post_migrate.connect(create_default_superuser, sender=self)


def create_default_superuser(sender, **kwargs):
    User = get_user_model()
    if not User.objects.filter(username=settings.DEFAULT_ADMIN_USERNAME).exists():
        User.objects.create_superuser(
            username=settings.DEFAULT_ADMIN_USERNAME,
            email=settings.DEFAULT_ADMIN_EMAIL,
            password=settings.DEFAULT_ADMIN_PASSWORD,
        )
