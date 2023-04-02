from . import views
from django.urls import path

urlpatterns = [
    path("", views.PostList.as_view(), name='home'),
    path('category/<str:category>', views.PostCategory.as_view(), name='category'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='news/post_detail'),
]
