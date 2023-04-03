from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from .models import UserModel, Address


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['full_name', 'phone', 'address_line_1',
                  'address_line_2', 'town_city', 'post_code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs.update(
            {'class': '', 'placeholder': 'Full Name'}
        )
        self.fields['phone'].widget.attrs.update(
            {'class': '', 'placeholder': 'Phone'}
        )
        self.fields['address_line_1'].widget.attrs.update(
            {'class': '', 'placeholder': 'Address Line 1'}
        )
        self.fields['address_line_2'].widget.attrs.update(
            {'class': '', 'placeholder': 'Address Line 2'}
        )
        self.fields['town_city'].widget.attrs.update(
            {'class': '', 'placeholder': 'Town/City/State'}
        )


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': '', 'placeholder': 'Username', 'id': 'username'}
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': '', 'placeholder': 'Password', 'id': 'password'}
    ))


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        label='Enter Username', min_length=4, max_length=50, help_text='Username is required')
    email = forms.EmailField(max_length=100, help_text='Email required', error_messages={
                             'required': 'Sorry, you will need an email address'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = UserModel
        fields = {'username', 'email'}

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        response = UserModel.objects.filter(username=username)
        if response.count():
            raise forms.ValidationError('Usernmame already exists')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if UserModel.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another email. This email is already taken.'
            )
        return email

    def clean_password(self):
        safe_password = self.cleaned_data
        if safe_password['password'] != safe_password['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return safe_password['password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': '', 'placeholder': 'Username',
                'name': 'username', 'id': 'username'}
        )
        self.fields['email'].widget.attrs.update(
            {'class': '', 'placeholder': 'E-mail', 'name': 'email', 'id': 'email'}
        )
        self.fields['password'].widget.attrs.update(
            {'class': '', 'placeholder': 'Password',
                'name': 'password', 'id': 'password'}
        )
        self.fields['password2'].widget.attrs.update(
            {'class': '', 'placeholder': 'Repeat password'}
        )


class CustomPasswordResetForm(PasswordResetForm):
    new_password = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': '', 'placeholder': 'New Password',
                   'id': 'new-password'}
        )
    )
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': '', 'placeholder': 'Repeat new password',
                   'id': 'new-password2'}
        )
    )


class UserEditForm(forms.ModelForm):
    username = forms.CharField(
        label='Account username (cannot be changed)', max_length=100, widget=forms.TextInput(
            attrs={'class': '', 'placeholder': 'username',
                   'id': 'username', 'readonly': 'readonly'}
        )
    )
    email = forms.EmailField(label='email', min_length=2, max_length=100, widget=forms.TextInput(
        attrs={'class': '', 'placeholder': 'email', 'id': 'email'}
    ))
    first_name = forms.CharField(label='First name', min_length=2, max_length=100, widget=forms.TextInput(
        attrs={'class': '', 'placeholder': 'first_name', 'id': 'first_name'}
    ))
    last_name = forms.CharField(label='Last name', min_length=2, max_length=100, widget=forms.TextInput(
        attrs={'class': '', 'placeholder': 'last_name', 'id': 'last_name'}
    ))

    class Meta:
        model = UserModel
        fields = ('username', 'email', 'firts_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.fields['username'].required = True
        self.fields['email'].required = True
