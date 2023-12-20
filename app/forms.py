# forms.py
from django import forms
from .models import SalesTransactions

class SalesTransactionsForm(forms.ModelForm):
    class Meta:
        model = SalesTransactions
        fields = '__all__'
