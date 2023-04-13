from django import forms
from django.contrib import admin

from .models import Category, SubCategory, Brand, Discount, Product, ProductUnit, ProductUnitImage, ProductSpecification, ProductSpecificationValue, ProductReview


admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Brand)
admin.site.register(Discount)


class ProductUnitInline(admin.TabularInline):
    model = ProductUnit


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification


class ProductSpecificationValueInline(admin.TabularInline):
    model = ProductSpecificationValue


class ProductUnitImageInline(admin.TabularInline):
    model = ProductUnitImage


class ProductInline(admin.TabularInline):
    model = ProductReview


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductUnitInline,
        ProductSpecificationInline,
    ]


@admin.register(ProductUnit)
class ProductUnitAdmin(admin.ModelAdmin):
    inlines = [
        ProductUnitImageInline,
        ProductSpecificationValueInline,
    ]
