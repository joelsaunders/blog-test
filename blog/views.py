from django.shortcuts import render, get_object_or_404
from .models import Post #import the model created previously
from django.utils import timezone #import timezone for sorting


def post_list(request):
    # order posts and exclude unpublished posts
    posts = Post.objects.filter(published_date__lte=
        timezone.now()).order_by('published_date')
    #render html page
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    #add view for post details pages
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})
