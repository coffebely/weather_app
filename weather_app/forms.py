from django import forms


class CityForm(forms.Form):
    city = forms.CharField(widget=forms.TextInput(attrs={"class": "myinput", "placeholder": "City"}))

