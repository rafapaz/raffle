from django import forms
from .models import Raffle


class RaffleForm(forms.ModelForm):
    class Meta:
        model = Raffle
        fields = ('title', 'desc', 'category', 'qtd_num', 'value', 'limit_date',)
