from django.urls import path
from django.contrib.auth.views import LogoutView
from django.conf import settings
from . import views


urlpatterns = [
    path('', views.MainView.as_view(), name='index'),
    path('blog/<slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signin/', views.SignInView.as_view(), name='signin'),
    path('signout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='signout',),
    path('contact/', views.FeedBackView.as_view(), name='contact'),
    path('contact/success/', views.SuccessView.as_view(), name='success'),
]
