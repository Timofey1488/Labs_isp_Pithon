# import logging
# from unittest import TestCase
#
# from django.contrib.auth import get_user_model
#
# from orders.models import Order
# from .models import *
# from django.test import Client
# from django.test import TestCase
#
# User = get_user_model()
# logging.disable()
#
#
# class CatalogTests(TestCase):
#     def setUp(self):
#         self.user = User.objects.create(username='Timon1488', password="pipom6pro")
#         self.client = Client(enforce_csrf_checks=False)
#         self.client.force_login(self.user)
#         self.profile = Profile.objects.create(user=self.user, address="aasfdgdsgdf")
#
#         self.category = Category.objects.create(name='kek')
#         self.product = Product.objects.create(name="lol", category=self.category, cost=10)
#         self.order = Order.objects.create(user=self.user, product=self.product, amount=10)
#
#     def test_orders_page_status_code(self):
#         response = self.client.get(reverse('orders'))
#         self.assertEqual(response.status_code, 200)
#
#     def test_cart_page_status_code(self):
#         response = self.client.get(reverse('cart'))
#         self.assertEqual(response.status_code, 200)

