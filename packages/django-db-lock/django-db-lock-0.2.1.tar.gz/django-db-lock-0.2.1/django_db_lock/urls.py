from django.urls import path
from . import views


urlpatterns = [
    path('acquireLock', views.acquireLock, name="django_db_lock.acquireLock"),
    path('releaseLock', views.releaseLock, name="django_db_lock.releaseLock"),
    path('getLockInfo', views.getLockInfo, name="django_db_lock.getLockInfo"),
    path('clearExpiredLocks', views.clearExpiredLocks, name="django_db_lock.clearExpiredLocks"),
]
