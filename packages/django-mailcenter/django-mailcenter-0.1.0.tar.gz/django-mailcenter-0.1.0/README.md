# django-mailcenter

Django mailcenter application.

## Install

```
pip install django-mailcenter
```

## Usage

**pro/settings.py**

```
INSTALLED_APPS = [
    ...
    'django_static_ace_builds',
    'django_db_lock',
    'django_fastadmin',
    'django_mailcenter',
    ...
]
```

- AceWidget used for options editor, so we needs `django_static_ace_builds` to provide ace-builds static files, and `django_fastadmin.widgets.AceWidget`.
- models.MailForDelivery as based on `django_fastadmin.models.SimpleTask` and it use `django_db_lock` to do distribute lock.

## Releases

### v0.1.0 2020/08/31

- First release.
