from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect, redirect, Http404
from .models import Post
from .forms import PostForm, CommentForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q

def post_index(request):
    post_list = Post.objects.filter(published=True)

    query = request.GET.get('q')
    
    if query:
        post_list = post_list.filter(
            Q(title__icontains=query) |
            Q(body__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()

    paginator = Paginator(post_list, 10) # Show 25 contacts per page

    page = request.GET.get('page')
    
    posts = paginator.get_page(page)
    
    return render(request, 'post/index.html', {'posts': posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return HttpResponseRedirect(post.get_absolute_url())

    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'post/detail.html', context)

def post_create(request):

    if not request.user.is_authenticated:
        return Http404

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        form = PostForm(initial={'published': False})

    context = {
        'form': form,
    }
    return render(request, 'post/form.html', context)

def post_edit(request, id):

    if not request.user.is_authenticated:
        return Http404

    post = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        messages.success(request, 'Kayıt Edildi.', extra_tags='alert-success')
        return HttpResponseRedirect(post.get_absolute_url())
    context = {
        'form': form
    }
    return render(request, 'post/form.html', context)

def post_delete(request, id):

    if not request.user.is_authenticated:
        return Http404
    
    post = get_object_or_404(Post, id=id)
    post.delete()
    messages.success(request, 'İlgili Post silindi.', extra_tags='alert-success')
    return redirect('post:index')