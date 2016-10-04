from django import forms
from .models import Wallet
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Button
from crispy_forms.bootstrap import Field, FormActions


class AddOperationForm(forms.Form):
    title = forms.CharField(label='Title', required=True)
    sum = forms.FloatField(label='Sum', required=True)
    wallets = forms.ChoiceField(label='Wallets', required=True)
    code = forms.ChoiceField(label='Codes', required=True)
    date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    helper = FormHelper()
    helper.form_id = 'id-add-operation-form'
    helper.form_method = 'POST'
    helper.form_class = 'form-horizontal, form-group'
    helper.form_show_labels = False
    # helper.form_action = '/add-operation/'

    helper.layout = Layout(
        Field('title', placeholder='Title', css_class='form-control'),
        Field('sum', placeholder='Sum', css_class='form-control'),
        Field('wallets', css_class='form-control'),
        Field('code', css_class='form-control'),
        Field('date', css_class='form-control'),
        FormActions(Button('Add', 'add', css_class='btn, btn-primary'))
    )