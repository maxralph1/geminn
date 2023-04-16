from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from inventory.models import Product, ProductUnit, ProductUnitImage, ProductSpecification, ProductSpecificationValue, Category, SubCategory


def index(request):
    product_units = ProductUnit.objects.prefetch_related(
        'product_unit_image').filter(is_active=True).order_by('?')[:1]

    return render(request, 'pages/index.html', {'product_units': product_units})


def categories(request):
    categories = Category.objects.all()
    sub_categories = SubCategory.objects.all()

    return render(request, 'pages/categories.html', {
        'categories': categories,
        'sub_categories': sub_categories
    })


def category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug, is_active=True)
    sub_categories_belonging_to_category = SubCategory.objects.filter(
        category__slug=category_slug, is_active=True)
    products_belonging_to_category = Product.objects.filter(
        category__slug=category_slug, is_active=True).order_by('-updated_at')

    product_unit_images = ProductUnitImage.objects.filter(
        is_product_unit_default=True, is_active=True)

    return render(request, 'pages/category.html', {
        'category': category,
        'sub_categories_belonging_to_category': sub_categories_belonging_to_category,
        'products_belonging_to_category': products_belonging_to_category,
        'product_unit_images': product_unit_images
    })


def sub_category(request, sub_category_slug):
    sub_category = get_object_or_404(
        SubCategory, slug=sub_category_slug, is_active=True)
    products_belonging_to_sub_category = Product.objects.filter(
        sub_category__slug=sub_category_slug, is_active=True).order_by('-updated_at')

    product_unit_images = ProductUnitImage.objects.filter(
        is_product_unit_default=True, is_active=True)

    return render(request, 'pages/sub_category.html', {
        'sub_category': sub_category,
        'products_belonging_to_sub_category': products_belonging_to_sub_category,
        'product_unit_images': product_unit_images
    })


def products(request):
    product_units = ProductUnit.objects.filter(is_product_default=True,
                                               is_active=True).order_by('-updated_at')
    product_unit_images = ProductUnitImage.objects.filter(
        is_product_unit_default=True, is_active=True)

    return render(request, 'pages/products.html', {
        'product_units': product_units,
        'product_unit_images': product_unit_images
    })


def product(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug, is_active=True)

    product_unit_count = ProductUnit.objects.filter(
        product__slug=product_slug).count()

    product_specifications = ProductSpecification.objects.filter(product__slug=product_slug, is_active=True).order_by(
        '-updated_at')

    # for product_specification in product_specifications:
    #     related_product_specification_values = ProductSpecificationValue.objects.filter(product_specification__slug=product_specification.slug, is_active=True).order_by(
    #         '-updated_at')

    related_product_specification_values = ProductSpecificationValue.objects.filter(product__slug=product_slug, is_active=True).order_by(
        '-updated_at')

    product_unit_images = ProductUnitImage.objects.filter(
        product__slug=product_slug, is_active=True).order_by('-is_product_unit_default')[:6]

    product_unit_image_default_for_product = ProductUnitImage.objects.filter(
        product__slug=product_slug, is_active=True).order_by('-is_product_unit_default').first()

    return render(request, 'pages/product.html', {
        'product': product,
        'product_unit_count': product_unit_count,
        'product_specifications': product_specifications,
        'product_unit_images': product_unit_images,
        'product_unit_image_default_for_product': product_unit_image_default_for_product,
        'related_product_specification_values': related_product_specification_values
    })


def lookup(request):
    if request.method == 'GET':

        query = request.GET.get('search')

        product_units = ProductUnit.objects.filter(
            Q(product__slug__icontains=query) |
            Q(product__title__icontains=query) |
            Q(product__description__icontains=query)
        )

        products_count = product_units.count()

    product_unit_images = ProductUnitImage.objects.filter(
        is_product_unit_default=True, is_active=True)

    return render(request, 'pages/lookup.html', {
        'query': query,
        'product_units': product_units,
        'products_count': products_count,
        'product_unit_images': product_unit_images
    })


def contact_us(request):
    return render(request, 'pages/contact_us.html')
