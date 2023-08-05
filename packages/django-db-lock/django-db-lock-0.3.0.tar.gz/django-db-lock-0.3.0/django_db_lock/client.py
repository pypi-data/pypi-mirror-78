from . import services



class DjangoDbLock(object):
    def __init__(self, lock_name, worker_name, timeout):
        self.lock_name = lock_name
        self.worker_name = worker_name
        self.timeout = timeout
    
    def __enter__(self):
        self.locked = services.acquire_lock(self.lock_name, self.worker_name, self.timeout)
        return self.locked
    
    def __exit__(self, type, value, traceback):
        if self.locked:
            services.release_lock(self.lock_name, self.worker_name)
