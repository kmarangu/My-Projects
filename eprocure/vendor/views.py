from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.urls import reverse_lazy
from django.http import Http404
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)
from django.utils import timezone

from braces.views import SelectRelatedMixin

from . import forms
from . import models

from django.contrib.auth import get_user_model
User = get_user_model()

class PostList(SelectRelatedMixin, ListView):
    model = models.Post
    select_related = ("user", "group")

    # Save published date
    def get_queryset(self):
        return post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class UserPosts(ListView):
    model = models.Post
    template_name = "vendor/user_post_list.html"

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related("posts").get(
                username__iexact=self.kwargs.get("username")
            )
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_user"] = self.post_user
        return context


class PostDetail(SelectRelatedMixin, DetailView):
    model = models.Post
    select_related = ("user", "group")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username")
        )


class CreatePost(LoginRequiredMixin, SelectRelatedMixin, CreateView):
    # form_class = forms.PostForm
    fields = ('message','group')
    model = models.Post

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update({"user": self.request.user})
    #     return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'vendor/post_detail.html'
    # form_class = PostForm
    model = models.Post

class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'vendor/post_draft_list.html'
    model = models.Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('create_date')

class DeletePost(LoginRequiredMixin, SelectRelatedMixin, DeleteView):
    model = models.Post
    select_related = ("user", "group")
    success_url = reverse_lazy("vendor:all")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Post Deleted")
        return super().delete(*args, **kwargs)

#######################################
## Functions that require a pk match ##
#######################################

@login_required
def post_publish(request, pk):
    Post = get_object_or_404(post, pk=pk)
    Post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def add_comments_to_post(request, pk):
    Post = get_object_or_404(post, pk=pk)
    if request.method == "POST":
        form = commentsForm(request.POST)
        if form.is_valid():
            comments = form.save(commit=False)
            comments.post = Post
            comments.save()
            return redirect('post_detail', pk=Post.pk)
    else:
        form = commentsForm()
    return render(request, 'blog/comment_form.html', {'form': form})


@login_required
def comment_approve(request, pk):
    Comments = get_object_or_404(comments, pk=pk)
    Comments.approve()
    return redirect('post_detail', pk=Comments.post.pk)


@login_required
def comment_remove(request, pk):
    Comments = get_object_or_404(comments, pk=pk)
    post_pk = Comments.post.pk
    Comments.delete()
    return redirect('post_detail', pk=post_pk)
