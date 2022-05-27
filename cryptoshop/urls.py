from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from . import views
from .views import *

app_name = 'cryptoshop'
urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='concrete_category'),
    path('profile/<int:pk>/', ShowProfileView.as_view(), name='profile'),
    path('add_product/', CreateNewProduct.as_view(), name='add_product'),
    path('delete_product/<int:pk>', DeleteProduct.as_view(), name='delete_product'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
