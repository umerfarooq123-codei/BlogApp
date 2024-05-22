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
    path('transactions/', views.list_of_transactions, name="AllTransactions"),
]
