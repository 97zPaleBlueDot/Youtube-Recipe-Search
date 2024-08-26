from django.urls import path

from .views import SearchResponseView, TestSearchFuzzyMenuView

urlpatterns = [
    path('search/', SearchResponseView.as_view(), name='menu'),
    path('search/fuzzy/', TestSearchFuzzyMenuView.as_view(), name='menu_fuzzy'),   # fuzzy 검색 기능 테스트용
    # path('search/term/', TestSearchTermMenuView.as_view(), name='menu_term'),   # term 검색 기능 테스트용
]
