from django import forms
from django.contrib.auth.models import User
from .models import VerificationAttempt

# Simple Form for User Registration with minimal password validation
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    password_confirm = forms.CharField(widget=forms.PasswordInput, required=True, label="Confirm Password")
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Passwords do not match.")
        return cleaned_data

# Form to upload signature for verification
class SignatureVerificationForm(forms.ModelForm):
    class Meta:
        model = VerificationAttempt
        fields = ['uploaded_signature']
