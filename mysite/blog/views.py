from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from blog.models import post, comments
from django.utils import timezone
from blog.forms import postForm, commentsForm

from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = post

    def get_queryset(self):
        return post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = post

class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'

    form_class = postForm

    model = post


class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'

    form_class = postForm

    model = post


class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_draft_list.html'
    model = post

    def get_queryset(self):
        return post.objects.filter(published_date__isnull=True).order_by('create_date')


class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = post
    success_url = reverse_lazy('post_list')

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
