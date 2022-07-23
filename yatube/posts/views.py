from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from .models import Post, Group, User
from .forms import PostForm


def index(request):
    post_list = Post.objects.select_related('group', 'author').all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts_in_group = group.posts.all()
    paginator = Paginator(posts_in_group, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'group': group,
        'page_obj': page_obj,
    }
    template = 'posts/group_list.html'
    return render(request, template, context)


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    author_posts = Post.objects.filter(author=user)
    posts_count = author_posts.count()
    paginator = Paginator(author_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'posts_count': posts_count,
        'user': user,
    }
    return render(request, 'posts/profile.html', context)


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    posts_count = Post.objects.filter(author=post.author).count()

    context = {
        'post': post,
        'posts_count': posts_count,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    
    form = PostForm(request.POST or None)

    if request.method == "POST":
        if not form.is_valid():
            return render(request, 'posts/create_post.html', {'form': form})

        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', post.author)
    
    return render(request, "posts/create_post.html", {"form": form})