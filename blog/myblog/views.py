from django.shortcuts import render, get_object_or_404
from django.views import View
from django.core.paginator import Paginator
from django.contrib.auth import login
from django.http import HttpResponseRedirect

from .models import Post
from .forms import SignUpForm
# Create your views here.


class MainView(View):
    template_name = 'myblog/home.html'
    post = Post
    paginator = Paginator

    def get(self, request):
        posts = self.post.objects.all()
        paginator = self.paginator(posts, 6)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {'page_obj': page_obj}
        return render(request, self.template_name, context)


class PostDetailView(View):
    template = 'myblog/post_detail.html'

    def get(self, request, slug):
        post = get_object_or_404(Post, url=slug)
        context = {'post': post}
        return render(request, self.template, context)


class SignUpView(View):

