from django.urls import path

from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.index, name='index'),
    path('categories/', views.categories, name='categories'),
    path('products/', views.products, name='products'),
    path('product/<slug:product_slug>/', views.product, name='product'),
    path('contact-us/', views.contact_us, name='contact_us'),
]
