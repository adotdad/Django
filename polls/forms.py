from polls.models import Job
from django import forms


class JobModelForm(forms.ModelForm):
    title = forms.CharField(
        label='عنوان',
        max_length=250,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    approx_time = forms.IntegerField(
        label='تخمین زمانی',
        required=True,
        widget=forms.NumberInput(attrs={'class': 'small form-control', 'type': 'number'})
    )

    value = forms.IntegerField(
        label='ارزش',
        required=True,
        widget=forms.NumberInput(attrs={'class': 'range', 'type': 'range', 'min': '0', 'max': '100000', 'step': '1', 'list': 'tickmarks'})
    )

    description = forms.CharField(
        label='توضیحات',
        max_length=250,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control big'})
    )

    class Meta:
        model = Job
        fields = ['title', 'approx_time', 'value', 'description']
