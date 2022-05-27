from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from . import views
from .views import *

app_name = 'cryptoshop'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.product_list, name='product_list'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='concrete_category')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
