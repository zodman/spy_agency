from invoke import run as local
from fabric import task


@task
def init_db(ctx):
    local("rm db.sqlite3")
    local("python manage.py migrate")
    local("python populate.py")


@task
def test(c):
    local("coverage run manage.py test --failfast")
    local("coverage report -m ")
    local("coverage html")


@task
def deploy(c):
    pass
