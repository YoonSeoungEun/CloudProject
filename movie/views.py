from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView, ListView

from movie.models import Post, Category, Tag


def show_category_posts(request, slug):
    if slug=='no-category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)
    context = {
        'categories' : Category.objects.all(),
        'count_posts_without_category' : Post.objects.filter(category=None).count(),
        'category' : category,
        'post_list' : post_list
    }
    return render(request, 'movie/post_list.html', context)


def show_tag_posts(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()

    context = {
        'categories' : Category.objects.all(),
        'count_posts_without_category' : Post.objects.filter(category=None).count(),
        'tag' : tag,
        'post_list' : post_list
    }
    return render(request, 'movie/post_list.html', context)


class PostList(ListView):
    model = Post
    ordering = '-pk'


class PostDetail(DetailView):
    model = Post

