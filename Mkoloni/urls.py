"""
URL configuration for Mkoloni project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from store import views
from django.conf import settings
from django.conf.urls.static import static
from store import mpesa
from store.views import home


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.product_list, name='home'),
    path('product/<int:category_id>/', views.product_detail, name="product"), 
    path('addtocart/<int:item_id>/', views.add_to_cart, name='addtocart'),
    path('cart/', views.cart_view, name='cart'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('removefromcart/<int:pk>/', views.remove_from_cart, name='removefromcart'),
    path('payment/', views.mpesa_payment, name='payment'),
    path('stkpush/',mpesa.lipa_na_mpesa_online, name='stkpush'),
    path('about/', views.about, name='about'),
    path('', home, name='home'),

    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

