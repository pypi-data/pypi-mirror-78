import datetime

from django.urls import path
from django.utils import timezone
from django.db.utils import IntegrityError
from django.db import transaction

from django_apiview.views import apiview

from . import settings


class DjangoDbLockServer(object):

    def __init__(self, model):
        self.model = model

    def clear_expired_locks(self):
        now_time = timezone.now()
        with transaction.atomic():
            self.model.objects.filter(expire_time__lte=now_time).delete()

    def acquire_lock(self, lock_name, worker_name, timeout):
        self.clear_expired_locks()
        lock = self.model()
        lock.lock_name = lock_name
        lock.worker_name = worker_name
        lock.lock_time = timezone.now()
        lock.expire_time = lock.lock_time + datetime.timedelta(seconds=timeout)
        try:
            with transaction.atomic():
                lock.save()
            return True
        except IntegrityError:
            return False

    def release_lock(self, lock_name, worker_name):
        self.clear_expired_locks()
        try:
            lock = self.model.objects.get(lock_name=lock_name, worker_name=worker_name)
            with transaction.atomic():
                lock.delete()
            return True
        except self.model.DoesNotExist:
            return True
        return False

    def get_lock_info(self, lock_name):
        try:
            lock = self.model.objects.get(lock_name=lock_name)
            return {
                "pk": lock.pk,
                "lockName": lock.lock_name,
                "workerName": lock.worker_name,
                "lockTime": lock.lock_time,
                "expireTime": lock.expire_time,
            }
        except self.model.DoesNotExist:
            return None

    def get_urls(self, prefix="django_db_lock"):
        return [
            path('acquireLock', self.getAcquireLockView(), name=prefix + ".acquireLock"),
            path('releaseLock', self.getReleaseLockView(), name=prefix + ".releaseLock"),
            path('getLockInfo', self.getGetLockInfoView(), name=prefix + ".getLockInfo"),
            path('clearExpiredLocks', self.GetClearExpiredLocksView(), name=prefix + ".clearExpiredLocks"),
        ]

    def getAcquireLockView(self):
        @apiview
        def acquireLock(lockName, workerName, timeout:int):
            result = self.acquire_lock(lockName, workerName, timeout)
            return result
        return acquireLock

    def getReleaseLockView(self):
        @apiview
        def releaseLock(lockName, workerName):
            result = self.release_lock(lockName, workerName)
            return result
        return releaseLock

    def getGetLockInfoView(self):
        @apiview
        def getLockInfo(lockName):
            info = self.get_lock_info(lockName)
            return info
        return getLockInfo

    def GetClearExpiredLocksView(self):
        @apiview
        def clearExpiredLocks():
            self.clear_expired_locks()
            return True
        return clearExpiredLocks

if settings.DJANGO_DB_LOCK_AUTO_REGISTER_SERVICES and settings.DJANGO_DB_LOCK_AUTO_REGISTER_MODEL:
    from .models import Lock
    django_db_lock_default_server = DjangoDbLockServer(Lock)
