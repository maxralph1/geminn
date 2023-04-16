from django.urls import path

from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.index, name='index'),
    path('categories/', views.categories, name='categories'),
    path('categories/<slug:category_slug>/', views.category, name='category'),
    path('sub_categories/<slug:sub_category_slug>/',
         views.sub_category, name='sub_category'),
    path('products/', views.products, name='products'),
    path('product/<slug:product_slug>/', views.product, name='product'),
    path('lookup/', views.lookup, name='lookup'),
    path('contact-us/', views.contact_us, name='contact_us'),
]
