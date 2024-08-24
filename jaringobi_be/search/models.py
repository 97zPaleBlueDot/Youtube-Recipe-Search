# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


####################################
# PositiveIntegerField 도 있네... 전부 이거로 바꾸고 싶..
class Ingredient(models.Model):
    id = models.AutoField(primary_key=True)
    recipe = models.ForeignKey('Recipe', related_name='ingredients', on_delete=models.DO_NOTHING)
    alternative_name = models.CharField(max_length=64, blank=True, null=True)
    cheapest_product = models.OneToOneField('Product', models.DO_NOTHING)
    name = models.CharField(max_length=64)
    quantity = models.FloatField(blank=True, null=True)
    unit = models.CharField(max_length=32, blank=True, null=True)
    vague = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ingredient'


class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=64)
    category = models.CharField(max_length=64, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'menu'


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=1024)
    product_title = models.CharField(max_length=1024, blank=True, null=True)
    unit_price = models.FloatField(blank=True, null=True)
    unit_value = models.FloatField(blank=True, null=True)
    unit_name = models.CharField(max_length=32, blank=True, null=True)
    url = models.CharField(max_length=2048, blank=True, null=True)
    img_src = models.CharField(max_length=2048, blank=True, null=True)
    badge_rocket = models.CharField(max_length=64, blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)
    is_bulk = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)  # auto_now_add=True

    class Meta:
        managed = False
        db_table = 'product'


class QuantityConversion(models.Model):
    conversion_id = models.AutoField(primary_key=True)
    ingredient_name = models.CharField(max_length=64, blank=True, null=True)
    unit_name = models.CharField(max_length=32, blank=True, null=True)
    converted_gram = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'quantity_conversion'


class Recipe(models.Model):
    id = models.AutoField(primary_key=True)
    youtube_vdo = models.OneToOneField('YoutubeVdo', models.DO_NOTHING)  # on_delete=models.CASCADE,
    menu = models.OneToOneField('Menu', models.DO_NOTHING)
    portions = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recipe'


class UnitConversion(models.Model):
    conversion_id = models.AutoField(primary_key=True)
    standard_unit = models.CharField(max_length=32, blank=True, null=True)
    converted_vol = models.FloatField(blank=True, null=True)
    unit_name = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'unit_conversion'


class YoutubeVdo(models.Model):
    id = models.AutoField(primary_key=True)
    menu = models.OneToOneField('Menu', models.DO_NOTHING)
    youtube_url = models.CharField(max_length=256)
    full_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'youtube_vdo'


class CheapRecipe(models.Model):
    id = models.AutoField(primary_key=True)
    recipe = models.OneToOneField('Recipe', models.DO_NOTHING)  # 재료id 리스트 갖고 오려고.
    # recipe_id = models.IntegerField()  # 재료id 리스트 갖고 오려고.
    menu = models.CharField(unique=True, max_length=64)  # 화면 렌더링 할 + 쿼리 파라미터로 받아 찾는, 알찬 용도의 메뉴명!
    youtube_url = models.CharField(max_length=1024)  # 화면 렌더링용
    min_total_price = models.FloatField(blank=True, null=True)  # 화면 렌더링용
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cheap_recipe'

class RequestLog(models.Model):
    request_url = models.CharField(max_length=255)
    http_method = models.CharField(max_length=10)
    request_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.url} - {self.method} - {self.timestamp}"