# django-checkbox-normalize

It's bad design to put label after checkbox for BooleanField widget, so let's make it normal.


## Install

```shell
pip install django-checkbox-normalize
```

## Settings

```python
INSTALLED_APPS = [
    ...
    'django_checkbox_normalize',
    ...
]
```

## Usage

Just insert app name "django_checkbox_normalize" into INSTALLED_APPS variable before "django.contrib.admin" in settings.py, and nothing more.

**Note:**

- "django_checkbox_normalize" must before "django.contrib.admin".

## Releases

### v0.1.2 2020/09/09

- Add LICENSE file.

### v0.1.1 2020/03/03

- Fix BooleanField field style under small screen size.

### v0.1.0 2020/03/02

- First release.
