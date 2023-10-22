"""
URL configuration for FutureCabin project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from viewer.views import homepage, reservations, contact
from accounts.views import logout_view, registration, account
from reservation.views import checkout, order

urlpatterns = [
    path('', homepage, name='homepage'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('registration/', registration, name='registration'),
    path('accounts/profile/', account, name='account_after_login'),
    path('account/', account, name='account'),
    path('logout/', logout_view, name='logout'),
    path('reservations/', reservations, name='reservations'),
    path('contact/', contact, name='contact'),
    path('checkout/', checkout, name='checkout'),
    path('order/<int:order_id>/', order, name='order'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
