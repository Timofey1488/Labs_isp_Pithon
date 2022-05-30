import logging
from django.test import Client, TestCase, SimpleTestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from cart.forms import CartAddProductForm
from cryptoshop.forms import ProductNewForm

from cryptoshop.models import Product, Category, Profile

User = get_user_model()
logging.disable()


class TestViews(TestCase):
    def __init__(self, methodName: str = ...):
        super().__init__(methodName)
        self.profile = None

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='testuser', password="password")
        self.category = Category.objects.create(name='Something')
        self.product = Product.objects.create(category=self.category, name="Your Mother", price="100", description="Somesdhfgkjdfg",
                                              stock=10)

    def test_register(self):
        response = self.client.get(reverse('cryptoshop:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cryptoshop/register.html')

    def test_login(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)

    def test_edit_profile(self):
        self.profile = Profile.objects.create(user=self.user)
        response = self.client.get(reverse('cryptoshop:edit_profile', kwargs={'pk': self.profile.pk}))
        self.assertEqual(response.status_code, 302)

    def test_change_password(self):
        self.profile = Profile.objects.create(user=self.user)
        response = self.client.get(reverse('cryptoshop:change_password', kwargs={'pk': self.profile.pk}))
        self.assertEqual(response.status_code, 302)


class SignUpPageTests(TestCase):

    def setUp(self):
        self.username = 'new_user1'
        self.password1 = 'clownsasgahjgf'
        self.password2 = 'clownsasgahjgf'
        self.client = Client()

    def test_signup_page_status_code(self):
        response = self.client.get(reverse('cryptoshop:register'))
        self.assertEqual(response.status_code, 200)

    def test_signup_form(self):
        response = self.client.post(reverse('login'), {'username': self.username, 'password1': self.password1,
                                                          'password2': self.password2})

        self.assertEqual(response.status_code, 200)


class ProductTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='testuser', password="password")
        self.client.force_login(self.user)
        self.profile = Profile.objects.create(user=self.user, address="aasfdgdsgdf")

        self.category = Category.objects.create(name='kek')
        self.product = Product.objects.create(category=self.category, name="My Mother", price="100",
                                              description="Somesdhfgkjdfg",
                                              stock=10)

    def test_product_delete_page(self):
        response = self.client.post(reverse("cryptoshop:delete_product", kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 302)

    def test_product_update_page(self):
        response = self.client.post(reverse("cryptoshop:edit_product", kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 200)


class TestForms(SimpleTestCase):
    def test_form_new_product(self):
        form = ProductNewForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)


class TestViewsCart(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        self.category = Category.objects.create(name='Something')
        self.product = Product.objects.create(category=self.category, name="Your Mother", price="100", description="Somesdhfgkjdfg",
                                              stock=10, )

    def test_register(self):
        response = self.client.get(reverse('cryptoshop:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cryptoshop/register.html')

    def test_cart_add(self):
        response = self.client.post(reverse("cart:cart_add", kwargs={'product_id': self.product.pk}))
        self.assertEqual(response.status_code, 302)

    def test_cart_detail(self):
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/detail.html')


class TestFormAdd(SimpleTestCase):
    def test_form_add(self):
        form = CartAddProductForm(data={
            'quantity': 10
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form = CartAddProductForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)




