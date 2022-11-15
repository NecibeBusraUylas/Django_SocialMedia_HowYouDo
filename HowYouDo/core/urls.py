from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'), # home page
    path('signup', views.signup, name='signup'),  # sign up/ register page
    path('signin', views.signin, name='signin'),  # sign in page
    path('logout', views.logout, name='logout'),  # sign in page
    path('settings', views.settings, name='settings'),  # profile settings page
    path('upload', views.upload, name='upload'),  # post upload page
    path('like-post', views.like_post, name='like-post'),
    path('profile/<str:pk>', views.profile, name='profile'), # user's profile page (url will be like /profile/username)
    path('follow', views.follow, name='follow'),
]