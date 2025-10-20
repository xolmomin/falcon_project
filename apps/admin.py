from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.models import Product, Cart, CartItem, Category, Tag, ProductImage, User


@admin.register(Tag)
class TagModelAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(ProductImage)
class ProductImageModelAdmin(admin.ModelAdmin):
    pass


class ProductImageStackedInline(admin.StackedInline):
    model = ProductImage
    min_num = 1
    extra = 0
    max_num = 8


class CartItemStackedInline(admin.StackedInline):
    model = CartItem
    min_num = 1
    extra = 0
    max_num = 8


@admin.register(CartItem)
class CartItemModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    inlines = CartItemStackedInline,


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    inlines = [ProductImageStackedInline]
    filter_horizontal = ['tags']
    search_fields = ['name']

@admin.register(User)
class UserModelAdmin(UserAdmin):
    pass
