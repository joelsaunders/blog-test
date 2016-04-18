from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Laser #import the model created previously
from django.utils import timezone #import timezone for sorting
from .forms import PostForm, MyForm

def post_list(request):
    # order posts and exclude unpublished posts
    posts = Post.objects.filter(published_date__lte=
        timezone.now()).order_by('-published_date')
    #render html page
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    #add view for post details pages
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render((request), 'blog/post_edit.html', {'form': form})

def spot_size(dia):
    areamm = 3.142*((dia/2)**2)
    aream = areamm / (1000**2)
    return aream

def p_density(power, dia):
    power_density = power / spot_size(dia)
    return power_density

def laser(request):
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            dia = float(form.cleaned_data['dia'])
            power = float(form.cleaned_data['power'])

            ans = p_density(power, dia)

            return render(request, 'blog/laser_out.html', {'ans': ans})
    else:
        form = MyForm()

    return render(request, 'blog/laser.html', {'form': form})
