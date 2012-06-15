from django import forms

class ThingForm(forms.Form):
    thing1 = forms.CharField(widget=forms.HiddenInput)
    thing2 = forms.CharField(widget=forms.HiddenInput)