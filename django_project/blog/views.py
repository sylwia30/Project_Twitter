from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)

from .forms import CreateCommentForm
from .models import Post, Comment


"""różne sposoby zapisania:
def home(request):
    context = {"post": Post.objects.all()}
    return render(request, 'blog/home.html', context)

def home(request):
    post = Post.objects.all()
    return render(request, 'blog/home.html', {"post": post}) """

""" jak nie jestesmy zalogowani to nie mozemy utorzyć postu wiec
# LoginRequiredMixin przekierowuje nas automatycznie do strony logowania """


class PostListView(LoginRequiredMixin, View):
    def get(self, request):
        posts = Post.objects.all().order_by('-date_posted')
        create_comment = CreateCommentForm()
        return render(request, 'blog/home.html', {'posts': posts,
                                                   'create_comment': create_comment})
    def post(self, request):
        created_comment = CreateCommentForm(request.POST)
        posts = Post.objects.all().order_by('-date_posted')
        if created_comment.is_valid():
            get_comment = created_comment.cleaned_data.get('text')
            post_id = int(request.POST.get("post_id"))
            save_comment = Comment(text=get_comment, user=request.user, post_id=post_id)
            save_comment.save()
            messages.success(request, "Your comment has been added!")
            create_comment = CreateCommentForm()
            return render(request, 'blog/home.html', locals())


""" Lista postów przy użyciu ListView
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'post'
    ordering = ['-date_posted'] # minus oznacza sortowanie od najnowszego postu
    paginate_by = 2 # pokazują się dwa posty na stronie
"""


class CommentListView(ListView):
    model = Comment
    template_name = 'blog/home.html'
    context_object_name = 'comment'
    ordering = ['-date_comment']
    paginate_by = 5


class UserPostView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'post'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(View):

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        create_comment = CreateCommentForm()
        return render(request, 'blog/post_detail.html', {'post': post,
                                                   'create_comment': create_comment})
    def post(self, request, pk):
        created_comment = CreateCommentForm(request.POST)
        post = Post.objects.get(pk=pk)
        if created_comment.is_valid():
            get_comment = created_comment.cleaned_data.get('text')
            save_comment = Comment(text=get_comment, user=request.user, post=post)
            save_comment.save()
            messages.success(request, "Your comment has been added!")
            create_comment = CreateCommentForm()
            return render(request, 'blog/post_detail.html', locals())


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user # czy autor równa sie zalogowanemu użytkownikowi
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user # czy autor równa sie zalogowanemu użytkownikowi
        return super().form_valid(form)

    """ poniższa funkcja wyklucza edytowanie postów przez innych użytkowników, zwraca 403 Forbidden """

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class About(View):
    def get(self, request):
        context = {
            "context": "Add your own journey here",
            'title': 'About'
        }
        return render(request, 'blog/about.html', context)