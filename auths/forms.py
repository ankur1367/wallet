from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Button
from crispy_forms.bootstrap import Field, FormActions, InlineField
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    username = forms.CharField(label='username', required=False, )
    password = forms.CharField(label='password', required=False, widget=forms.PasswordInput)

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_class = 'form-group'
    helper.form_show_labels = False
    helper.form_action = '/authentication/'
    helper.layout = Layout(
        Field('username', placeholder='Username', css_class='form-control'),
        Field('password', placeholder='Password', css_class='form-control'),
        InlineField(Button('auth-back', 'Back', css_class='btn-danger')),
        InlineField(Submit('login', 'Sign in', css_class='btn-primary')),
    )

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()

        username = cleaned_data['username']
        password = cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError("Incorrect username or password")
        return cleaned_data


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', required=True)
    email = forms.EmailField()
    password = forms.CharField(label='Password', required=True, widget=forms.PasswordInput)

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_show_labels = False
    helper.form_action = '/registration/'
    helper.layout = Layout(
        Field('username', placeholder='Username', css_class='form-control'),
        Field('email', placeholder='Email (example@gmail.com)', css_class='form-control'),
        Field('password', placeholder='Password', css_class='form-control'),
        InlineField(Button('reg-back', 'Back', css_class='btn-danger')),
        InlineField(Submit('sign up', 'Sign up', css_class='btn-primary')),
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("username already exists")
        return username
