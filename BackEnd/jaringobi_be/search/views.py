from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView

from .models import CheapRecipe
from .serializers import CheapRecipeSerializer

from .es import search_fuzzy

# TODO: 나중에 get+post=ListCreateAPIView(메뉴 1개 찾고 없으면 post)로 리팩토링
class SearchResponseView(generics.RetrieveAPIView):  # get(read-one)
    queryset = CheapRecipe.objects.all()
    serializer_class = CheapRecipeSerializer
    lookup_field = 'menu'  # Use the menu field for lookup instead of pk

    def get(self, request, *args, **kwargs):
        menu = request.query_params.get('menu')
        if menu is not None:
            menu_candidates = search_fuzzy(menu, test=False)

            if isinstance(menu_candidates, list):
                for menu_candidate in menu_candidates:
                    results = CheapRecipe.objects.filter(menu__icontains=menu_candidate)
                    if results.exists():
                        serializer = CheapRecipeSerializer(results, many=True)
                        return Response({'results': serializer.data})
            return Response({'message': "There's no recipe you find."}, status=404)  # 이 코드 위치 주의
        return Response({'message': 'Menu parameter is required.'}, status=400)



class TestSearchFuzzyMenuView(APIView):  # fuzzy 검색 기능 테스트용
    def get(self, request, *args, **kwargs):
        menu = request.query_params.get('menu', None)
        response = search_fuzzy(menu)
        if response.status_code == 200:
            return Response(response.json())
        return Response({"error": response.text}, status=response.status_code)

