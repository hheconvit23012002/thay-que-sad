"""vnpay_python URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import vnpay_python.views

urlpatterns = [
    path('', vnpay_python.views.index, name='index'),
    path('payment', vnpay_python.views.payment, name='payment'),
    path('payment_ipn', vnpay_python.views.payment_ipn, name='payment_ipn'),
    path('payment_return', vnpay_python.views.payment_return, name='payment_return'),
    path('query', vnpay_python.views.query, name='query'),
    path('refund', vnpay_python.views.refund, name='refund'),
    path('admin/', admin.site.urls),
]

