from django.conf import settings

DJANGO_DB_LOCK_AUTO_REGISTER_ADMIN = getattr(settings, "DJANGO_DB_LOCK_AUTO_REGISTER_ADMIN", True)
DJANGO_DB_LOCK_APP_LABEL = getattr(settings, "DJANGO_DB_LOCK_APP_LABEL", "django_db_lock")
