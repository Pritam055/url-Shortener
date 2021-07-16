from django.urls import path

from .views import HomeView, RedirectToURLView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('<str:shortcode>/', RedirectToURLView.as_view(), name='redirect_url')
]