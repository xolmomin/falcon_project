from django.contrib import admin

from apps.models import Product, Category, Tag, ProductImage


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


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    inlines = [ProductImageStackedInline]
    filter_horizontal = ['tags']
