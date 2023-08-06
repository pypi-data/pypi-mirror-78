# Django Runtime Options

[![CircleCI](https://circleci.com/gh/pennlabs/django-runtime-options.svg?style=shield)](https://circleci.com/gh/pennlabs/django-runtime-options)
[![Coverage Status](https://codecov.io/gh/pennlabs/django-runtime-options/branch/master/graph/badge.svg)](https://codecov.io/gh/pennlabs/django-runtime-options)
[![PyPi Package](https://img.shields.io/pypi/v/django-runtime-options.svg)](https://pypi.org/project/django-runtime-options/)

## Requirements

* Python 3.6+
* Django 2.2+

## Installation

Install with pip `pip install django-runtime-options`

Add `options` to `INSTALLED_APPS`

```python
INSTALLED_APPS = (
    ...
    'options.apps.OptionsConfig',
    ...
)
```

(Optionally) add the following to `urls.py`

```python
urlpatterns = [
    ...
    path("options/", include("options.urls", namespace="options")),
    ...
]
```

## Documentation

Runtime options can either be set in the django admin site or by using the `setoption` command.

An example of the management command is `./manage.py setoption key value --type TXT` which will create or update an option with the key "key" to the value "value"

## Changelog

See [CHANGELOG.md](https://github.com/pennlabs/django-runtime-options/blob/master/CHANGELOG.md)

## License

See [LICENSE](https://github.com/pennlabs/django-runtime-options/blob/master/LICENSE)
