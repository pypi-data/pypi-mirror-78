from django_apiview.views import apiview
from .services import acquire_lock as do_acquire_lock
from .services import release_lock as do_release_lock
from .services import get_lock_info as do_get_lock_info
from .services import clear_expired_locks as do_clear_expired_locks


@apiview
def acquireLock(lockName, workerName, timeout:int):
    result = do_acquire_lock(lockName, workerName, timeout)
    return result


@apiview
def releaseLock(lockName, workerName):
    result = do_release_lock(lockName, workerName)
    return result


@apiview
def getLockInfo(lockName):
    info = do_get_lock_info(lockName)
    return info


@apiview
def clearExpiredLocks():
    do_clear_expired_locks()
    return True
