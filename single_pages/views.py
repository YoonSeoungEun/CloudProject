from django.shortcuts import render

# Create your views here.
from movie.models import Post, Category


def landing(request):
    notice_category = '공지'
    return render(request, 'single_pages/landing.html',{
        'recent_notice_post' : Post.objects.filter(category__name=notice_category).order_by('-pk'),
        'recent_post': Post.objects.order_by('-pk'),
        'categories' : Category.objects.all(),
        'count_posts_without_category': Post.objects.filter(category=None).count(),
    })