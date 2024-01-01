"""jwttoken URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from rest_framework_simplejwt import views as jwt_views
from authentication.views import Loginview, RegisterView, LogoutView, BillsView, BillCreateView, BillDetailView, CustomerView, CustomerView, UserView, ProductListView, SwiftConnectionView
from authentication.views import create_payment, webhook

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('authentication.urls')),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name ="token_obtain_pair"),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path('bills/', BillsView.as_view(), name="bills"),
    path('bills/<int:id>', BillsView.as_view(), name="bills"),
    path('bills/create/', BillCreateView.as_view(), name="create-bill"),
    path('bills/<int:id>', BillDetailView.as_view(), name="bill-detail"),
    path('customers/', CustomerView.as_view(), name="customers"),
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', Loginview.as_view(), name="login"),
    path('users/', UserView.as_view(), name="users"),
    path('users/<int:id>', UserView.as_view(), name="users"),
    path('api/create-payment/', create_payment, name='create-payment'),
    path('webhook/', webhook, name='webhook'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('swift/', SwiftConnectionView.as_view(), name='swift-connection'),
]
