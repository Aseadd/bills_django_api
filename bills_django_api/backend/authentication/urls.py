from django.contrib import admin
from django.urls import path, include
from .views import Loginview, RegisterView, LogoutView, BillsView, BillCreateView, SwiftConnectionView

urlpatterns = [
    path('register', RegisterView.as_view(), name="register"),
    path('login', Loginview.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name = "logout"),
    path('bills', BillsView.as_view(), name="bills"),
    path('bills/<int:id>', BillsView.as_view(), name="bills"),
    path('create-bill', BillCreateView.as_view(), name="create-bill"),
    path('swift', SwiftConnectionView.as_view(), name="swift-connection"),
]
