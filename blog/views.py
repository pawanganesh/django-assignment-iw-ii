from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView

from account.models import User
from blog.models import BlogPost

from .forms import CreateBlogPostForm, UpdateBlogPostForm


class IndexView(ListView):
    template_name = 'blog/index.html'
    model = BlogPost
    context_object_name = 'posts'


class DetailView(DetailView):
    template_name = 'blog/detail.html'
    model = BlogPost
    context_object_name = 'post'


class BlogPostView(View):

    def get(self, request):
        return render(request, 'blog/create_blog.html')

    def post(self, request):
        form = CreateBlogPostForm(request.POST or None, request.FILES or None)
        user = request.user
        if form.is_valid():
            obj = form.save(commit=False)
            author = User.objects.filter(email=user.email).first()
            obj.author = author
            obj.save()
            return redirect('blog:index')
        form = CreateBlogPostForm()
        context = {
            'form': form
        }
        return render(request, 'blog/create_blog.html', context)


def edit_blog_view(request, slug):
    context = {}
    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')

    blog_post = get_object_or_404(BlogPost, slug=slug)

    if blog_post.author != user:
        return HttpResponse("You are not the author of that post.")

    if request.POST:
        form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance=blog_post)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success_message'] = "Updated"
            blog_post = obj

    form = UpdateBlogPostForm(
        initial={
            "title": blog_post.title,
            "body": blog_post.body,
            "image": blog_post.image,
        }
    )

    context['form'] = form
    return render(request, 'blog/edit_blog.html', context)


class DeleteView(DeleteView):
    model = BlogPost
    success_url = '/blog/index/'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
