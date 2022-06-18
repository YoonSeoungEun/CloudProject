from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView, ListView

from movie.models import Post

def index(request):
    posts = Post.objects.all().order_by('-pk')
    return render(request, 'movie/post_list.html',
                  {
                      'posts': posts,
                  }
                  )


class PostList(ListView):
    model = Post
    ordering = '-pk'


class PostDetail(DetailView):
    model = Post

