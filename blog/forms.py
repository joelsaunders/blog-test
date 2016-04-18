from django import forms
from .models import Post, Laser

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title','text')

class MyForm(forms.ModelForm):

    #dia = forms.DecimalField(max_digits=8, decimal_places=5)
	#power = forms.DecimalField(max_digits=8, decimal_places=5)
    class Meta:
        model = Laser
        fields = ('dia','power')
