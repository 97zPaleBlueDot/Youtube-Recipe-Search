from rest_framework import serializers
from .models import Ingredient, Product, Recipe, YoutubeVdo, CheapRecipe


# ModelSerializer 객체의 arguments들이 뭐가 더 있는지 보기.
class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        # fields = "__all__"
        exclude = ("id", "alternative",)


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        exclude = ("id", "menu_id",)


class CheapRecipeSerializer(serializers.ModelSerializer):
    # include ingredient details. Nested serializer: Handling Nested Relationships
    # ingredients = IngredientSerializer(many=True)  # read_only=True
    recipe = RecipeSerializer(read_only=True)
    
    class Meta:
        model = CheapRecipe
        exclude = ("id", "created_at", "updated_at",)


"""
ORM 라이브러리로 레시피 최저가 계산하는 코드 예시. 나중에 사용 가능
def get_total_price(self, obj):
        total = 0
        for recipe_ingredient in RecipeIngredient.objects.filter(recipe=obj):
            ingredient = recipe_ingredient.ingredient
            try:
                product = CheapestProduct.objects.get(ingredient_id=ingredient.id)
                if product.unit_price and ingredient.quantity:
                    total += ingredient.quantity * product.unit_price
            except CheapestProduct.DoesNotExist:
                pass
        return total
"""
