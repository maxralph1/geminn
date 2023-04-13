from datetime import datetime

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect,  render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from inventory.models import Product
from orders.models import Order
from orders.views import user_orders

from .forms import UserRegistrationForm, CustomPasswordResetForm, UserAddressForm, UserEditForm
from .models import Address, UserModel
from .tokens import account_activation_token, password_reset_token


# User

@login_required
def favorites(request):
    products = Product.objects.filter(users_favorite=request.user)
    return render(request, 'accounts/users/user_favorites.html', {'favorites': products})


@login_required
def add_to_favorites(request, id):
    product = get_object_or_404(Product, id=id)
    if product.users_favorite.filter(id=request.user.id).exists():
        product.users_favorite.remove(request.user)
        messages.success(request, product.title +
                         ' has been removed from your favorites')
    else:
        product.users_favorite.add(request.user)
        messages.success(request, 'Added ' +
                         product.title + ' to your favorites')
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def dashboard(request):
    orders = user_orders(request)
    return render(request, 'accounts/dashboard/index.html', {
        'orders': orders
    })


@login_required
def edit_details(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request, 'accounts/users/edit.html', {'user_form': user_form})


@login_required
def delete_user(request):
    user = UserModel.objects.get(user_name=request.user)
    user.is_active = False
    user.deleted_at = datetime.now()
    user.save()
    logout(request)
    return redirect('accounts:delete_confirmation')


def account_register(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        registerForm = UserRegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.first_name = registerForm.cleaned_data['first_name']
            user.last_name = registerForm.cleaned_data['last_name']
            user.username = registerForm.cleaned_data['username']
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = _('Activate your Account')
            message = render_to_string(
                'accounts/registration/account_activation_email.html',
                {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                },
            )
            user.email_user(subject=subject, message=message)
            return render(request, 'accounts/registration/register_email_confirm.html', {'form': registerForm})
        else:
            return render(request, 'accounts/registration/register.html', {'form': registerForm})
    else:
        registerForm = UserRegistrationForm()
    return render(request, 'accounts/registration/register.html', {'form': registerForm})


def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserModel.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('accounts:dashboard')
    else:
        return render(request, 'accounts/registration/activation_invalid.html')


def password_reset(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        passwordResetForm = CustomPasswordResetForm(request.POST)
        if passwordResetForm.is_valid():
            resetEmail = passwordResetForm.cleaned_data['email']
            user = UserModel.objects.get(email=resetEmail)
            current_site = get_current_site(request)
            subject = _('Activate your Account')
            message = render_to_string(
                'accounts/password_reset/password_reset_email.html',
                {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': password_reset_token.make_token(user),
                },
            )
            user.email_user(subject=subject, message=message)
            return render(request, 'accounts/password_reset/reset_status.html', {'form': passwordResetForm})
        else:
            return render(request, 'accounts/password_reset/password_reset_form.html', {'form': passwordResetForm})
    else:
        passwordResetForm = CustomPasswordResetForm()
    return render(request, 'accounts/password_reset/password_reset_form.html', {'form': passwordResetForm})


def password_reset_token_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserModel.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and password_reset_token.check_token(user, token):
        # user.is_active = True
        # user.save()
        # login(request, user)
        # return redirect('accounts:dashboard')
        return render(request, 'accounts/password_reset/password_reset_form.html', {'user': uid})
    else:
        return render(request, 'accounts/registration/activation_invalid.html')


def password_edit(request, user):
    if request.method == 'POST':
        user = UserModel.objects.get(pk=id, user=request.user)
        user_form = UserRegistrationForm(instance=user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('accounts:users'))
    else:
        user = UserModel.objects.get(pk=id, user=request.user)
        user_form = UserRegistrationForm(instance=user)
    return render(request, 'accounts/dashboard/edit_users.html', {'form': user_form})


# Address

@login_required
def view_address(request):
    addresses = Address.objects.filter(
        user=request.user).order_by('-default')
    address_form = UserAddressForm()
    return render(request, 'accounts/addresses/index.html', {
        'addresses': addresses,
        'form': address_form
    })


@login_required
def add_address(request):
    if request.method == 'POST':
        address_form = UserAddressForm(data=request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.user = request.user
            address_form.save()
            return HttpResponseRedirect(reverse('accounts:addresses'))
        else:
            return HttpResponse('Error handler content', status=400)
    else:
        address_form = UserAddressForm()
    return render(request, 'accounts/addresses/index.html', {
        'form': address_form
    })


@login_required
def edit_address(request, id):
    if request.method == 'POST':
        address = Address.objects.get(pk=id, user=request.user)
        address_form = UserAddressForm(instance=address, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            return HttpResponseRedirect(reverse('accounts:addresses'))
    else:
        address = Address.objects.get(pk=id, user=request.user)
        address_form = UserAddressForm(instance=address)
    return render(request, 'accounts/addresses/edit.html', {
        'form': address_form
    })


@login_required
def set_default(request, id):
    Address.objects.filter(user=request.user,
                           default=True).update(default=False)
    Address.objects.filter(pk=id, user=request.user).update(default=True)

    previous_url = request.META.get('HTTP_REFERER')

    if 'delivery_address' in previous_url:
        return redirect('checkout:delivery_address')

    return redirect('accounts:addresses')


@login_required
def delete_address(request, id):
    Address.objects.filter(pk=id, user=request.user).delete()
    messages.success(request, 'Address removed')
    return redirect('accounts:addresses')


# User Orders

@login_required
def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return render(request, 'accounts/users/user_orders.html', {'orders': orders})
