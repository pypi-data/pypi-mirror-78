from . import settings

if settings.DJANGO_DB_LOCK_AUTO_REGISTER_ADMIN and settings.DJANGO_DB_LOCK_AUTO_REGISTER_MODEL:
    default_app_config = "django_db_lock.apps.DjangoDbLockConfig"

