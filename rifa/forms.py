from django import forms
from .models import Raffle


class RaffleForm(forms.ModelForm):
    class Meta:
        model = Raffle
        fields = ('title', 'desc', 'category', 'qtd_num', 'value', 'limit_date',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w3-input w3-border'}),
            'desc': forms.Textarea(attrs={'class': 'w3-input w3-border'}),
            'category': forms.Select(attrs={'class': 'w3-select w3-border'}),
            'qtd_num': forms.NumberInput(attrs={'class': 'w3-input w3-border'}),
            'value': forms.NumberInput(attrs={'class': 'w3-input w3-border'}),
            'limit_date': forms.DateInput(attrs={'class': 'w3-input w3-border'}),
        }

