from django import forms
from .models import Author, Quote, Tag

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['fullname', 'born_date','born_location', 'description'] 

class QuoteForm(forms.ModelForm):
    
    author = forms.ModelChoiceField(queryset=Author.objects.all(), empty_label=None, to_field_name='id', label='Author')
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple, label='Tags')

    class Meta:
        model = Quote
        fields = ['author', 'quote', 'tags'] 
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].label_from_instance = lambda obj: obj.fullname
        self.fields['tags'].label_from_instance = lambda obj: obj.name
