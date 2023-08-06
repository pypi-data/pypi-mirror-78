from django.urls import path

from drf_expiring_token.views import LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login')
]
