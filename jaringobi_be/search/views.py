from django.http import Http404

from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import generics
from rest_framework.decorators import api_view

from .models import CheapRecipe
from .serializers import CheapRecipeSerializer


# https://wikidocs.net/70649
@api_view(['GET'])
def home(request):
    return Response("최저가 유튜버 레시피는?")


# TODO: 나중에 get+post=ListCreateAPIView(메뉴 1개 찾고 없으면 post)로 리팩토링
# 오버라이드 할 수 있는 다른 메서드도 많다.
class SearchResponseView(generics.RetrieveAPIView):  # get(read-one)
    queryset = CheapRecipe.objects.all()
    serializer_class = CheapRecipeSerializer
    lookup_field = 'menu'  # Use the menu field for lookup instead of pk

    def get_object(self):
        menu = self.kwargs.get('menu') # TODO: (도균님) 정확하게 일치하는 결과만을 찾지 않도록, 유연한 검색 로직 개발
        if menu is not None:
            try:
                return self.queryset.get(menu=menu)
            except CheapRecipe.DoesNotExist:
                raise NotFound("Menu not found")
        raise NotFound("Invalid parameter")
