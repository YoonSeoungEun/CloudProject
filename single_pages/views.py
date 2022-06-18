from django.shortcuts import render

# Create your views here.
from movie.models import Post, Category


def landing(request):
    return render(request, 'single_pages/landing.html',{
        'recent_post' : Post.objects.order_by('-pk'),
        'categories' : Category.objects.all(),
        'count_posts_without_category': Post.objects.filter(category=None).count(),
    })