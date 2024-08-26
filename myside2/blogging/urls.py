from django.urls import path
from .views import (BlogListView, CustomLoginView, RegisterPageView,
                    LogoutView, BlogCreateView, HomePageView, BlogUpdateView, BlogDeleteView)

urlpatterns = [
    path('blogs/', BlogListView.as_view(), name='blog_list'),
    path('login/', CustomLoginView.as_view(), name='login_page'),
    path('register/', RegisterPageView.as_view(), name='register_page'),
    path('logout/', LogoutView.as_view(), name='log_out'),
    path('newblog/', BlogCreateView.as_view(), name='new_blog'),
    path('', HomePageView.as_view(), name='home'),
    path('updateblog/<uuid:id>/', BlogUpdateView.as_view(), name='update_blog'),
    path('deleteblog/<uuid:id>/', BlogDeleteView.as_view(), name='delete_blog'),


]
