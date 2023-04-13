from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from .models import Brand, Discount, Category, SubCategory, Product, ProductUnit, ProductUnitImage, ProductSpecification, ProductSpecificationValue, ProductReview
from .forms import BrandForm, DiscountForm, CategoryForm, SubCategoryForm, ProductForm, ProductUnitForm, ProductSpecificationForm, ProductSpecificationValueForm, ProductUnitImageForm, ProductReviewForm


def home(request):
    products = Product.objects.prefetch_related(
        'product_image').filter(is_active=True)
    return render(request, 'inventory/index.html', {'products': products})


# Brands

@login_required
def brands(request):
    brands = Brand.objects.filter(is_active=True).order_by('-updated_at')
    return render(request, 'inventory/brands/index.html', {'brands': brands})


@login_required
def add_brand(request):
    if request.method == 'POST':
        brand_form = BrandForm(request.POST, request.FILES)

        if brand_form.is_valid():
            brand = brand_form.save(commit=False)
            brand.title = brand_form.cleaned_data['title']
            brand.slug = slugify(
                brand_form.cleaned_data['title'], allow_unicode=False)
            brand.description = brand_form.cleaned_data['description']
            brand.logo = brand_form.cleaned_data['logo']
            brand.web = brand_form.cleaned_data['web']
            brand.instagram = brand_form.cleaned_data['instagram']
            brand.twitter = brand_form.cleaned_data['twitter']
            brand.added_by = request.user
            brand.save()
            messages.success(request, brand.title + ' added')
            return redirect('inventory:view_brand', brand.slug)
        else:
            return HttpResponse('Error handler content', status=400)
    else:
        brand_form = BrandForm()

    return render(request, 'inventory/brands/add.html', {'form': brand_form})


@login_required
def view_brand(request, brand_slug):
    brand = get_object_or_404(Brand, slug=brand_slug, is_active=True)

    return render(request, 'inventory/brands/brand.html', {'brand': brand})


@login_required
def update_brand(request, brand_slug):
    if request.method == 'POST':
        brand = Brand.objects.get(slug=brand_slug)
        brand_form = BrandForm(
            instance=brand, data=request.POST, files=request.FILES)
        if brand_form.is_valid():
            brand_form.save()
            return redirect('inventory:view_brand', brand_slug)
    else:
        brand = Brand.objects.get(slug=brand_slug)
        brand_form = BrandForm(instance=brand)
    return render(request, 'inventory/brands/edit.html', {'brand': brand, 'form': brand_form})


@login_required
def delete_brand(request, brand_slug):
    brand = Brand.objects.get(slug=brand_slug)
    brand.is_active = False
    brand.deleted_at = datetime.now()
    brand.save()
    messages.success(request, 'Brand removed')
    return HttpResponseRedirect(reverse('inventory:brands'))


# Discounts

@login_required
def discounts(request):
    discounts = Discount.objects.filter(is_active=True).order_by('-updated_at')
    return render(request, 'inventory/discounts/index.html', {'discounts': discounts})


@login_required
def add_discount(request):
    if request.method == 'POST':
        discount_form = DiscountForm(request.POST)

        if discount_form.is_valid():
            discount = discount_form.save(commit=False)
            discount.title = discount_form.cleaned_data['title']
            discount.slug = slugify(
                discount_form.cleaned_data['title'], allow_unicode=False)
            discount.code = discount_form.cleaned_data['code']
            discount.description = discount_form.cleaned_data['description']
            discount.value = discount_form.cleaned_data['value']
            discount.value_unit = discount_form.cleaned_data['value_unit']
            discount.usable_once = discount_form.cleaned_data['usable_once']
            discount.added_by = request.user
            discount.save()
            messages.success(request, discount.title + ' added')
            return redirect('inventory:view_discount', discount.slug)
        else:
            return HttpResponse('Error handler content', status=400)
    else:
        discount_form = DiscountForm()

    return render(request, 'inventory/discounts/add.html', {'form': discount_form})


@login_required
def view_discount(request, discount_slug):
    discount = get_object_or_404(Discount, slug=discount_slug, is_active=True)

    return render(request, 'inventory/discounts/discount.html', {'discount': discount})


@login_required
def update_discount(request, discount_slug):
    if request.method == 'POST':
        discount = Discount.objects.get(slug=discount_slug)
        discount_form = DiscountForm(
            instance=discount, data=request.POST, files=request.FILES)
        if discount_form.is_valid():
            discount_form.save()
            return redirect('inventory:view_discount', discount_slug)
    else:
        discount = Discount.objects.get(slug=discount_slug)
        discount_form = DiscountForm(instance=discount)
    return render(request, 'inventory/discounts/edit.html', {'discount': discount, 'form': discount_form})


@login_required
def delete_discount(request, discount_slug):
    discount = Discount.objects.get(slug=discount_slug)
    discount.is_active = False
    discount.deleted_at = datetime.now()
    discount.save()
    messages.success(request, 'Discount removed')
    return HttpResponseRedirect(reverse('inventory:discounts'))


# Categories

@login_required
def categories(request):
    categories = Category.objects.filter(
        is_active=True).order_by('-updated_at')
    return render(request, 'inventory/categories/index.html', {'categories': categories})


@login_required
def add_category(request):
    if request.method == 'POST':
        category_form = CategoryForm(request.POST)

        if category_form.is_valid():
            category = category_form.save(commit=False)
            category.title = category_form.cleaned_data['title']
            category.slug = slugify(
                category_form.cleaned_data['title'], allow_unicode=False)
            category.description = category_form.cleaned_data['description']
            category.added_by = request.user
            category.save()
            # return HttpResponseRedirect(reverse('inventory:categories'))
            # return redirect('checkout:delivery_address')
            messages.success(request, category.title + ' added')
            return redirect('inventory:view_category', category.slug)
        else:
            return HttpResponse('Error handler content', status=400)
    else:
        category_form = CategoryForm()

    return render(request, 'inventory/categories/add.html', {'form': category_form})


@login_required
def view_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug, is_active=True)
    # sub_categories = get_object_or_404(
    #     SubCategory, category=category.id, is_active=True).order_by('-updated_at')
    sub_categories = SubCategory.objects.filter(category=category.id, is_active=True).order_by(
        '-updated_at')
    sub_category_form = SubCategoryForm()

    if sub_categories:
        return render(request, 'inventory/categories/category.html', {'category': category, 'sub_categories': sub_categories, 'form': sub_category_form})
    else:
        return render(request, 'inventory/categories/category.html', {'category': category, 'form': sub_category_form})


@login_required
def update_category(request, category_slug):
    if request.method == 'POST':
        category = Category.objects.get(slug=category_slug)
        category_form = CategoryForm(instance=category, data=request.POST)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('inventory:categories'))
    else:
        category = Category.objects.get(slug=category_slug)
        category_form = CategoryForm(instance=category)
    return render(request, 'inventory/categories/edit.html', {'category': category, 'form': category_form})


@login_required
def delete_category(request, category_slug):
    Category.objects.filter(slug=category_slug).delete()
    messages.success(request, 'Category removed')
    return redirect('inventory:categories')


# Sub-Categories

@login_required
def add_sub_category(request, category_slug):
    category = Category.objects.get(slug=category_slug)

    if request.method == 'POST':
        sub_category_form = SubCategoryForm(request.POST)

        if sub_category_form.is_valid():
            sub_category = sub_category_form.save(commit=False)
            sub_category.title = sub_category_form.cleaned_data['title']
            sub_category.slug = slugify(
                sub_category_form.cleaned_data['title'], allow_unicode=False)
            sub_category.description = sub_category_form.cleaned_data['description']
            sub_category.category = category
            sub_category.added_by = request.user
            sub_category.save()
            messages.success(request, sub_category.title + ' added')
            return redirect('inventory:view_category', category_slug)
        else:
            return HttpResponse('Error handler content', status=400)
    else:
        sub_category_form = SubCategoryForm()

    return render(request, 'inventory/categories/category.html', {'category': category, 'form': sub_category_form})


@login_required
def view_sub_category(request, category_slug, sub_category_slug):
    sub_category = get_object_or_404(
        SubCategory, slug=sub_category_slug, category__slug=category_slug, is_active=True)

    return render(request, 'inventory/sub_categories/sub_category.html', {'sub_category': sub_category, 'category_slug': category_slug})


@login_required
def update_sub_category(request, category_slug, sub_category_slug):
    if request.method == 'POST':
        sub_category = SubCategory.objects.get(
            slug=sub_category_slug, category__slug=category_slug)
        sub_category_form = SubCategoryForm(
            instance=sub_category, data=request.POST)
        if sub_category_form.is_valid():
            sub_category_form.save()
            return redirect('inventory:view_sub_category', category_slug, sub_category_slug)
    else:
        sub_category = SubCategory.objects.get(slug=sub_category_slug)
        sub_category_form = SubCategoryForm(instance=sub_category)
    return render(request, 'inventory/sub_categories/edit.html', {'sub_category': sub_category, 'form': sub_category_form})


@login_required
def delete_sub_category(request, category_slug, sub_category_slug):
    sub_category = SubCategory.objects.get(
        slug=sub_category_slug, category__slug=category_slug)
    sub_category.is_active = False
    sub_category.deleted_at = datetime.now()
    sub_category.save()
    messages.success(request, 'Sub-Category removed')
    return redirect('inventory:view_category', category_slug)


# Products

@login_required
def products(request):
    products = Product.objects.filter(
        is_active=True).order_by('-updated_at')
    return render(request, 'inventory/products/index.html', {'products': products})


@login_required
def add_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST)

        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.title = product_form.cleaned_data['title']
            product.slug = slugify(
                product_form.cleaned_data['title'] + str(datetime.now()), allow_unicode=False)
            product.description = product_form.cleaned_data['description']
            product.category = product_form.cleaned_data['category']
            product.sub_category = product_form.cleaned_data['sub_category']
            product.brand = product_form.cleaned_data['brand']
            product.discount = product_form.cleaned_data['discount']
            product.retail_price = product_form.cleaned_data['retail_price']
            product.retail_price_unit = product_form.cleaned_data['retail_price_unit']
            product.initial_discount_value = product_form.cleaned_data['initial_discount_value']
            product.initial_discount_value_unit = product_form.cleaned_data[
                'initial_discount_value_unit']

            product.added_by = request.user
            product.save()
            messages.success(request, product.title + ' added')
            return redirect('inventory:view_product', product.slug)
        else:
            return HttpResponse('Error handler content', status=400)
    else:
        product_form = ProductForm()

    return render(request, 'inventory/products/add.html', {'form': product_form})


@login_required
def view_product(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug, is_active=True)
    product_units = ProductUnit.objects.filter(
        product=product.id, is_active=True).order_by('-is_product_default', '-updated_at')
    product_unit_form = ProductUnitForm()

    product_specifications = ProductSpecification.objects.filter(product=product.id, is_active=True).order_by(
        '-updated_at')
    product_specification_form = ProductSpecificationForm()

    return render(request, 'inventory/products/product.html', {'product': product, 'product_units': product_units, 'product_specifications': product_specifications, 'product_unit_form': product_unit_form, 'product_specification_form': product_specification_form})


@login_required
def update_product(request, product_slug):
    if request.method == 'POST':
        product = Product.objects.get(slug=product_slug)
        product_form = ProductForm(instance=product, data=request.POST)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('inventory:products'))
    else:
        product = Product.objects.get(slug=product_slug)
        product_form = ProductForm(instance=product)
    return render(request, 'inventory/products/edit.html', {'product': product, 'form': product_form})


@login_required
def delete_product(request, product_slug):
    product = Product.objects.get(
        slug=product_slug)
    product.is_active = False
    product.deleted_at = datetime.now()
    product.save()
    messages.success(request, 'Product removed')
    return redirect('inventory:products')


# Product Units

@login_required
def add_product_unit(request, product_slug):
    product = Product.objects.get(slug=product_slug)

    product_unit_default_exists = ProductUnit.objects.filter(
        product__slug=product_slug, is_product_default=True).exists()

    if request.method == 'POST':
        product_unit_form = ProductUnitForm(request.POST)

        if product_unit_form.is_valid():
            product_unit = product_unit_form.save(commit=False)
            product_unit.title = product_unit_form.cleaned_data['title']
            product_unit.description = product_unit_form.cleaned_data['description']
            product_unit.product = product

            if product_unit_default_exists == False:
                product_unit.is_product_default = True
            else:
                product_unit.is_product_default = False

            product_unit.slug = slugify(
                str(product_unit.title) + str(product_unit.product) + str(datetime.now()), allow_unicode=False)
            product_unit.added_by = request.user
            product_unit.save()
            messages.success(request, product_unit.title + ' added')
            return redirect('inventory:view_product', product_slug)
        else:
            return HttpResponse('Error handler content', status=400)
    else:
        product_unit_form = ProductUnitForm()

    return render(request, 'inventory/products/product.html', {'product': product, 'form': product_unit_form})


@login_required
def view_product_unit(request, product_slug, product_unit_slug):
    product_unit = get_object_or_404(
        ProductUnit, slug=product_unit_slug, product__slug=product_slug, is_active=True)

    product = get_object_or_404(
        Product, slug=product_slug, is_active=True)

    product_unit_images = ProductUnitImage.objects.filter(product_unit__slug=product_unit_slug, is_active=True).order_by(
        '-is_product_unit_default', '-updated_at')
    product_image_form = ProductUnitImageForm()

    product_specifications = ProductSpecification.objects.filter(product__slug=product_slug, is_active=True).order_by(
        '-updated_at')

    product_specification_values = ProductSpecificationValue.objects.filter(product__slug=product_slug, product_unit__slug=product_unit_slug, is_active=True).order_by(
        '-updated_at')
    product_specification_form = ProductSpecificationForm()
    product_specification_value_form = ProductSpecificationValueForm()

    return render(request, 'inventory/product_units/product_unit.html', {'product_unit': product_unit, 'product': product, 'product_slug': product_slug, 'product_unit_images': product_unit_images, 'product_image_form': product_image_form, 'product_specifications': product_specifications, 'product_specification_values': product_specification_values,  'product_specification_form': product_specification_form, 'product_specification_value_form': product_specification_value_form})


@login_required
def update_product_unit(request, product_slug, product_unit_slug):
    if request.method == 'POST':
        product_unit = ProductUnit.objects.get(
            slug=product_unit_slug, product__slug=product_slug)
        product_unit_form = ProductUnitForm(
            instance=product_unit, data=request.POST)
        if product_unit_form.is_valid():
            product_unit_form.save()
            return redirect('inventory:view_product_unit', product_slug, product_unit_slug)
    else:
        product_unit = ProductUnit.objects.get(
            slug=product_unit_slug, product__slug=product_slug)
        product_unit_form = ProductUnitForm(instance=product_unit)
    return render(request, 'inventory/product_units/edit.html', {'product_unit': product_unit, 'product_unit_form': product_unit_form})


@login_required
def set_is_default_product_unit(request, product_slug, product_unit_slug):
    ProductUnit.objects.filter(
        product__slug=product_slug, is_product_default=True).update(is_product_default=False)

    ProductUnit.objects.filter(
        slug=product_unit_slug, product__slug=product_slug, is_product_default=False).update(is_product_default=True)

    return redirect('inventory:view_product', product_slug)


@login_required
def delete_product_unit(request, product_slug, product_unit_slug):
    product_unit = ProductUnit.objects.get(
        slug=product_unit_slug, product__slug=product_slug)
    product_unit.is_active = False
    product_unit.deleted_at = datetime.now()
    product_unit.save()
    messages.success(request, 'Product Unit removed')
    return redirect('inventory:view_product_unit', product_slug, product_unit_slug)


# Product Specifications

@login_required
def add_product_specification(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    product_count = ProductSpecification.objects.filter(
        product__slug=product_slug, is_active=True).count()

    if product_count < 10:
        if request.method == 'POST':
            product_specification_form = ProductSpecificationForm(request.POST)

            if product_specification_form.is_valid():
                product_specification = product_specification_form.save(
                    commit=False)
                product_specification.title = product_specification_form.cleaned_data['title']
                product_specification.slug = slugify(
                    product_specification_form.cleaned_data['title'], allow_unicode=False)
                product_specification.product = product
                product_specification.added_by = request.user

                if ProductSpecification.objects.filter(slug=product_specification.slug, product__slug=product_slug).exists():
                    messages.warning(
                        request, 'You cannot add duplicate copies of product specification to a product. You may update the existing one instead.')
                    return redirect('inventory:view_product', product_slug)
                else:

                    product_specification.save()
                messages.success(
                    request, product_specification.title + ' added')
                return redirect('inventory:view_product', product_slug)
            else:
                return HttpResponse('Error handler content', status=400)
        else:
            product_specification_form = ProductSpecificationForm()
    else:
        messages.warning(request, product.title +
                         ' could not be added. A product must not exceed 10 specifications.')
        return redirect('inventory:view_product', product.slug)
        # product_specification_form = ProductSpecificationForm()

    return render(request, 'inventory/products/product.html', {'product': product, 'product_specification_form': product_specification_form})


@login_required
def update_product_specification(request, product_slug, product_specification_slug):
    if request.method == 'POST':
        product_specification = ProductSpecification.objects.get(
            slug=product_specification_slug, product__slug=product_slug)
        product_specification_form = ProductSpecificationForm(
            instance=product_specification, data=request.POST)
        if product_specification_form.is_valid():
            product_specification_form.save()
            return redirect('inventory:view_product', product_slug)
    else:

        return redirect('inventory:view_product', product_slug)


@login_required
def delete_product_specification(request, product_slug, product_specification_slug):
    product_specification = ProductSpecification.objects.get(
        slug=product_specification_slug, product__slug=product_slug)
    product_specification.is_active = False
    product_specification.deleted_at = datetime.now()
    product_specification.save()
    messages.success(request, 'Product Specification removed')
    return redirect('inventory:view_product', product_slug)


# Product Specification Value

@login_required
def add_product_specification_value(request, product_slug, product_unit_slug, product_specification_slug):
    product = get_object_or_404(
        Product, slug=product_slug, is_active=True)
    product_unit = get_object_or_404(
        ProductUnit, slug=product_unit_slug, product__slug=product_slug, is_active=True)
    product_specification = get_object_or_404(
        ProductSpecification, slug=product_specification_slug, product__slug=product_slug, is_active=True)

    if request.method == 'POST':

        product_specification_value_form = ProductSpecificationValueForm(
            request.POST)

        if product_specification_value_form.is_valid():
            product_specification_value = product_specification_value_form.save(
                commit=False)
            product_specification_value.value = product_specification_value_form.cleaned_data[
                'value']
            product_specification_value.product = product
            product_specification_value.product_unit = product_unit
            product_specification_value.product_specification = product_specification
            product_specification_value.slug = slugify(str(product_specification_value.value) + str(product_specification_value.product) + str(
                product_specification_value.product_unit) + str(product_specification_value.product_specification), allow_unicode=False)
            product_specification_value.added_by = request.user

            if ProductSpecificationValue.objects.filter(product__slug=product_slug, product_unit__slug=product_unit_slug, product_specification__slug=product_specification_slug).exists():
                messages.warning(
                    request, 'You cannot add product specification value to a product specification with an existing product specification value. You may update the existing value instead.')
                return redirect('inventory:view_product_unit', product_slug, product_unit_slug)
            else:
                product_specification_value.save()
            messages.success(
                request, product_specification_value.value + ' added to product specification ' + product_specification.title + ' of product ' + product.title)
            return redirect('inventory:view_product_unit', product_slug, product_unit_slug)
        else:
            return HttpResponse('Error handler content', status=400)
    else:
        product_specification_value_form = ProductSpecificationForm()
        product_image_form = ProductUnitImageForm()

    return render(request, 'inventory/product_units/product_unit.html', {'product': product, 'product_unit': product_unit, 'product_specification': product_specification, 'product_specification_value_form': product_specification_value_form, 'product_image_form': product_image_form})


@login_required
def update_product_specification_value(request, product_slug, product_unit_slug, product_specification_slug, product_specification_value_slug):
    if request.method == 'POST':
        product_specification_value = ProductSpecificationValue.objects.get(
            slug=product_specification_value_slug, product__slug=product_slug, product_unit__slug=product_unit_slug, product_specification__slug=product_specification_slug)
        product_specification_value_form = ProductSpecificationValueForm(
            instance=product_specification_value, data=request.POST)
        if product_specification_value_form.is_valid():
            product_specification_value_form.save()
            return redirect('inventory:view_product_unit', product_slug, product_unit_slug)
    else:
        return redirect('inventory:view_product_unit', product_slug, product_unit_slug)


@login_required
def delete_product_specification_value(request, product_slug, product_unit_slug, product_specification_slug, product_specification_value_slug):
    product_specification_value = get_object_or_404(
        ProductSpecificationValue, slug=product_specification_value_slug, product__slug=product_slug, product_unit__slug=product_unit_slug, product_specification__slug=product_specification_slug, is_active=True)
    product_specification_value.is_active = False
    product_specification_value.deleted_at = datetime.now()
    product_specification_value.save()
    messages.success(request, 'Product Specification Value removed')
    return redirect('inventory:view_product_unit', product_slug, product_unit_slug)


# Product Review

@login_required
def add_product_review(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    product_review_by_user_exists = ProductReview.objects.get(
        product__slug=product_slug, added_by=request.user, is_active=True).exists()

    if request.method == 'POST':
        if product_review_by_user_exists:
            messages.warning(
                request, 'User is allowed to add only one review per product. You may wish to update \your existing review instead.')
            return redirect('inventory:view_product', product.slug)
        else:
            product_review_form = ProductReviewForm(request.POST)

            if product_review_form.is_valid():
                product_review = product_review_form.save(
                    commit=False)
                product_review.title = product_review_form.cleaned_data['title']
                product_review.content = product_review_form.cleaned_data['content']
                product_review.slug = slugify(
                    product_review.title + product_review.content, allow_unicode=False)
                product_review.product = product
                product_review.added_by = request.user
                product_review.save()
                messages.success(
                    request, 'Review ' + product_review.title + ' added')
                return redirect('inventory:view_product', product_slug)
            else:
                return HttpResponse('Error handler content', status=400)
    else:
        product_review_form = ProductReviewForm()

    return redirect('inventory:view_product', product.slug)


@login_required
def update_product_review(request, product_slug, product_review_slug):
    product_review = get_object_or_404(
        ProductReview, slug=product_review_slug, product__slug=product_slug, is_active=True)

    if request.method == 'POST':
        if product_review.user != request.user:
            messages.warning(
                request, 'User is allowed to update only reviews belonging to them.')
            return redirect('inventory:view_product', product_slug)
        else:
            product_review_form = ProductReviewForm(
                instance=product_review, data=request.POST)
            if product_review_form.is_valid():
                product_review_form.save()
                return redirect('inventory:view_product', product_slug)
    else:

        return redirect('inventory:view_product', product_slug)


@login_required
def delete_product_review(request, product_slug, product_review_slug):
    product_review = get_object_or_404(
        ProductReview, slug=product_review_slug, product__slug=product_slug, is_active=True)

    if product_review.user != request.user:
        messages.warning(
            request, 'User is allowed to update only reviews belonging to them.')
        return redirect('inventory:view_product', product_slug)
    else:
        product_review = ProductReview.objects.get(
            slug=product_review_slug, product__slug=product_slug)
        product_review.is_active = False
        product_review.deleted_at = datetime.now()
        product_review.save()
        messages.success(request, 'Product Review removed')
    return redirect('inventory:view_product', product_slug)


# Product Unit Image

@login_required
def add_product_unit_image(request, product_slug, product_unit_slug):
    product = get_object_or_404(
        Product, slug=product_slug, is_active=True)
    product_unit = get_object_or_404(
        ProductUnit, slug=product_unit_slug, product__slug=product_slug, is_active=True)

    product_unit_image_count = ProductUnitImage.objects.filter(
        product_unit__slug=product_unit_slug, is_active=True).count()

    if request.method == 'POST':

        if product_unit_image_count >= 6:
            messages.warning(
                request, product_unit.title + ' cannot have more than 6 images. Try updating the older images instead.')
            return redirect('inventory:view_product_unit', product_slug, product_unit_slug)
        else:
            product_unit_image_form = ProductUnitImageForm(
                request.POST, request.FILES)

            if product_unit_image_form.is_valid():
                product_unit_image = product_unit_image_form.save(
                    commit=False)
                product_unit_image.image = product_unit_image_form.cleaned_data[
                    'image']
                product_unit_image.alt_text = product_unit_image_form.cleaned_data[
                    'alt_text']
                product_unit_image.product = product
                product_unit_image.product_unit = product_unit
                product_unit_image.slug = slugify(
                    str(product_unit_image.image) + str(product_unit_image.product) + str(product_unit_image.product_unit) + str(product_unit_image.alt_text) + str(datetime.now()), allow_unicode=False)

                product_unit_image.added_by = request.user
                product_unit_image.save()
                messages.success(
                    request, 'Image added to product unit ' + product_unit.title + ' of product ' + product.title)
                return redirect('inventory:view_product_unit', product_slug, product_unit_slug)
            else:
                return HttpResponse('Error handler content', status=400)
    else:
        product_specification_value_form = ProductSpecificationForm()
        product_image_form = ProductUnitImageForm(request.POST, request.FILES)

    return render(request, 'inventory/product_units/product_unit.html', {'product': product, 'product_unit': product_unit, 'product_specification_value_form': product_specification_value_form, 'product_image_form': product_image_form})


@login_required
def update_product_unit_image(request, product_slug, product_unit_slug, product_unit_image_slug):
    if request.method == 'POST':
        product_unit_image = ProductUnitImage.objects.get(
            slug=product_unit_image_slug, product__slug=product_slug, product_unit__slug=product_unit_slug)
        product_unit_image_form = ProductUnitImageForm(
            instance=product_unit_image, data=request.POST)
        if product_unit_image_form.is_valid():
            product_unit_image_form.save()
            return redirect('inventory:view_product_unit', product_slug, product_unit_slug)
    else:
        return redirect('inventory:view_product_unit', product_slug, product_unit_slug)


@login_required
def set_default_image_for_product_unit(request, product_slug, product_unit_slug, product_unit_image_slug):
    ProductUnitImage.objects.filter(product_unit__slug=product_unit_slug,
                                    is_product_unit_default=True).update(is_product_unit_default=False)
    ProductUnitImage.objects.filter(
        slug=product_unit_image_slug, product_unit__slug=product_unit_slug, is_product_unit_default=False).update(is_product_unit_default=True)

    return redirect('inventory:view_product_unit', product_slug, product_unit_slug)


@login_required
def delete_product_unit_image(request, product_slug, product_unit_slug, product_unit_image_slug):
    product_unit_image = get_object_or_404(
        ProductUnitImage, slug=product_unit_image_slug, product__slug=product_slug, product_unit__slug=product_unit_slug, is_active=True)
    product_unit_image.is_active = False
    product_unit_image.deleted_at = datetime.now()
    product_unit_image.save()
    messages.success(request, 'Product Unit Image removed')
    return redirect('inventory:view_product_unit', product_slug, product_unit_slug)
