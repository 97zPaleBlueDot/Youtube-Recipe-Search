from django.urls import path

from .views import SearchResponseView, home

urlpatterns = [
    # path('search/<str:menu>', SearchResponseView.as_view(), name='result'),
    path('search/', SearchResponseView.as_view(), name='menu'),
]
