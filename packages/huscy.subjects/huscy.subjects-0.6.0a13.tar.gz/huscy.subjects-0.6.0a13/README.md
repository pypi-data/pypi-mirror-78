huscy.subjects
======

![PyPi Version](https://img.shields.io/pypi/v/huscy-subjects.svg)
![PyPi Status](https://img.shields.io/pypi/status/huscy-subjects)
![PyPI Downloads](https://img.shields.io/pypi/dm/huscy-subjects)
![PyPI License](https://img.shields.io/pypi/l/huscy-subjects?color=yellow)
![Python Versions](https://img.shields.io/pypi/pyversions/huscy-subjects.svg)
![Django Versions](https://img.shields.io/pypi/djversions/huscy-subjects)



Requirements
------

- Python 3.6+
- A supported version of Django

Tox tests on Django versions 2.1, 2.2 and 3.0.



Installation
------

To install `husy.subjects` simply run:
```
pip install huscy.subjects
```



Configuration
------

First of all, the `huscy.subjects` application has to be hooked into the project.

1. Add `huscy.subjects` and further required apps to `INSTALLED_APPS` in settings module:

```python
INSTALLED_APPS = (
	...
	'django_countries',
	'phonenumber_field',
	'rest_framework',
	'rest_framework_nested',

	'huscy.subjects',
)
```

2. Create `huscy.subjects` database tables by running:

```
python manage.py migrate
```



REST-Endpoints
------

URL                                                   | HTTP Method | Description
------------------------------------------------------|-------------|------------
`/api/subjects/`                                      | GET         | Returns 500 subjects, paginated by 25 items per page and ordered by `contact__last_name` and `contact__first_name`.
                                                      |             | Additional get parameter allowed:
                                                      |             | - `count=<items_per_page>` - configure the items per page; max count is 100
                                                      |             | - `ordering=<field_name>` - comma separated list of fields. One can order by `contact__first_name`, `contact__last_name`, `contact__gender` or `contact__date_of_birth`
                                                      |             | - `page=<page>` - show results on page `page`
                                                      |             | - `serach=<query_string>` - search for `display_name` or `date_of_birth`
`/api/subjects/<subject_id>/guardians/`               | POST        | Create new contact and add as guardian to subject.
`/api/subjects/<subject_id>/guardians/<guardian_id>/` | DELETE      | Removes the guardian for subject.
`/api/subjects/<subject_id>/notes/`                   | GET         | Returns the list of all notes for subject.
`/api/subjects/<subject_id>/notes/`                   | POST        | Create new note about subject. Other option should be chosen to save comment.
`/api/subjects/<subject_id>/notes/<note_id>/`         | DELETE      | Removes the note about subject
`/api/subjects/<subject_id>/inactivity/`              | DELETE      | Removes inactivity for subject.
                                                      | POST        | Creates or updates the inactivity for a subject.



Development
------

After checking out the repository you should activate any virtual environment.
Install all development and test dependencies:

```
make install
```

Create migration files and database tables:

```
make makemigrations
make migrate
```

We assume you're having a running postgres database with a user `huscy` and a database also called `huscy`.
You can easily create them by running

```
sudo -u postgres createuser -d huscy
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE huscy TO huscy;"
sudo -u postgres psql -c "ALTER USER huscy WITH PASSWORD '123';"
sudo -u postgres createdb huscy
```
