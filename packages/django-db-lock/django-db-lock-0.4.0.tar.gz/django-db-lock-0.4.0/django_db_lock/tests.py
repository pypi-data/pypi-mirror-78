import time
import json
from django.test import TestCase
from django.test import Client
from django.urls import reverse_lazy as reverse
from django_db_lock.server import django_db_lock_default_server

class TestDjangoDbLock(TestCase):

    def setUp(self):
        self.url_acquire_lock = reverse("django_db_lock.acquireLock")
        self.url_release_lock = reverse("django_db_lock.releaseLock")
        self.url_get_lock_info = reverse("django_db_lock.getLockInfo")
        self.url_clear_expired_locks = reverse("django_db_lock.clearExpiredLocks")
        self.browser = Client()

    def test01(self):
        assert django_db_lock_default_server.acquire_lock("lock01", "worker01", 100)
        assert django_db_lock_default_server.acquire_lock("lock01", "worker01", 100) == False
        assert django_db_lock_default_server.release_lock("lock01", "worker01")

    def test02(self):
        assert django_db_lock_default_server.acquire_lock("lock01", "worker01", 1)
        time.sleep(2)
        assert django_db_lock_default_server.acquire_lock("lock01", "worker01", 1)

    def test03(self):
        assert django_db_lock_default_server.acquire_lock("lock01", "worker01", 100)
        assert django_db_lock_default_server.release_lock("lock01", "worker01")
        assert django_db_lock_default_server.release_lock("lock01", "worker01")

    def test04(self):
        django_db_lock_default_server.acquire_lock("lock01", "worker01", 100)
        info = django_db_lock_default_server.get_lock_info("lock01")
        assert info["lockName"] == "lock01"
        assert info["workerName"] == "worker01"

    def test05(self):
        browser = Client()
        response = browser.get(self.url_acquire_lock, {"lockName": "lock01", "workerName": "worker01", "timeout": 300})
        data = json.loads(response.content)
        assert data["result"]

        browser = Client()
        response = browser.get(self.url_acquire_lock, {"lockName": "lock01", "workerName": "worker01", "timeout": 300})
        data = json.loads(response.content)
        assert data["result"] is False

        browser = Client()
        response = browser.get(self.url_get_lock_info, {"lockName": "lock01"})
        data = json.loads(response.content)
        assert data["result"]
        assert data["result"]["lockName"] == "lock01"

        browser = Client()
        response = browser.get(self.url_release_lock, {"lockName": "lock01", "workerName": "worker01"})
        data = json.loads(response.content)
        assert data["result"]

    def test09(self):
        browser = Client()
        response = browser.get(self.url_clear_expired_locks)
        data = json.loads(response.content)
        assert data["result"]
