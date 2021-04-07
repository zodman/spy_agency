## Spy agency

[![Django
CI](https://github.com/zodman/spy_agency/actions/workflows/django.yml/badge.svg)](https://github.com/zodman/spy_agency/actions/workflows/django.yml)


[![Coverage
Status](https://coveralls.io/repos/github/zodman/spy_agency/badge.svg?branch=master)](https://coveralls.io/github/zodman/spy_agency?branch=master)


Demo online: https://spy-agency.python3.ninja


## Install

```bash
cd spy_agency
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
fab init-db
yarn install # or npm install
yarn run build # or npm run build
python manage.py runserver
```
go to http://localhost:8000/

[init-db](https://github.com/zodman/spy_agency/blob/master/populate.py)

## Run test:

```bash
source .env/bin/activate
fab test
```

## deploy:
```
fab deploy -H zodman@python3.ninja

```
[tasks for deploy](https://github.com/zodman/spy_agency/blob/master/fabfile.py)

## Administration (internal)

    http://localhost:8000/admin
    admin/admin

The application contains a loginas.

With the admin go to: `Core >> Profiles`  
There will show the list of users  

    click on user >> then click on "Login as User"

That's the way more easy to switch username auth (without login with password)


* timeconsuming: 

    6 april: 7hrs
    5 april: 5hrs
    4 april: 2hrs
    3 april: 5hrs
    2 april: 2hrs
    1 april: 3hrs

    total: 24hrs
