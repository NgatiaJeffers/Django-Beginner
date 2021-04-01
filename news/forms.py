from django import forms
from .models import Article

class NewsLetterForm(forms.Form):
    name = forms.CharField(label='First Name', max_length=30)
    email = forms.EmailField(label='Email')

# ModelForms allows us to easily create form fields from the different attributes in a model.
class NewArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ['editor', 'published']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }
        