from django.http import Http404

from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from .models import CheapRecipe
from .serializers import CheapRecipeSerializer

from .es import search_fuzzy, search_match, search_term


# TODO: 나중에 get+post=ListCreateAPIView(메뉴 1개 찾고 없으면 post)로 리팩토링
class SearchResponseView(generics.RetrieveAPIView):  # get(read-one)
    queryset = CheapRecipe.objects.all()
    serializer_class = CheapRecipeSerializer
    lookup_field = 'menu'  # Use the menu field for lookup instead of pk

    def get(self, request, *args, **kwargs):
        menu = request.query_params.get('menu')
        if menu is not None:
            results = CheapRecipe.objects.filter(menu__icontains=menu)
            if results.exists():
                serializer = CheapRecipeSerializer(results, many=True)
                return Response({'results': serializer.data})
            else:
                return Response({'message': "There's no recipe you find."}, status=404)
        return Response({'message': 'Menu parameter is required.'}, status=400)

        
class SearchFuzzyMenuView(APIView):
    def get(self, request, *args, **kwargs):
        menu = request.query_params.get('menu', None)
        
        result = search_fuzzy(menu)
        
        if isinstance(result, tuple):
            return Response({"error": result[1]}, status=result[0])
        
        return Response(result)
    
class SearchMatchMenuView(APIView):
    def get(self, request, *args, **kwargs):
        menu = request.query_params.get('menu', None)
        
        result = search_match(menu)
        
        if isinstance(result, tuple):
            return Response({"error": result[1]}, status=result[0])
        
        return Response(result)
    
class SearchTermMenuView(APIView):
    def get(self, request, *args, **kwargs):
        menu = request.query_params.get('menu', None)
        
        result = search_term(menu)
        
        if isinstance(result, tuple):
            return Response({"error": result[1]}, status=result[0])
        
        return Response(result)
