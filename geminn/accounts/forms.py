from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from .models import UserModel, Address


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['full_name', 'phone', 'address_line_1',
                  'address_line_2', 'post_code', 'town_city', 'delivery_instructions']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Full Name'}
        )
        self.fields['phone'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Phone'}
        )
        self.fields['address_line_1'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Address Line 1'}
        )
        self.fields['address_line_2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Address Line 2'}
        )
        self.fields['post_code'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Postal Code'}
        )
        self.fields['town_city'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Town/City/State'}
        )
        self.fields['delivery_instructions'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Delivery Instructions'}
        )


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Username', 'id': 'username', 'name': 'username', 'required': 'required', 'type': 'text'}
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control',
               'placeholder': 'Password', 'id': 'password', 'name': 'password', 'required': 'required', 'type': 'password'}
    ))


class UserRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(
        label='First Name',
        min_length=1,
        max_length=100,
        help_text='First name is required')
    last_name = forms.CharField(
        label='Last Name',
        min_length=1,
        max_length=100,
        help_text='Last name is required')
    username = forms.CharField(
        label='Username',
        min_length=4,
        max_length=50,
        help_text='Username is required')
    email = forms.EmailField(
        max_length=100,
        help_text='Email required',
        error_messages={'required': 'Please enter a valid email address for shipping updates.'})
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat password',
        widget=forms.PasswordInput)

    class Meta:
        model = UserModel
        fields = ('first_name', 'last_name', 'username', 'email', 'password', )

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        return last_name

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        response = UserModel.objects.filter(username=username)
        if response.count():
            raise forms.ValidationError('Username already exists')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if UserModel.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another email. This email is already taken.'
            )
        return email

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update(
            {'type': 'text', 'name': 'first_name', 'id': 'first_name',
                'class': 'form-control', 'placeholder': 'eg. John', 'required': 'required'}
        )
        self.fields['last_name'].widget.attrs.update(
            {'type': 'text', 'name': 'last_name', 'id': 'last_name',
                'class': 'form-control', 'placeholder': 'eg. Doe', 'required': 'required'}
        )
        self.fields['username'].widget.attrs.update(
            {'type': 'text', 'name': 'username', 'id': 'username',
                'class': 'form-control', 'placeholder': 'Username', 'required': 'required'}
        )
        self.fields['email'].widget.attrs.update(
            {'type': 'email', 'name': 'email', 'id': 'email', 'class': 'form-control',
                'placeholder': 'you@example.com', 'required': 'required'}
        )
        self.fields['password'].widget.attrs.update(
            {'type': 'password', 'name': 'password', 'id': 'password',
                'class': 'form-control', 'placeholder': '********', 'required': 'required'}
        )
        self.fields['password2'].widget.attrs.update(
            {'type': 'password', 'id': 'password2',
                'class': 'form-control', 'placeholder': '********', 'required': 'required'}
        )


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=255, widget=forms.TextInput(
        attrs={'type': 'email', 'name': 'email', 'id': 'email', 'class': 'form-control',
               'placeholder': 'you@example.com', 'required': 'required'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        foundUser = UserModel.objects.filter(email=email)
        if not foundUser:
            raise forms.ValidationError(
                'Unfortunately we can not find an account associated with that email address')
        return email


class PasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'type': 'password', 'id': 'new-password1',
                   'class': 'form-control', 'placeholder': 'New password', 'required': 'required'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'type': 'password', 'id': 'new-password2',
                   'class': 'form-control', 'placeholder': 'Repeat new password', 'required': 'required'}))


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
        fields = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.fields['username'].required = True
        self.fields['email'].required = True
