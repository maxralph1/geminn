from django import forms
from .models import Brand, Discount, Category, SubCategory, Product, ProductUnit, ProductSpecification, ProductSpecificationValue, ProductUnitImage, ProductReview


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['title', 'description', 'logo',
                  'web', 'instagram', 'twitter']

    def clean_title(self):
        title = self.cleaned_data['title']
        return title

    def clean_description(self):
        description = self.cleaned_data['description']
        return description

    def clean_logo(self):
        logo = self.cleaned_data['logo']
        return logo

    def clean_web(self):
        web = self.cleaned_data['web']
        return web

    def clean_instagram(self):
        instagram = self.cleaned_data['instagram']
        return instagram

    def clean_twitter(self):
        twitter = self.cleaned_data['twitter']
        return twitter

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'type': 'text', 'name': 'title', 'id': 'title',
                'class': 'form-control', 'placeholder': 'e.g. Nike', 'required': 'required'}
        )
        self.fields['description'].widget.attrs.update(
            {'type': 'text', 'name': 'description', 'id': 'description',
                'class': 'form-control', 'placeholder': 'e.g. Nike is footwear brand', 'required': 'required'}
        )
        self.fields['logo'].widget.attrs.update(
            {'type': 'file', 'name': 'logo', 'id': 'logo',
                'class': 'form-control', 'placeholder': 'Brand logo'}
        )
        self.fields['web'].widget.attrs.update(
            {'type': 'text', 'name': 'web', 'id': 'web',
                'class': 'form-control', 'placeholder': 'e.g. https://www.johndoe.com'}
        )
        self.fields['instagram'].widget.attrs.update(
            {'type': 'text', 'name': 'instagram', 'id': 'instagram',
                'class': 'form-control', 'placeholder': 'e.g. https://instagram.com/johndoe/'}
        )
        self.fields['twitter'].widget.attrs.update(
            {'type': 'text', 'name': 'twitter', 'id': 'twitter',
                'class': 'form-control', 'placeholder': 'e.g. https://twitter.com/johndoe/'}
        )


class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = ['title', 'code', 'description', 'value',
                  'value_unit', 'usable_once']

    def clean_title(self):
        title = self.cleaned_data['title']
        return title

    def clean_code(self):
        code = self.cleaned_data['code']
        return code

    def clean_description(self):
        description = self.cleaned_data['description']
        return description

    def clean_value(self):
        value = self.cleaned_data['value']
        return value

    def clean_value_unit(self):
        value_unit = self.cleaned_data['value_unit']
        return value_unit

    def clean_usable_once(self):
        usable_once = self.cleaned_data['usable_once']
        return usable_once

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'type': 'text', 'name': 'title', 'id': 'title',
                'class': 'form-control', 'placeholder': 'e.g. Summer Discount', 'required': 'required'}
        )
        self.fields['code'].widget.attrs.update(
            {'type': 'text', 'name': 'code', 'id': 'code',
                'class': 'form-control', 'placeholder': 'e.g. SUMMER2023', 'required': 'required'}
        )
        self.fields['description'].widget.attrs.update(
            {'type': 'text', 'name': 'description', 'id': 'description',
                'class': 'form-control', 'placeholder': 'e.g. This is a discount code for summer purchases.', 'required': 'required'}
        )
        self.fields['value'].widget.attrs.update(
            {'type': 'text', 'name': 'value', 'id': 'value',
                'class': 'form-control', 'placeholder': 'e.g. 200', 'required': 'required'}
        )
        self.fields['value_unit'].widget.attrs.update(
            {'type': 'text', 'name': 'value_unit', 'id': 'value_unit',
                'class': 'form-select', 'placeholder': 'e.g. Percentage'}
        )
        self.fields['usable_once'].widget.attrs.update(
            {'type': 'radio', 'name': 'usable_once', 'id': 'usable_once',
                'class': 'form-check', 'placeholder': 'e.g. True'}
        )


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title', 'description']

    def clean_title(self):
        title = self.cleaned_data['title']
        return title

    def clean_description(self):
        description = self.cleaned_data['description']
        return description

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'type': 'text', 'name': 'title', 'id': 'title',
                'class': 'form-control', 'placeholder': 'Title', 'required': 'required'}
        )
        self.fields['description'].widget.attrs.update(
            {'type': 'text', 'name': 'description', 'id': 'description',
                'class': 'form-control', 'placeholder': 'Description', 'required': 'required'}
        )


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['title', 'description']

    def clean_title(self):
        title = self.cleaned_data['title']
        return title

    def clean_description(self):
        description = self.cleaned_data['description']
        return description

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'type': 'text', 'name': 'title', 'id': 'title',
                'class': 'form-control', 'placeholder': 'Title', 'required': 'required'}
        )
        self.fields['description'].widget.attrs.update(
            {'type': 'text', 'name': 'description', 'id': 'description',
                'class': 'form-control', 'placeholder': 'Description', 'required': 'required'}
        )


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'category', 'sub_category', 'brand', 'discount',
                  'retail_price', 'retail_price_unit', 'initial_discount_value', 'initial_discount_value_unit']

    def clean_title(self):
        title = self.cleaned_data['title']
        return title

    def clean_description(self):
        description = self.cleaned_data['description']
        return description

    def clean_category(self):
        category = self.cleaned_data['category']
        return category

    def clean_sub_category(self):
        sub_category = self.cleaned_data['sub_category']
        return sub_category

    def clean_brand(self):
        brand = self.cleaned_data['brand']
        return brand

    def clean_discount(self):
        discount = self.cleaned_data['discount']
        return discount

    def clean_retail_price(self):
        retail_price = self.cleaned_data['retail_price']
        return retail_price

    def clean_retail_price_unit(self):
        retail_price_unit = self.cleaned_data['retail_price_unit']
        return retail_price_unit

    def clean_initial_discount_value(self):
        initial_discount_value = self.cleaned_data['initial_discount_value']
        return initial_discount_value

    def clean_initial_discount_value_unit(self):
        initial_discount_value_unit = self.cleaned_data['initial_discount_value_unit']
        return initial_discount_value_unit

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'type': 'text', 'name': 'title', 'id': 'title',
                'class': 'form-control', 'placeholder': 'e.g. Nike Shoes', 'required': 'required'}
        )
        self.fields['description'].widget.attrs.update(
            {'type': 'text', 'name': 'description', 'id': 'description',
                'class': 'form-control', 'placeholder': 'e.g. Nike shoes is a footwear.', 'required': 'required'}
        )
        self.fields['category'].widget.attrs.update(
            {'type': 'text', 'name': 'category', 'id': 'category',
                'class': 'form-select', 'placeholder': 'Category', 'required': 'required'}
        )
        self.fields['sub_category'].widget.attrs.update(
            {'type': 'text', 'name': 'sub_category', 'id': 'sub_category',
                'class': 'form-select', 'placeholder': 'Sub-category'}
        )
        self.fields['brand'].widget.attrs.update(
            {'type': 'text', 'name': 'brand',
                'class': 'form-select', 'placeholder': 'Brand'}
        )
        self.fields['discount'].widget.attrs.update(
            {'type': 'text', 'name': 'discount', 'id': 'discount',
                'class': 'form-select', 'placeholder': 'Discount'}
        )
        self.fields['retail_price'].widget.attrs.update(
            {'type': 'text', 'name': 'retail_price', 'id': 'retail_price',
                'class': 'form-control', 'placeholder': 'e.g. 1000.00'}
        )
        self.fields['retail_price_unit'].widget.attrs.update(
            {'type': 'text', 'name': 'retail_price_unit', 'id': 'retail_price_unit',
                'class': 'form-select'}
        )
        self.fields['initial_discount_value'].widget.attrs.update(
            {'type': 'text', 'name': 'initial_discount_value', 'id': 'initial_discount_value',
                'class': 'form-control', 'placeholder': 'e.g. 1000.00'}
        )
        self.fields['initial_discount_value_unit'].widget.attrs.update(
            {'type': 'text', 'name': 'initial_discount_value_unit', 'id': 'initial_discount_value_unit',
                'class': 'form-select'}
        )


class ProductUnitForm(forms.ModelForm):
    class Meta:
        model = ProductUnit
        fields = ['title', 'sku', 'description', 'purchase_price', 'purchase_price_unit', 'retail_price',
                  'retail_price_unit', 'initial_discount_value', 'initial_discount_value_unit']

    def clean_title(self):
        title = self.cleaned_data['title']
        return title

    def clean_sku(self):
        sku = self.cleaned_data['sku']
        return sku

    def clean_description(self):
        description = self.cleaned_data['description']
        return description

    def clean_purchase_price(self):
        purchase_price = self.cleaned_data['purchase_price']
        return purchase_price

    def clean_purchase_price_unit(self):
        purchase_price_unit = self.cleaned_data['purchase_price_unit']
        return purchase_price_unit

    def clean_retail_price(self):
        retail_price = self.cleaned_data['retail_price']
        return retail_price

    def clean_retail_price_unit(self):
        retail_price_unit = self.cleaned_data['retail_price_unit']
        return retail_price_unit

    def clean_initial_discount_value(self):
        initial_discount_value = self.cleaned_data['initial_discount_value']
        return initial_discount_value

    def clean_initial_discount_value_unit(self):
        initial_discount_value_unit = self.cleaned_data['initial_discount_value_unit']
        return initial_discount_value_unit

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'type': 'text', 'name': 'title', 'id': 'title',
                'class': 'form-control', 'placeholder': 'e.g. Red', 'required': 'required'}
        )
        self.fields['sku'].widget.attrs.update(
            {'type': 'text', 'name': 'sku', 'id': 'sku',
                'class': 'form-control', 'required': 'required'}
        )
        self.fields['description'].widget.attrs.update(
            {'type': 'text', 'name': 'description', 'id': 'description',
                'class': 'form-control', 'required': 'required'}
        )
        self.fields['purchase_price'].widget.attrs.update(
            {'type': 'text', 'name': 'purchase_price', 'id': 'purchase_price',
                'class': 'form-control', 'required': 'required'}
        )
        self.fields['purchase_price_unit'].widget.attrs.update(
            {'type': 'text', 'name': 'purchase_price_unit', 'id': 'purchase_price_unit',
                'class': 'form-select', 'required': 'required'}
        )
        self.fields['retail_price'].widget.attrs.update(
            {'type': 'text', 'name': 'retail_price', 'id': 'retail_price',
                'class': 'form-control', 'required': 'required'}
        )
        self.fields['retail_price_unit'].widget.attrs.update(
            {'type': 'text', 'name': 'retail_price_unit', 'id': 'retail_price_unit',
                'class': 'form-select', 'required': 'required'}
        )
        self.fields['initial_discount_value'].widget.attrs.update(
            {'type': 'text', 'name': 'initial_discount_value', 'id': 'initial_discount_value',
                'class': 'form-control'}
        )
        self.fields['initial_discount_value_unit'].widget.attrs.update(
            {'type': 'text', 'name': 'initial_discount_value_unit', 'id': 'initial_discount_value_unit',
                'class': 'form-select'}
        )


class ProductSpecificationForm(forms.ModelForm):
    class Meta:
        model = ProductSpecification
        fields = ['title']

    def clean_title(self):
        title = self.cleaned_data['title']
        return title

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'type': 'text', 'name': 'title', 'id': 'title',
                'class': 'form-control', 'placeholder': 'Title', 'required': 'required'}
        )


class ProductSpecificationValueForm(forms.ModelForm):
    class Meta:
        model = ProductSpecificationValue
        fields = ['value']

    def clean_value(self):
        value = self.cleaned_data['value']
        return value

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['value'].widget.attrs.update(
            {'type': 'text', 'name': 'value', 'id': 'value',
                'class': 'form-control', 'placeholder': 'e.g. Red', 'required': 'required'}
        )


class ProductUnitImageForm(forms.ModelForm):
    class Meta:
        model = ProductUnitImage
        fields = ['image', 'alt_text']

    def clean_image(self):
        image = self.cleaned_data['image']
        return image

    def clean_alt_text(self):
        alt_text = self.cleaned_data['alt_text']
        return alt_text

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update(
            {'type': 'file', 'name': 'image', 'id': 'image',
                'class': 'form-control', 'placeholder': 'e.g. img/hsg.jpg'}
        )
        self.fields['alt_text'].widget.attrs.update(
            {'type': 'text', 'name': 'alt_text', 'id': 'alt_text',
                'class': 'form-control', 'placeholder': 'e.g. img/hsg.jpg'}
        )


class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['title', 'content', 'stars']

    def clean_title(self):
        title = self.cleaned_data['title']
        return title

    def clean_content(self):
        content = self.cleaned_data['content']
        return content

    def clean_stars(self):
        stars = self.cleaned_data['stars']
        return stars

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'type': 'text', 'name': 'title', 'id': 'title',
                'class': 'form-control', 'placeholder': 'Title'}
        )
        self.fields['content'].widget.attrs.update(
            {'type': 'text', 'name': 'content', 'id': 'content',
                'class': 'form-control', 'placeholder': 'Content'}
        )
        self.fields['stars'].widget.attrs.update(
            {'type': 'text', 'name': 'stars', 'id': 'stars',
                'class': 'form-control', 'placeholder': 'Stars'}
        )
