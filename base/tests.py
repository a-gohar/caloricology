from django.test import TestCase
from .models import food, macro_day, user_goals
from django.test import Client
from accounts.models import User
from django.urls import reverse
from django.test.client import RequestFactory
import json
class emptyUserGoalsTestCase(TestCase):
    def setUp(self):
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
        
    def test_addWeight(self):
        c1 = Client()
        c2 = Client()
        c1.login(username='john', password="glass onion")
        c2.login(username="john1", password="glass")
        response1 = c1.post(reverse("Add_weight"), data={"date": "2024-01-01", "weight": "80"})
        response2 = c2.post(reverse("Add_weight"), data={"date": "2024-01-01", "weight": "75"})
        self.assertEqual(80, macro_day.objects.get(owner = self.u1, date="2024-01-01").weight)
        self.assertEqual(75, macro_day.objects.get(owner = self.u2, date="2024-01-01").weight)
    
    def test_common_food(self):
        c1 = Client()
        c1.login(username='john', password="glass onion")
        data = {"food_name":"Test", "date":"2024-01-01",
                                               "calories":"100", "fat": "10", 
                                               "protein": "10", "carb":"10", "weight":"200"}
        response = c1.post(reverse("log_common_food"), json.dumps(data), content_type='application/json')
        dayObject = macro_day.objects.get(owner = self.u1, date="2024-01-01")
        self.assertEqual(200, dayObject.calories)
        self.assertEqual(200, food.objects.get(day=dayObject).cal)
        self.assertEqual(20, food.objects.get(day=dayObject).carbs)
        self.assertEqual(20, food.objects.get(day=dayObject).protein)
        self.assertEqual(20, food.objects.get(day=dayObject).fat)
        

        
        
        
    