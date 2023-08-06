# django-server-controller

Django server controllers, e.g. UwsgiController.

## Install

```shell
pip install django-server-controller
```

## Examples

**pro/settings.py**

```
INSTALLED_APPS = [
    ...
    'django_server_controller',
    ...
]
```

## wsgi.ini file paths

1. settings.UWSGI_INI_FILE pointed file.
1. ./etc/wsgi.ini
1. ./lib/python3.6/site-packages/the_project_package/wsgi.ini


**Chrooted to PROJECT_BASE before find wsgi.ini**


## Suggest project folders

```
./bin/
./etc/
./lib/
./lib64/
./web/
./web/static/
./web/upload/
./logs/
```

- bin/lib/lib64 folders are created by virutalenv.
- etc/web/logs folders are ours.

## Releases

### v0.2.0 2020/09/02

- Use as django's command.

### v0.1.3 2020/07/25

- Fix time import problem.

### v0.1.2 2020/07/25

- Fix reload parameter problem.

### v0.1.1 2020/07/25

- Fix psutil import problem.

### v0.1.0 2020/07/25

- First release.
