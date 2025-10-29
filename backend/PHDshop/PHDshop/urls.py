"""
URL configuration for PHDshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('customer.urls')),
    path('api/goods/', include('good.urls')),
    path('api/cart/', include('Cart.urls')),
    path('api/order/', include('Order.urls')),
    path('api/vouchers/', include('Voucher.urls')),



    # for admin
    path('api/admin/', include('Admin.urls')),
    

    path('api/vn/', include('vnpay_python.urls'))

]
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_URL = '/media/'  # Đường dẫn URL cho file media
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Thư mục chứa các file media được tải lên

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)