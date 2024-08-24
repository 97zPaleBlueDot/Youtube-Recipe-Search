from rest_framework import serializers
from .models import Ingredient, Product, Recipe, YoutubeVdo, CheapRecipe


from rest_framework import serializers
from .models import Ingredient, Recipe, CheapRecipe, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ("id", "name", "badge_rocket", "expiration_date", "is_bulk", "created_at",)

# ModelSerializer 객체의 arguments들이 뭐가 더 있는지 보기.
class IngredientSerializer(serializers.ModelSerializer):
    cheapest_product = ProductSerializer(read_only=True)
    
    class Meta:
        model = Ingredient
        # fields = "__all__"
        exclude = ("id", "alternative_name", "recipe",)


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        exclude = ("id", "menu", "youtube_vdo",)


class CheapRecipeSerializer(serializers.ModelSerializer):
    # include ingredient details. Nested serializer: Handling Nested Relationships
    # ingredients = IngredientSerializer(many=True)  # read_only=True
    recipe = RecipeSerializer(read_only=True)
    
    class Meta:
        model = CheapRecipe
        exclude = ("id", "created_at", "updated_at",)