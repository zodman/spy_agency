from test_plus.test import TestCase
from django_seed import Seed
from django.contrib.auth.models import User
from .models import Profile, Hit
from django.db.models import Q


class TestMixin:
    def setUp(self):
        self.make_user("u1")
        self.make_user("u2")
        self.make_user("u3")
        hitman_user = User.objects.all().first()
        Profile.objects.create(type="hitman", user=hitman_user)
        user = User.objects.all()[1]
        boss = Profile.objects.create(type="boss", user=user)
        boss.manages.add(hitman_user)
        user = User.objects.all().last()
        Profile.objects.create(type="leader", user=user)
        s = Seed.seeder()
        s.add_entity(
            Hit, 30, {
                'assigned':
                lambda x: (User.objects.filter(username__startswith='u').
                           order_by("?")[0]),
                'created_by':
                lambda x: boss.user
            })
        s.execute()
        self.seeder = s


class TestFlow(TestMixin, TestCase):
    def test_flow_boss(self):
        with self.subTest("User Registration"):
            data = {
                'username': 'u4',
                'email': self.seeder.faker.email(),
                'password1': 'zxczxc123',
                'password2': 'zxczxc123'
            }
            self.post("registration_register", data=data)
            self.response_302()
            # self.assertFalse(self.get_context("form").errors)
            self.assertTrue(
                User.objects.filter(username='u4',
                                    profile__type='hitman').exists())
        with self.subTest("Add user to the boss"):
            user = User.objects.get(username="u4")
            with self.login(username="u2"):
                data = {
                    'user': user.id,
                    'manager': User.objects.get(username="u2").id
                }
                self.post("manage", data=data)
                self.response_302()
                user_boss = User.objects.get(username="u2")
                self.assertTrue(
                    user_boss.profile.manages.filter(id=user.id).exists())
        with self.subTest("Create hit to the new user"):
            with self.login(username="u2"):
                data = {
                    'assigned': user.id,
                    'target': self.seeder.faker.name(),
                    'description': self.seeder.faker.sentence(),
                }
                self.post("create_hit", data=data)
                self.response_302()
                self.assertTrue(
                    Hit.objects.filter(assigned=user,
                                       status="assigned").count() == 1)
        with self.subTest("Change status of the assigment"):
            with self.login(username="u4", password='zxczxc123'):
                hit = Hit.objects.filter(assigned=user,
                                         status="assigned").last()
                data = {'change_status': 'completed'}
                self.post("update_hit", pk=hit.id, data=data)
                hit = Hit.objects.get(id=hit.id)
                self.assertTrue(hit.status == 'completed')
        with self.subTest("Check listening assinged and created by"):
            with self.login(username="u2"):
                self.get("dashboard")
                table = self.get_context("table")
                hits = Hit.objects.filter(
                    Q(assigned__username="u2") | Q(created_by__username="u2"))
                self.assertTrue(hits.count() == table.data.data.count())

    def test_bigboss_flow(self):
        with self.login(username="u3"):
            with self.subTest("View all hits for the bigboss"):
                self.get("dashboard")
                table = self.get_context("table")
                hits = Hit.objects.all()
                self.assertTrue(hits.count() == table.data.data.count())
            with self.subTest("The bigboss cann't change hit closed"):
                hit = Hit.objects.all().last()
                hit.status = "failed"
                hit.save()
                self.get("hit_view", pk=hit.id)
                self.response_200()
                self.assertFalse("form_assigned" in self.last_response.context)
            with self.subTest("The bigboss can change assigment"):
                hit = Hit.objects.all().last()
                hit.status = "assigned"
                hit.save()
                self.get("hit_view", pk=hit.id)
                self.response_200()
                self.assertInContext("form_assigned")
                data = {
                    'assigned': 'u3',
                }
                self.post("update_hit", pk=hit.id, data=data)
                self.response_302()
            with self.subTest("the bigboss can assign hitmans to the boss"):
                self.get_check_200("manage")
                user = self.make_user("u5")
                Profile.objects.create(type="hitman", user=user)
                data = {
                    'manager': User.objects.get(username="u2").id,
                    'user': user.id,
                }
                self.post("manage", data=data)
                self.response_302()
                boss = Profile.objects.get(user__username="u2")
                self.assertTrue(boss.manages.filter(id=user.id).exists())
                with self.subTest("remove the hitman"):
                    data = {
                        'manager': User.objects.get(username="u2").id,
                        'user': user.id,
                    }
                    self.post("manage", data=data)
                    self.response_302()
                    boss = Profile.objects.get(user__username="u2")
                    self.assertFalse(boss.manages.filter(id=user.id).exists())

    def test_flow_manage_users(self):
        with self.login(username="u1"):
            self.get("hitmen")
            self.response_404()
        with self.subTest("boss can view here people"):
            with self.login(username="u2"):
                self.get("hitmen")
                self.response_200()
                self.assertInContext("table")
                table = self.get_context("table")
                self.assertEqual(1, table.data.data.count())
        with self.subTest("leader can view all"):
            with self.login(username="u3"):
                self.get("hitmen")
                self.response_200()
                table = self.get_context("table")
                self.assertTrue(table.data.data.count() > 1)
        with self.subTest("leader can change status of hitman"):
            with self.login(username="u3"):
                profile = Profile.objects.get(type="hitman")
                data = {
                    'status': 'inactive',
                    'description': 'Deactivated!',
                    'type': profile.type
                }
                self.post("hitman_update", pk=profile.id, data=data)
                self.response_302()
                profile = Profile.objects.get(type="hitman")
                self.assertEqual(profile.status, 'inactive')

    def test_boss_hitman_flow(self):
        with self.subTest("boss can change status of hitman"):
            with self.login(username="u2"):
                self.assertEqual(User.objects.get(username="u2").profile.type,
                                 "boss")
                profile = Profile.objects.get(type="hitman")
                data = {
                    'status': 'inactive',
                    'description': 'Deactivated!',
                }
                self.post("hitman_update", pk=profile.id, data=data)
                self.response_302()
                profile = Profile.objects.get(type="hitman")
                self.assertEqual(profile.status, 'inactive')

    def test_bulk_flow(self):
        with self.login(username="u3"):
            self.get_check_200("bulk")
            user = Profile.objects.get(type="hitman").user
            self.post("bulk", data={'assigned': user.id})
            self.response_302()


class TestHitman(TestMixin, TestCase):
    def test_views(self):
        self.get_check_200("index")
        with self.login(username="u2"):
            self.get("index")
            self.response_302()
            self.get("/hits")
            self.response_301()
            self.get("/hitmen")
            self.response_301()
            self.get("/hits/bulk")
            self.response_302()


        self.get("/register")
        self.response_301()
        self.get("/logout")
        self.response_301()

    def test_hit_detail(self):
        h = Hit.objects.filter(assigned__username="u1").first()

        with self.subTest("view own hit") and self.login(username="u1"):
            self.get_check_200("hit_view", pk=h.id)
        h = Hit.objects.exclude(assigned__username="u1").first()
        with self.subTest("view others hit") and self.login(username="u1"):
            self.get("hit_view", pk=h.id)
            self.response_404()

    def test_create_hit(self):
        user = User.objects.get(username='u1')
        with self.login(username='u2'):
            self.get("create_hit")
            form = self.get_context("form")
            self.assertTrue(form.fields["assigned"].queryset.count() == 1)
            data = {
                'target': "target1",
                'description': "description",
                'assigned': user.id,
            }
            self.post("create_hit", data=data)
            self.response_302()

    def test_assing_user(self):
        user = User.objects.get(username='u1')
        with self.login(username=user.username):
            response = self.get("dashboard")
            qs = response.context["table"].data.data
            for i in qs:
                with self.subTest(i=i):
                    self.assertTrue(i.assigned == user)

    def test_update_view(self):
        h = Hit.objects.filter(assigned__username="u1").first()
        h.status = 'assigned'
        h.save()
        with self.login(username="u1"):
            data = {'change_status': 'failed'}
            with self.subTest("success"):
                response = self.post("update_hit", pk=h.id, data=data)
                self.response_302(response)
                h = Hit.objects.get(id=h.id)
                self.assertTrue(h.status == 'failed', h.status)
            with self.subTest("notFound"):
                h = Hit.objects.exclude(assigned__username="u1").first()
                oldstatus = h.status
                response = self.post("update_hit", pk=h.id, data=data)
                self.response_302(response)
                h = Hit.objects.get(id=h.id)
                self.assertTrue(h.status == oldstatus, h.status)
