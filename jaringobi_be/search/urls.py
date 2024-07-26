from django.urls import path

from .views import SearchResponseView, home

urlpatterns = [
    path('search/', home),
    path('search/<str:menu>', SearchResponseView.as_view(), name='result'),
]
