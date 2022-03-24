from django.shortcuts import render, get_object_or_404
from django.views import View
from django.core.paginator import Paginator
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q
from django.core.mail import send_mail, BadHeaderError

from .models import Post
from .forms import SignUpForm, SignInForm, FeedBackForm
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


class SignInView(View):
    template = 'myblog/signin.html'

    def get(self, request):
        form = SignInForm()
        return render(request, self.template, context={
            'form': form,
        })

    def post(self, request):
        form = SignInForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, self.template, context={
            'form': form,
        })


class FeedBackView(View):
    def get(self, request, *args, **kwargs):
        form = FeedBackForm()
        return render(request, 'myblog/contact.html', context={
            'form': form,
            'title': 'Написать мне'
        })

    def post(self, request, *args, **kwargs):
        form = FeedBackForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            from_email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            try:
                send_mail(f'От {name} | {subject}', message, from_email, ['alteslo31@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Невалидный заголовок')
            return HttpResponseRedirect('success')
        return render(request, 'myblog/contact.html', context={
            'form': form,
        })


class SuccessView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'myblog/success.html', context={
            'title': 'Спасибо'
        })


class SearchResultsView(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')
        results = ""
        if query:
            results = Post.objects.filter(
                Q(h1__icontains=query) | Q(content__icontains=query)
            )
        paginator = Paginator(results, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'myblog/search.html', context={
            'title': 'Поиск',
            'results': page_obj,
            'count': paginator.count
        })
