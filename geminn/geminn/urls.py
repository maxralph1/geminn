from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls', namespace='pages')),
    path('dashboard/', include('inventory.urls', namespace='inventory')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('checkout/', include('checkout.urls', namespace='checkout')),
    path('bag/', include('bag.urls', namespace='bag')),
    path('orders/', include('orders.urls', namespace='orders'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
