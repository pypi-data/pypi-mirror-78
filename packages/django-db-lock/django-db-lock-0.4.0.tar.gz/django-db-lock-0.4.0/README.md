# django-db-lock

Lock something and keep status in database. A simple distributed lock system.

## Install

```shell
pip install django-db-lock
```

## Usage With django_db_lock app in project

**pro/settings.py**

```
INSTALLED_APPS = [
    ...
    'django_db_lock',
    'django.contrib.humanize',
    ...
]

DJANGO_DB_LOCK_AUTO_REGISTER_MODEL = True
DJANGO_DB_LOCK_AUTO_REGISTER_ADMIN = True
DJANGO_DB_LOCK_AUTO_REGISTER_SERVICES = True
DJANGO_DB_LOCK_APP_LABEL = "django_db_lock"
```

- Required.
- Insert `django_db_lock` into INSTALLED_APPS.
- Insert `django.contrib.humanize` into INSTALLED_APPS to enable the i18n translation.
- DJANGO_DB_LOCK_AUTO_REGISTER_MODEL default to True, so that the Lock model is auto registerd.
- DJANGO_DB_LOCK_AUTO_REGISTER_ADMIN default to True, so that the Lock model's admin site is auto registered.
- DJANGO_DB_LOCK_AUTO_REGISTER_SERVICES default to True, so that the Lock Services is auto registered in django_db_lock.urls.
- DJANGO_DB_LOCK_APP_LABEL default to django_db_lock, so that the Lock model is registered under django_db_lock. You can change it to any exists app.

**pro/urls.py**

```
...
from django.urls import path
from django.urls import include

urlpatterns = [
    ...
    path('dblock/', include("django_db_lock.urls")),
    ...
]
```

- Optional.
- Export db-lock services only if you have client app to use the service.

**app/views.py**

```
import uuid
from django_db_lock.client import get_default_lock_server
from django_db_lock.client import DjangoDbLock

def view01(request):
    lock_server = get_default_lock_server()
    lock_name = "view01lock"
    worker_name = "view01worker"
    timeout = 10
    with DjangoDbLock(lock_server, lock_name, worker_name, timeout) as locked:
        if locked:
            do_something...
    ...
```

##  Usage Without django_db_lock app in project 

**pro/settings.py**

```
DJANGO_DB_LOCK_AUTO_REGISTER_MODEL = False
DJANGO_DB_LOCK_AUTO_REGISTER_ADMIN = False
DJANGO_DB_LOCK_AUTO_REGISTER_SERVICES = False
DJANGO_DB_LOCK_API_SERVER = **You api server**
DJANGO_DB_LOCK_ACQUIRE_LOCK_PATH = "acquireLock"
DJANGO_DB_LOCK_RELEASE_LOCK_PATH = "releaseLock"

```

- You must set DJANGO_DB_LOCK_AUTO_REGISTER_MODEL to False, so that you will not get django_db_model's Lock model auto registered.
- You must set DJANGO_DB_LOCK_API_SERVER in your settings.py
- DJANGO_DB_LOCK_ACQUIRE_LOCK_PATH default to "acquireLock". Only if your server have changed the url, you have to change it to match the server.
- DJANGO_DB_LOCK_RELEASE_LOCK_PATH default to "releaseLock". Only if your server have changed the url, you have to change it to match the server.

**app/views.py**

```
import uuid
from django_db_lock.client import get_default_lock_server
from django_db_lock.client import DjangoDbLock

def view01(request):
    lock_server = get_default_lock_server()
    lock_name = "view01lock"
    worker_name = "view01worker"
    timeout = 10
    with DjangoDbLock(lock_server, lock_name, worker_name, timeout) as locked:
        if locked:
            do_something...
    ...
```


## Releases

### v0.4.0 2020/09/08

- Add abstract LockBase model.
- Add django_db_lock.client module.
- Put services in one class, so that you may create many lock server instance.

### v0.3.1 2020/09/01

- Rename zh_hans to zh_Hans.
- Fix setup descriptions.

### v0.3.0 2020/09/01

- Add django_db_lock.client.DjangoDbLock.

### v0.2.1 2020/08/29

- Fix setup description.

### v0.2.0 2020/08/29

- Reconstituted.
- Allow register the Lock model into another app, use setting DJANGO_DB_LOCK_APP_LABEL.
- Use django-apiview to provides restful API.
- Use camelStyle parameter format.
- Add i18n for zh-hans.
- Incompatible with old releases.

### v0.1.1 2018/5/11

- Fix.

### v0.1.0 2018/5/10

- First release.
