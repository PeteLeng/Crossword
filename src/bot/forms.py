from django import forms
from .models import WordList

class WordForm(forms.ModelForm):
    words_raw = forms.CharField(
        label='Enter your words below:',
        widget=forms.Textarea(
            attrs={
                'placeholder': 'One word each line.\nMaximum 15 words.',
                'rows': 20,
            }
        )
    )
    class Meta:
        model = WordList
        fields = {
            "words_raw",
        }

    def clean_words_raw(self):
        words_raw = self.cleaned_data.get('words_raw')
        words_clean = words_raw.split('\r\n')
        if len(words_clean) > 15:
            raise forms.ValidationError("Maximum 15 words!")
        check = {}
        for word in words_clean:
            if word not in check:
                check[word] = 1
            else:
                raise forms.ValidationError(f'{word} is repetitive!')
        return words_raw
