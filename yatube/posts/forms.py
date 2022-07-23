from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        fields = ('text', 'group')
        help_texts = {
            'group': 'Группа, к которой будет относиться пост',
            'text': 'Текст нового поста',
        }
        labels = {
            'group': 'Группа',
            'text': 'Текст',
        }
        model = Post 


    def clean_text(self):
        data = self.cleaned_data['text']
        if Post.text == '':
            raise forms.ValidationError(
                'Это поле обязательно должно быть заполнено')
        return data
