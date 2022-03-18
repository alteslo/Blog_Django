from django.urls import path
from . import views


urlpatterns = [
    path('', views.MainView.as_view(), name='index'),
    path('blog/<slug>/', views.PostDetailView.as_view(), name='post_detail'),
]
