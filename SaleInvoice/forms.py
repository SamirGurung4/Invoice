from django import forms
from django.forms import BaseInlineFormSet
from .models import Invoice, InvoiceItem


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['Date', 'Payment_method', 'Customer']


class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['Product', 'Quantity']


