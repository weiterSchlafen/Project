from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .forms import PostForm
from .models import Post

def post_add(request):
    form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_list(request):
    posts = Post.objects.for_user(user=request.user)
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    if not post.is_publish() and not request.user.is_staff:
        raise Http404("Запись в блоге не найдена")
    return render(request, 'blog/post_detail.html', {'post': post})

def post_add(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PostForm(request.Post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('post_detail', id=post.id)
            else:
                form = PostForm()
            return render(request, 'blog/post_edit.html', {'form': form})
    return redirect('post_list')

def post_update(request, id):
    post = get_object_or_404(Post, id=id) if id else None

    if post and post.author != request.user:
        return redirect('post_list')

    if request.method == "POST":
        form = PostForm(request.Post, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', id=post.id)
        else:
            form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, id=None):
    post = get_object_or_404(Post, id=id) if id else None

    if post and post.author != request.user:
        return redirect('post_list')

    if request.method == "POST":
        form = PostForm(request.Post, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if post.is_published:
                post.published_date = timezone.now()
            else:
                post.published_date = None
            post.save()
            return redirect('post_detail', id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_publish(request, id):
    post = get_object_or_404(Post, id=id)
    post.publish()
    return redirect('post_detail', id=id)

def add_comment(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', id=post.id)
        else:
            form = PostForm()
        return render(request, 'blog/add_comment.html', {'form': form})

    # post = get_object_or_404(Post, id=id)
    # if request.method == "POST":
    #     form = PostForm(request.POST, instance=post)
    #     if form.is_valid():
    #         post = form.save(commit=False)
    #         post.author = request.user
    #         post.published_date = timezone.now()
    #         post.save()
    #         return redirect('post_detail', id=post.id)
    #     else:
    #         form = PostForm(instance=post)
    #     return render(request, 'blog/post_edit.html', {'form': form})

# def handler404(request, exception, template_name="404.html"):
#     response = render_to_response("404.html")
#     response.status_code = 404
#     return response
