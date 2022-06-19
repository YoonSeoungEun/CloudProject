from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views.generic import DetailView, ListView, CreateView, UpdateView, FormView

from movie.forms import CommentForm, PostSearchForm
from movie.models import Post, Category, Tag


class SearchFormView(FormView):
    form_class = PostSearchForm
    template_name = 'movie/post_search.html'

    def form_valid(self, form):
        searchWord = form.cleaned_data['search_word']
        post_list = Post.objects.filter(Q(title__contains=searchWord) | Q(content__icontains=searchWord)).distinct()

        context = {}
        context['form'] = form
        context['search_term'] = searchWord
        context['object_list'] = post_list

        return render(self.request, self.template_name, context)


def my_post(request):
    post = Post.objects.all()
    mypost = post.filter(author_id=request.user.id).order_by('-pk')
    context = {
        'my_post_list' : mypost
    }
    return render(request, 'movie/myposts.html', context)


def delete_post(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, '성공적으로 삭제하였습니다.')
        return redirect('http://127.0.0.1:8000/movie/')
    return render(request, 'movie/post_delete.html', {'Post': post})


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'hook_msg', 'head_image', 'attached_file', 'category', 'tags']

    template_name = 'movie/post_form_update.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'head_image', 'hook_msg', 'attached_file', 'category', 'tags']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff or self.request.user.is_authenticated

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated or (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('movie/')


def show_category_posts(request, slug):
    if slug == 'no-category':
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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['count_posts_without_category'] = Post.objects.filter(category=None).count()
        return context


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['count_posts_without_category'] = Post.objects.filter(category=None).count()
        context['comment_form'] = CommentForm
        return context


def addComment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect(comment.get_absolute_url())
        else:
            return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied