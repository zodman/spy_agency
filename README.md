## Spy agency

[![Django
CI](https://github.com/zodman/spy_agency/actions/workflows/django.yml/badge.svg)](https://github.com/zodman/spy_agency/actions/workflows/django.yml)


[![Coverage
Status](https://coveralls.io/repos/github/zodman/spy_agency/badge.svg?branch=master)](https://coveralls.io/github/zodman/spy_agency?branch=master)


[https://spy-agency.python3.ninja]


## Install

```python
cd spy_agency
python3 -m venv .env/bin/activate
pip install -r requirements.in
fab init-db
yarn install
yarn run build
python manage.py runserver
```

go to http://localhost:8000/


## admisnitration (internal)

http://localhost:8000/admin
admin/admin

the application contains a loginas module you can go to:

With the admin go to: Core >> Profiles

Here show the list of users

click on user >> then click on "Login as User"

Thats the way more easy to switch username
