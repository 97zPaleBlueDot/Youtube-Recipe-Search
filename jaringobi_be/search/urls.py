from django.urls import path

from .views import SearchResponseView, home, SearchFuzzyMenuView, SearchMatchMenuView, SearchTermMenuView

urlpatterns = [
    path('search/', home),
    path('search/<str:menu>', SearchResponseView.as_view(), name='result'),
    path('search/fuzzy/', SearchFuzzyMenuView.as_view(), name='menu_fuzzy'),
    path('search/match/', SearchMatchMenuView.as_view(), name='menu_match'),
    path('search/term/', SearchTermMenuView.as_view(), name='menu_term'),
]
