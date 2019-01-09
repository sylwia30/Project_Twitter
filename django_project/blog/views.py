from __future__ import unicode_literals

from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from .forms import CreateCommentForm
from .models import Post, Comment


# def home(request):
#     context = {
#         "post": Post.objects.all()
#     }
#     return render(request, 'blog/home.html', context)
# inny sposób zapisania:

def home(request):
    post = Post.objects.all()
    return render(request, 'blog/home.html', {"post": post})


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'post'
    ordering = ['-date_posted'] # minus oznacza sortowanie od najnowszego postu
    paginate_by = 5 # pokazują się dwa posty na stronie


class CommentListView(ListView):
    model = Comment
    template_name = 'blog/home.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'comment'
    ordering = ['-date_comment'] # minus oznacza sortowanie od najnowszego postu
    paginate_by = 5 # pokazują się dwa posty na stronie



class UserPostView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'post'
    paginate_by = 5 # pokazują się dwa posty na stronie

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
# jak nie jestesmy zalogowani to nie mozemy utorzyć postu wiec
# LoginRequiredMixin przekierowuje nas automatycznie do strony logowania
    def form_valid(self, form):
        form.instance.author = self.request.user # czy autor równa sie zalogowanemu użytkownikowi
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user # czy autor równa sie zalogowanemu użytkownikowi
        return super().form_valid(form)

# ta funkcja wyklucza edytowanie postów innych użytkowników, zwraca 403 Forbidden
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




# class CommentCreateView(LoginRequiredMixin, CreateView):
#     model = Comment
#     fields = ['text']
#     success_url = '/'
#
#     def form_valid(self, form):
#         form.instance.user = self.request.user # czy autor równa sie zalogowanemu użytkownikowi
#         return super().form_valid(form)


# class CommentCreateView(LoginRequiredMixin, View):
#
#     def get(self, request):
#         comment = CommentCreateForm()
#         return render(request, 'blog/comment_form.html', {'comment': comment})
#
#     def post(self, request):
#         comment = CommentCreateForm(request.POST)
#         if comment.is_valid():
#             add_comment = comment.cleaned_data.get('text')
#             create_comment = Comment.objects.create(text=add_comment)
#             messages.success(request, f'Your comment has been created!')
#             return render(request, 'blog/comment_form.html', locals())
#             # comment.instance.user = self.request.user


class CommentCreateView(LoginRequiredMixin, View):
        pass
#     def get(self, request):
#         comment = CommentCreateForm
#         return render(request, 'blog/comment_form.html', locals())
#
#     def post(self, request):
#         comment = CommentCreateForm(request.POST)
#         if comment.is_valid():
#             new_comment = comment.save()
#             comment_get = comment.cleaned_data['text']
#             Comment.objects.create(text=comment_get)
#             # if comment_get:
#             #     for comment in comment_get:
#             #         comment.post.add(new_comment)
#             return render(request, 'blog/comment_form.html', locals())

# class AddProductViewxx(View):
#
#     def get(self, request):
#         form = AddProductFormxxx
#         return render(request, 'homework/new_product.html', locals())
#
#     def post(self, request):
#         form = AddProductFormxxx(request.POST)
#         if form.is_valid():
#             new_prod = form.save()
#             category_get = form.cleaned_data['categories']
#             if category_get:
#                 for category in category_get:
#                     category.products.add(new_prod)
#             return render(request, 'homework/new_product.html', locals())

class About(LoginRequiredMixin, View):
    def get(self, request):
        posts = Post.objects.all().order_by('-date_posted')
        create_comment = CreateCommentForm()
        return render(request, 'blog/about.html', {'posts': posts,
                                                   'create_comment': create_comment})
    # def post(self, request):
    #     created_comment = CreateCommentForm(request.POST, instance=?????????)
    #     if created_comment.is_valid():
    #         get_comment = created_comment.cleaned_data.get('text')
    #         save_comment = Comment(text=get_comment, user=request.user, post==?????????)
    #         save_comment.save()
    #         messages.success(request, "Your comment has been added!")
    #         return render(request, 'blog/about.html', locals())








    # def get(self, request):
    #     posts = Post.objects.all().order_by('-date_posted')
    #     for post in posts:
    #         one_post = Post.objects.get(pk=post.id).comment_set.all()
    #         # comments = one_post.comment_set.all()
    #     return render(request, 'blog/about.html', {'posts': posts,
    #                                                'one_post': one_post})


# stara funkcja do linku about
# def about(request):
#     return render(request, 'blog/about.html', {'title': 'About'})