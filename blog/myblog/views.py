from venv import create
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

    def get(self, request):
        # выборка постов неупорядочена и поэтому выводится предупреждение
        posts = self.post.objects.all().order_by('created_at')
        paginator = Paginator(posts, 6)

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
    form = SignUpForm
    template = 'myblog/signup.html'

    def get(self, request):
        form = self.form
        context = {'form': form}
        return render(request, self.template, context)

    def post(self, request):
        form = self.form(request.POST)
        context = {'form': form}
        if form.is_valid():
            user = form.save()
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        return render(request, self.template, context)
