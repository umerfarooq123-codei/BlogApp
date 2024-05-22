from django.urls import path
from BlogApp import views

urlpatterns = [
    path('', views.home, name="Home"),
    path('gen/', views.generatePosts, name="Posts"),
    path('addPost/', views.addPost, name='addPost'),
    path('login/', views.login_user, name="Login"),
    path('register/', views.register, name="Register"),
    path('logout/', views.logout_user, name="Logout"),
    path('forgot-password/', views.forgotpass, name="ForgotPassword"),
    path('category/<str:category>/', views.category_view, name='category_view'),
]
