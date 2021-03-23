from django import forms

class NewsLetterForm(forms.ModelForm):
    name = forms.CharField(label='First Name', max_length=30)
    email = forms.EmailField(label='Email')