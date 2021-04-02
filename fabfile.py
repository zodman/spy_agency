from invoke import run as local
from fabric import task

@task
def init_db(ctx):
    local("rm db.sqlite3")
    local("python manage.py migrate")
    local("python populate.py")

