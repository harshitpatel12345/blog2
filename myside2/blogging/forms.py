from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Blog
from django.core.exceptions import ValidationError
import re


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'is_active', 'is_staff')


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2


def validate_alphabetical(value):
    """Validator to ensure the field contains only alphabetic characters."""
    if not re.match("^[a-zA-Z]*$", value):
        raise ValidationError('Title should contain only alphabetic characters.')


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['author', 'title', 'content', 'image', 'category']

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter blog title',
                                            'class': 'form-control'}),
        }

    def clean_title(self):
        """Custom validation for the title field."""
        title = self.cleaned_data.get('title')
        validate_alphabetical(title)
        return title


class BlogUpdateForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'image', 'category']