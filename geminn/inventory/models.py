from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from accounts.models import UserModel


class Brand(models.Model):
    title = models.CharField(
        verbose_name=_('Brand Title'),
        help_text=_('Required and unique'),
        max_length=255,
        unique=True,
    )
    slug = models.SlugField(verbose_name=_(
        'Brand safe URL'), max_length=255, unique=True)
    description = models.CharField(
        verbose_name=_('Brand Description'),
        help_text=_('Required and unique'),
        max_length=255,
    )
    logo = models.ImageField(
        verbose_name=_('Brand Logo'),
        help_text=_('Upload logo image'),
        upload_to='images/brands/',
        default='images/default.png',
    )
    web = models.CharField(
        verbose_name=_('Brand Website'),
        max_length=255,
    )
    instagram = models.CharField(
        verbose_name=_('Brand Instagram'),
        max_length=255,
    )
    twitter = models.CharField(
        verbose_name=_('Brand Twitter'),
        max_length=255,
    )
    added_by = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    is_active = models.BooleanField(
        verbose_name=_('Brand visibility'),
        help_text=_('Change brand visibility'),
        default=True,
    )
    created_at = models.DateTimeField(
        _('Created at'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')

    def get_absolute_url(self):
        return reverse('inventory:brands', args=[self.slug])

    def __str__(self):
        return self.title


class Discount(models.Model):
    DISCOUNT_CHOICES = [
        ('PERC', 'Percent'),
        ('USD', 'USD'),
    ]

    title = models.CharField(
        verbose_name=_('Title'),
        help_text=_('Required'),
        max_length=255,
    )
    slug = models.SlugField(verbose_name=_(
        'Category safe URL'), max_length=255, unique=True)
    code = models.SlugField(max_length=255)
    description = models.CharField(verbose_name=_(
        'Discount description'), help_text=_('Not Required'), max_length=255, blank=True)
    value = models.DecimalField(
        verbose_name=_('Discount Value'),
        help_text=_('Discount value'),
        null=True,
        blank=True,
        max_digits=9,
        decimal_places=2
    )
    value_unit = models.CharField(
        choices=DISCOUNT_CHOICES,
        verbose_name=_('Value unit'),
        help_text=_('Required'),
        max_length=255
    )
    usable_once = models.BooleanField(
        verbose_name=_('Usable Once?'),
        help_text=_('Usable once?'),
        default=False,
    )
    used_at = models.DateTimeField(null=True, blank=True)
    used_by = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(
        verbose_name=_('Discount visibility'),
        help_text=_('Change discount visibility'),
        default=True,
    )
    created_at = models.DateTimeField(
        _('Created at'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('Discount')
        verbose_name_plural = _('Discounts')

    def get_absolute_url(self):
        return reverse('inventory:discount_detail', args=[self.slug])

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(
        verbose_name=_('Category Title'),
        help_text=_('Required and unique'),
        max_length=255,
        unique=True,
    )
    slug = models.SlugField(verbose_name=_(
        'Category safe URL'), max_length=255, unique=True)
    description = models.CharField(
        verbose_name=_('Category Description'),
        help_text=_('Required and unique'),
        max_length=255,
    )
    added_by = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    is_active = models.BooleanField(
        verbose_name=_('Category visibility'),
        help_text=_('Change category visibility'),
        default=True,
    )
    created_at = models.DateTimeField(
        _('Created at'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def get_absolute_url(self):
        return reverse('inventory:categories', args=[self.slug])

    def __str__(self):
        return self.title


class SubCategory(models.Model):
    title = models.CharField(
        verbose_name=_('Sub-category Title'),
        help_text=_('Required and unique'),
        max_length=255,
        unique=True,
    )
    slug = models.SlugField(verbose_name=_(
        'Sub-category safe URL'), max_length=255, unique=True)
    description = models.CharField(
        verbose_name=_('Sub-category Description'),
        help_text=_('Required and unique'),
        max_length=255,
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    added_by = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    is_active = models.BooleanField(
        verbose_name=_('Sub-category visibility'),
        help_text=_('Change sub-category visibility'),
        default=True,
    )
    created_at = models.DateTimeField(
        _('Created at'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _('Sub-category')
        verbose_name_plural = _('Sub-categories')

    def get_absolute_url(self):
        return reverse('inventory:sub_categories', args=[self.category, self.slug])

    def __str__(self):
        return self.title


class Product(models.Model):
    RETAIL_PRICE_UNIT_CHOICES = [
        ('EUR', 'Euro'),
        ('USD', 'USD'),
    ]
    DISCOUNT_VALUE_UNIT_CHOICES = [
        ('EUR', 'Euro'),
        ('USD', 'USD'),
        ('PERC', 'Percent'),
    ]

    title = models.CharField(
        verbose_name=_('Product title'),
        help_text=_('Required'),
        max_length=255,
    )
    slug = models.SlugField(verbose_name=_(
        'Category safe URL'), max_length=255, unique=True)
    description = models.TextField(verbose_name=_(
        'Product description'), help_text=_('Not required'), null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE, null=True, blank=True)
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, null=True, blank=True)
    discount = models.ForeignKey(Discount, verbose_name=_(
        'Discount (if any) — (select discount code)'), on_delete=models.CASCADE, null=True, blank=True)
    retail_price = models.DecimalField(
        verbose_name=_('Retail Price'),
        null=True,
        blank=True,
        max_digits=9,
        decimal_places=2
    )
    retail_price_unit = models.CharField(
        choices=RETAIL_PRICE_UNIT_CHOICES,
        verbose_name=_('Retail Price Value Unit'),
        help_text=_('Required'),
        max_length=255,
        null=True,
        blank=True
    )
    initial_discount_value = models.DecimalField(
        verbose_name=_('Initial Discount Value (if any)'),
        help_text=_('Required'),
        null=True,
        blank=True,
        max_digits=9,
        decimal_places=2
    )
    initial_discount_value_unit = models.CharField(
        choices=DISCOUNT_VALUE_UNIT_CHOICES,
        verbose_name=_('Initial Discount Value Unit'),
        help_text=_('Required'),
        max_length=255,
        null=True,
        blank=True
    )
    users_favorite = models.ManyToManyField(
        UserModel, related_name='user_favorite', null=True, blank=True)
    added_by = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    is_active = models.BooleanField(
        verbose_name=_('Product visibility'),
        help_text=_('Change product visibility'),
        default=True,
    )
    created_at = models.DateTimeField(
        _('Created at'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def get_absolute_url(self):
        return reverse('inventory:view_product', args=[self.slug])

    def __str__(self):
        return self.title


class ProductUnit(models.Model):
    PURCHASE_PRICE_UNIT_CHOICES = [
        ('EUR', 'Euro'),
        ('USD', 'USD'),
    ]
    RETAIL_PRICE_UNIT_CHOICES = [
        ('EUR', 'Euro'),
        ('USD', 'USD'),
    ]
    DISCOUNT_VALUE_UNIT_CHOICES = [
        ('EUR', 'Euro'),
        ('USD', 'USD'),
        ('PERC', 'Percent'),
    ]

    title = models.CharField(
        verbose_name=_('title'),
        help_text=_('Required'),
        max_length=255,
    )
    slug = models.SlugField(verbose_name=_(
        'Category safe URL'), max_length=255, unique=True)
    sku = models.SlugField(verbose_name=_(
        'Stock Keeping Unit'), max_length=255)
    description = models.TextField(verbose_name=_(
        'description'), help_text=_('Not Required'), blank=True)
    purchase_price = models.DecimalField(
        verbose_name=_('Purchase price'),
        null=True,
        blank=True,
        max_digits=9,
        decimal_places=2
    )
    purchase_price_unit = models.CharField(
        choices=PURCHASE_PRICE_UNIT_CHOICES,
        verbose_name=_('Purchase Price Value Unit'),
        help_text=_('Required'),
        max_length=255,
        null=True,
        blank=True
    )
    retail_price = models.DecimalField(
        verbose_name=_('Retail Price'),
        null=True,
        blank=True,
        max_digits=9,
        decimal_places=2
    )
    retail_price_unit = models.CharField(
        choices=RETAIL_PRICE_UNIT_CHOICES,
        verbose_name=_('Retail Price Value Unit'),
        help_text=_('Required'),
        max_length=255,
        null=True,
        blank=True
    )
    initial_discount_value = models.DecimalField(
        verbose_name=_('Discount Value'),
        help_text=_('Required'),
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    initial_discount_value_unit = models.CharField(
        choices=DISCOUNT_VALUE_UNIT_CHOICES,
        verbose_name=_('Initial Discount Value Unit'),
        help_text=_('Required'),
        max_length=255,
        null=True,
        blank=True
    )
    sold = models.BooleanField(
        verbose_name=_('Sold?'),
        help_text=_('Change product availability'),
        default=False,
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    is_product_default = models.BooleanField(
        verbose_name=_('Product default'),
        help_text=_('Change as product default'),
        default=False,
    )
    added_by = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    is_active = models.BooleanField(
        verbose_name=_('Product Unit visibility'),
        help_text=_('Change product unit visibility'),
        default=True,
    )
    created_at = models.DateTimeField(
        _('Created at'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('Product Unit')
        verbose_name_plural = _('Product Units')

    def get_absolute_url(self):
        return reverse('inventory:product_unit_detail', args=[self.slug])

    def __str__(self):
        return self.title


class ProductUnitImage(models.Model):
    image = models.ImageField(
        verbose_name=_('image'),
        help_text=_('Upload a product image'),
        upload_to='images/products/',
        default='images/default.png',
    )
    slug = models.SlugField(verbose_name=_(
        'Product Unit safe URL'), max_length=255, unique=True)
    alt_text = models.CharField(
        verbose_name=_('Alternative text'),
        help_text=_('Add an alternative text'),
        max_length=255,
        null=True,
        blank=True,
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product')
    product_unit = models.ForeignKey(
        ProductUnit, on_delete=models.CASCADE, related_name='product_unit_image')
    is_product_unit_default = models.BooleanField(
        verbose_name=_('Product unit default image'),
        help_text=_('Change as default image of product unit'),
        default=False,
    )
    added_by = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    is_active = models.BooleanField(
        verbose_name=_('Product unit visibility'),
        help_text=_('Change product unit visibility'),
        default=True,
    )
    created_at = models.DateTimeField(
        _('Created at'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _('Product Image')
        verbose_name_plural = _('Product Images')


class ProductSpecification(models.Model):
    title = models.CharField(verbose_name=_(
        'Product Specification title'), help_text=_('Required'), max_length=255)
    slug = models.SlugField(verbose_name=_(
        'Product Specification safe URL'), max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_by = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    is_active = models.BooleanField(
        verbose_name=_('Product specification visibility'),
        help_text=_('Change product specification visibility'),
        default=True,
    )
    created_at = models.DateTimeField(
        _('Created at'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('Product Specification')
        verbose_name_plural = _('Product Specifications')

    def __str__(self):
        return self.title


class ProductSpecificationValue(models.Model):
    value = models.CharField(
        verbose_name=_('Product Specification Value'),
        help_text=_('Product specification value (maximum of 255 words'),
        max_length=255,
    )
    slug = models.SlugField(verbose_name=_(
        'Product Specification Value safe URL'), max_length=255, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_unit = models.ForeignKey(ProductUnit, on_delete=models.CASCADE)
    product_specification = models.ForeignKey(
        ProductSpecification, related_name='product_specification', on_delete=models.CASCADE)
    added_by = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    is_active = models.BooleanField(
        verbose_name=_('Product specification value visibility'),
        help_text=_('Change product specification value visibility'),
        default=True,
    )
    created_at = models.DateTimeField(
        _('Created at'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('Product Specification Value')
        verbose_name_plural = _('Product Specification Values')

    def __str__(self):
        return self.value


class ProductReview(models.Model):
    REVIEW_STARS = [
        ('1', 'Very poor'),
        ('2', 'Poor'),
        ('3', 'Average'),
        ('4', 'Good'),
        ('5', 'Very Good'),
    ]

    title = models.CharField(
        verbose_name=_('title'),
        max_length=50,
        null=True,
        blank=True
    )
    content = models.CharField(
        verbose_name=_('content'),
        help_text=_('Required'),
        max_length=255,
        null=True,
        blank=True
    )
    slug = models.SlugField(verbose_name=_(
        'Product Review safe URL'), max_length=255, unique=True)
    stars = models.CharField(
        choices=REVIEW_STARS,
        verbose_name=_('Stars'),
        max_length=255,
        null=True,
        blank=True
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_by = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    is_active = models.BooleanField(
        verbose_name=_('Product review visibility'),
        help_text=_('Change product review visibility'),
        default=True,
    )
    created_at = models.DateTimeField(
        _('Created at'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('Product Review')
        verbose_name_plural = _('Product Reviews')

    # def get_absolute_url(self):
    #     return reverse('inventory:product_review_detail', args=[self.pk])

    def __str__(self):
        return self.title
