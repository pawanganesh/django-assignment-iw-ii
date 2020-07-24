from django.urls import path

from .views import IndexView, DetailView, BlogPostView, edit_blog_view, DeleteView


app_name = 'blog'
urlpatterns = [
    path('index/', IndexView.as_view(), name='index'),
    path('detail/<slug:slug>/', DetailView.as_view(), name='detail'),
    path('create/', BlogPostView.as_view(), name="create"),
    path('edit/<slug>', edit_blog_view, name="edit"),
    path('delete/<int:pk>', DeleteView.as_view(), name="delete"),
]
