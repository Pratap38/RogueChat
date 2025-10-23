from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('',views.login_view,name='login'),
    path('signup/',views.signup_view,name='signup'),
     path('home/', views.home_view, name='home'),
    path('post/', views.post_create_view, name='post_create'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('comment/<int:post_id>/', views.add_comment_view, name='add_comment'),
    path('chat/', views.chat_view, name='chat'),
      path('profile/<str:username>/', views.profile_view, name='profile'),
       path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
        path('search/', views.search_user, name='search'),
]
