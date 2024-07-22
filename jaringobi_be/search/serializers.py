from rest_framework import serializers
from .models import Ingredient, Product, Recipe, RecipeIngredient, YoutubeVdo, CheapestProduct, CheapRecipe



# ModelSerializer 객체의 arguments들이 뭐가 더 있는지 보기.
class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"


class RecipeIngredientSerializer(serializers.ModelSerializer):
    # This serializer will be used to include additional fields from the RecipeIngredient model.
    ingredients = IngredientSerializer()
    
    class Meta:
        model = RecipeIngredient
        fields = "__all__"


class RecipeSerializer(serializers.ModelSerializer):
    # SerializerMethodField는 메서드 통해 Custom Fields 정의할 떄 사용
    ingredients = serializers.SerializerMethodField()
    ingredients_without_unit = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = "__all__"

    def get_ingredients(self, obj):
        ingredients = [ri.ingredient for ri in RecipeIngredient.objects.filter(recipe=obj)]
        return RecipeIngredientSerializer(ingredients, many=True).data

    def get_ingredients_without_unit(self, obj):
        ingredients_without_unit = Ingredient.objects.filter(recipeingredient__recipe=obj, unit__isnull=True, vague__isnull=False)
        return RecipeIngredientSerializer(ingredients_without_unit, many=True).data


###################################################
class CheapRecipeSerializer(serializers.ModelSerializer):
    # include ingredient details.
    ingredients = RecipeSerializer(many=True)  # Nested serializer: Handling Nested Relationships
    ingredients_without_unit = RecipeSerializer(many=True)
    
    class Meta:
        model = CheapRecipe
        exclude = ("id", "created_at", "updated_at",)


class CheapestProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheapestProduct
        exclude = ("id", "created_at", "updated_at",)


# 궁극 목표
# 한 번에 2개 이상의 모델 사용 가능하면 ModelSerializer 쓰는데, 아니라면...
# Combining Serializers for Complex Responses
class SearchResponseSerializer(serializers.Serializer):
    cheap_recipes = CheapRecipeSerializer(many=True)
    cheapest_products = CheapestProductSerializer(many=True)


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
