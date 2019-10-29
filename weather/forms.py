from django import forms

class CityForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter City'}), label=False)

