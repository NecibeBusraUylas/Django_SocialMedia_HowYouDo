from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'), # home page
    path('signup', views.signup, name='signup'),  # sign up/ register page
    path('signin', views.signin, name='signin'),  # sign in page
    path('logout', views.logout, name='logout')  # sign in page
]