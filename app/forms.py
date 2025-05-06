from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation
from .models import Customer
from django.contrib.auth import authenticate

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Confirm Password Again',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    email = forms.CharField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'email': 'Email'}
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'})
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match. Please re-enter.")
        return password2




class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'autofocus': True, 'class': 'form-control'
    }))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={
        'autocomplete': 'current-password', 'class': 'form-control'
    }))

  

# form for change password by old password
class MyPasswordChangeForm(PasswordChangeForm):
     # _ for translate
     old_password = forms.CharField(label=_("Old password"),
          strip=False,
          widget=forms.PasswordInput
          (attrs={'autocomplete':'current-password',
          'autofocus':True,
          'class':'form-control'
          }))
     new_password1 = forms.CharField(label=_("New password"),
          strip=False,
          widget=forms.PasswordInput(attrs={'autocomplete':'current-password',
                                                                      'autofocus':True,
                                                                      'class':'form-control'
                                                                      }),help_text=password_validation.password_validators_help_text_html())
     new_password2 = forms.CharField(label=_('Confirm New Password'),strip=False,
                                     widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'})
                                     )

class MyPasswordResetForm(PasswordResetForm):
     email=forms.EmailField(label=_("Email"),
          max_length=254,
          widget=forms.EmailInput(attrs={'autocomplete':'email','class':'form-control'}))     
     def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("No account found with this email address."))
        return email     
     
     

class MySetPasswordForm(SetPasswordForm):
     new_password1=forms.CharField(label=_("New Password"),strip=False,
                    widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}),
                    help_text=password_validation.password_validators_help_text_html())     
     new_password2= forms.CharField(label=_("Confirm New Password"),strip=False,
                    widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}) )                   

# model form of Profile-> custom forms using own Model
from django import forms
from .models import Customer

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city', 'state', 'zipcode']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name', 'required': True}),
            'locality': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter locality', 'required': True}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter city', 'required': True}),
            'state': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'zipcode': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter ZIP code', 'required': True}),
        }

    def clean_zipcode(self):
        zipcode = self.cleaned_data.get('zipcode')
        if not str(zipcode).isdigit() or len(str(zipcode)) != 6:
            raise forms.ValidationError("Zipcode must be a 6-digit number.")
        return zipcode
