import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
import django
from django.conf import settings

django.setup()
from django_seed import Seed
from core.models import Profile, Hit
from django.contrib.auth.models import User

seeder = Seed.seeder()

seeder.add_entity(User, 4, {'is_staff': lambda x: False})
seeder.execute()

user = User.objects.all()[0]
hitman = Profile.objects.create(type="hitman", user=user)
user = User.objects.all()[1]
boss = Profile.objects.create(type="boss", user=user)
user = User.objects.all()[2]
Profile.objects.create(type="leader", user=user)
user = User.objects.all()[3]
boss = Profile.objects.create(type="boss", user=user)

s = Seed.seeder()
s.add_entity(Hit, 30, {'assigned': hitman.user, 'created_by': boss.user , 'target': lambda x: s.faker.name()})
s.execute()
s.add_entity(Hit, 30, {'target': lambda x: s.faker.name()})
s.execute()
admin = User.objects.create_superuser("admin", "admin@example.com", "admin")
Profile.objects.create(type="leader", user=admin)


for i in User.objects.exclude(username='admin'):
    i.set_password("demo1")
    i.save()
    try:
        i.profile
    except Profile.DoesNotExist:
        Profile.objects.create(type="hitman", user=i)
