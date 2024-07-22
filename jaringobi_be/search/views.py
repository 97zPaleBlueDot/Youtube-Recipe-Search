from django.http import Http404

from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import api_view

from .models import CheapRecipe, CheapestProduct
from .serializers import SearchResponseSerializer


# https://wikidocs.net/70649
@api_view(['GET'])
def home(request):
    return Response("최저가 유튜버 레시피는?")


# TODO: 나중에 get+post=ListCreateAPIView(메뉴 1개 찾고 없으면 post)로 리팩토링
# 오버라이드 할 수 있는 다른 메서드들도 알아보기
class SearchResponseView(generics.RetrieveAPIView):  # get(read-one)
    serializer_class = SearchResponseSerializer

    # def get(self, request, pk, format=None):
    def get_object(self):
        try:
            menu = self.request.query_params.get('search', None)  # URL query parameter 로 넘어온 메뉴명 get
            # 해당 메뉴명과 정확히 일치하는 CheapRecipe 테이블 row 1개 반환
            recipe = CheapRecipe.objects.get(menu=menu)  # TODO: (도균님) 정확하게 일치하는 결과만을 찾지 않도록, 유연한 검색 로직 개발
        except CheapRecipe.DoesNotExist:
            return Response({'error': 'Recipe not found'}, status=404)

        serializer = SearchResponseSerializer(recipe)
        return Response(serializer.data)

    # def get_queryset(self):
    #     queryset = CheapRecipe.objects.all()
    #     menu = self.request.query_params.get('search', None)
    #     if menu:
    #         # 여러개면 filter. 그리고 검색 기능 정교함에 따라 이거 갖고 안될 수 있음. menu__icontians는 lookup 찾아보면 나오고, case-insensitive match 말하는거임.
    #         queryset = queryset.filter(title__icontains=menu)
    #     return queryset
