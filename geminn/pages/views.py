from django.shortcuts import get_object_or_404, redirect, render

from inventory.models import Product, ProductUnit, ProductUnitImage, ProductSpecification, ProductSpecificationValue, Category


def index(request):
    product_units = ProductUnit.objects.prefetch_related(
        'product_unit_image').filter(is_active=True).order_by('?')[:1]
    return render(request, 'pages/index.html', {'product_units': product_units})


def categories(request):
    return render(request, 'pages/categories.html')


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


def contact_us(request):
    return render(request, 'pages/contact_us.html')
