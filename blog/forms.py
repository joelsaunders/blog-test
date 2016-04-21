from django import forms
from .models import Post, Laser

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title','text')

class MyForm(forms.ModelForm):

    dia = forms.FloatField(label='dia')
    power = forms.FloatField(label='power')
    lam = forms.FloatField(label='lam')
    class Meta:
        model = Laser
        fields = ('dia','power','lam')
