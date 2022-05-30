from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def get_absolute_url(self):
        return reverse('cryptoshop:product_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    profile_pic = models.ImageField(blank=True, upload_to="photos/profile/%Y/%m/%d", default="static/img/no_image.png")
    address = models.CharField(max_length=100, blank=True)
    work_place = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=254, default=False)

    def __str__(self):
        return self.user.username
