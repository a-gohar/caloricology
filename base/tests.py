from django.test import TestCase
from .models import food, macro_day, user_goals
from django.test import Client
from accounts.models import User
from django.urls import reverse
class emptyUserGoalsTestCase(TestCase):
    def setUp(self):
        print("TEST")
        self.u1 = User.objects.create_user(username='john',
                                    email='jlennon@beatles.com',
                                    password='glass onion')
        self.u2 = User.objects.create_user(username='john1',
                                    email='jlennon1@beatles.com',
                                    password='glass')
    def test_settings(self):
        c1 = Client()
        c2 = Client()
        c1.login(username='john', password="glass onion")
        c2.login(username="john1", password="glass")
        response1 = c1.post(reverse("Settings"), data={'weekly_target': "1", "tdee": "1000"}, follow=True)
        response2 = c2.post(reverse("Settings"), data={"weekly_target":"-1", "tdee":"1000"})
        g2 = self.u2.user_goals
        g1 = self.u1.user_goals
        self.assertEqual(50, g1.pRatio)
        self.assertEqual(15, g2.pRatio)