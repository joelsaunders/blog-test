from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Laser #import the model created previously
from django.utils import timezone #import timezone for sorting
from .forms import PostForm, MyForm
import os
import sqlite3



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

# Function to calculate laser power density and protection level
def spot_size(dia):
    areamm = 3.142*((dia/2)**2)
    aream = areamm / (1000**2)
    return aream

def p_density(power, dia):
    power_density = power / spot_size(dia)
    return power_density


def p_level_lookup(p_dens, lam):
    """Lookup p level in small sqlite database"""
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "db/testDB.db")

    db_norm = os.path.normpath(str(db_path))
    db = sqlite3.connect(db_norm)
    c = db.cursor()

    if lam < 315:
        p_level = c.execute("SELECT * FROM LASER WHERE D1 >?", (p_dens,))
        values = p_level.fetchone()
        return values[1]
    elif lam < 1300:
        p_level = c.execute("SELECT * FROM LASER WHERE D2 >?", (p_dens,))
        values = p_level.fetchone()
        return values[1]
    elif lam < 10000:
        p_level = c.execute("SELECT * FROM LASER WHERE D3 >?", (p_dens,))
        values = p_level.fetchone()
        return values[1]
    else:
        return "0"

    db.close()

def laser(request):
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            dia = float(form.cleaned_data['dia'])
            power = float(form.cleaned_data['power'])
            lam = float(form.cleaned_data['lam'])

            ans = int(p_density(power, dia))
            powerlevel = p_level_lookup(int(ans), lam)

            return render(request, 'blog/laser_out.html',
            {'ans': ans, 'powerlevel': powerlevel})
    else:
        form = MyForm()

    return render(request, 'blog/laser.html', {'form': form})
