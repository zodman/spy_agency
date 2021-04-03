from test_plus.test import TestCase
from django_seed import Seed
from django.contrib.auth.models import User
from .models import Profile, Hit


class TestAssigned(TestCase):
    def setUp(self):
        self.make_user("u1")
        self.make_user("u2")
        self.make_user("u3")
        user = User.objects.all().first()
        Profile.objects.create(type="hitman", user=user)
        user = User.objects.all()[1]
        boss = Profile.objects.create(type="boss", user=user)
        user = User.objects.all().last()
        Profile.objects.create(type="leader", user=user)
        s = Seed.seeder()
        s.add_entity(
            Hit, 30, {
                'assigned': lambda x: (User.objects
                                       .filter(username__startswith='u')
                                       .order_by("?")[0]),
                'created_by': lambda x: boss.user
            })
        s.execute()

    def test_hit_detail(self):
        h = Hit.objects.filter(assigned__username="u1").first()

        with self.subTest("view own hit") and self.login(username="u1"):
            self.get_check_200("hit_view", pk=h.id)
        h = Hit.objects.exclude(assigned__username="u1").first()
        with self.subTest("view others hit") and self.login(username="u1"):
            self.get("hit_view", pk=h.id)
            self.response_404()


    def test_assing_user(self):
        user = User.objects.get(username='u1')
        with self.login(username=user.username):
            response = self.get("dashboard")
            qs = response.context["table"].data.data
            for i in qs:
                with self.subTest(i=i):
                    self.assertTrue(i.assigned == user)

    def test_update_view(self):
        with self.login(username="u1"):
            data = {'change_status':'new'}
            with self.subTest("success"):
                h = Hit.objects.filter(assigned__username="u1").first()
                response = self.post("update_hit", pk=h.id, data=data)
                self.response_302(response)
            with self.subTest("notFound"):
                h = Hit.objects.exclude(assigned__username="u1").first()
                response = self.post("update_hit", pk=h.id, data=data)
                self.response_404(response)


