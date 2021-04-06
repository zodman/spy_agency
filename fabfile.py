from invoke import run as local
from fabric import task
from patchwork.transfers import rsync

exclude_dirs = [".git", "node_modules", ".cache", ".github", "db.sqlite3",
                ".env"]


@task
def init_db(ctx):
    local("rm -f db.sqlite3")
    local("python manage.py migrate")
    local("python populate.py")


@task
def test(c):
    local("coverage run manage.py test --failfast")
    local("coverage report -m ")
    local("coverage html")


@task
def deploy(ctx):
    local("yarn install", echo=True)
    local("yarn run build", echo=True)
    local("python manage.py collectstatic --noinput", echo=True)
    local("find . -name '__pycache__' |xargs rm -rf ", echo=True)
    rsync(ctx, ".", "apps/spy_agency", exclude=exclude_dirs)
    with ctx.cd("apps/spy_agency"):
        with ctx.prefix("source ~/apps/spy_agency/.env/bin/activate"):
            ctx.run("pip install -r requirements.txt")
            ctx.run("python manage.py migrate")
    ctx.run("sudo supervisorctl restart spy-agency")


