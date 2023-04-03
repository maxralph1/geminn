import uuid
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomAccountsManager(BaseUserManager):
    def validateUsername(self, username):
        try:
            username.isalpha()
        except ValidationError:
            raise ValueError(_('You must provide an alphanumeric username'))

    def validateEmail(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("You must provide a valid email address"))

    def validatePassword(self, password):
        if len(password) < 8:
            raise ValidationError(
                "This password is too short. It must contain at least 8 characters.",
            )

    def create_superuser(self, username, email, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must be assigned to is_staff=True'))
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                _('Superuser must be assigned to is_superuser=True'))

        return self.create_user(username, email, password, **other_fields)

    def create_user(self, username, email, password, **other_fields):
        user = self.model(username=username, email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user


class UserModel(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    email = models.CharField((_("Email address")), unique=True, max_length=150)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomAccountsManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'password']

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            'no-reply@gem-inn.com',
            [self.email],
            fail_silently=False
        )

    def __str__(self):
        return self.name


class Address(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    full_name = models.CharField(_('Full Name'), max_length=150)
    phone = models.CharField(_('Phone Number'), max_length=150)
    post_code = models.CharField(_('Post Code'), max_length=20)
    address_line_1 = models.CharField(_('Address Line 1'), max_length=250)
    address_line_2 = models.CharField(_('Address Line 2'), max_length=250)
    town_city = models.CharField(_('Town/City/State'), max_length=150)
    delivery_instructions = models.CharField(
        _('Delivery Instructions'), max_length=250)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    default = models.BooleanField(_('Default'), default=False)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return '{} Address'.format(self.first_name + ' ' + self.last_name)
