from random import choice
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import os
import datetime
import requests
from .models import Post
from django.conf import settings
from faker import Faker
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.conf import settings
from datetime import datetime

fake = Faker()
# Create your views here.


listOfCategories = [
    "Home",
    "Politics",
    "Tech",
    "Entertainment",
    "Travel",
    "Sports",
]

# @login_required(login_url='/login/')


def home(request):
    posts = Post.objects.all()
    for post in posts:
        post.updated_at = post.updated_at.strftime('%B %d, %Y')
    content = {"posts": posts, 'page': "Home"}
    return render(request, "home.html", context=content)


@login_required(login_url='/login/')
def addPost(request):
    if request.method == "POST":
        data = request.POST
        image = request.FILES
        title_ = data.get("title")
        author = data.get("author")
        content = data.get("content")
        created_at = data.get("created_At")
        updated_at = data.get("updated_at")
        is_published = data.get("is_published")
        slug = data.get("slug")
        image_file = image.get("image")

        if is_published == "on":
            is_published = True
        else:
            is_published = False

        Post.objects.create(
            title=title_,
            content=content,
            author=author,
            created_at=created_at,
            updated_at=updated_at,
            slug=slug,
            is_published=is_published,
            image=image_file
        )
        return redirect("/")

    # If the user was redirected from the addPost page, store the original URL in session
    if request.GET.get('next') == reverse('addPost'):
        request.session['add_post_redirect'] = True
    else:
        request.session.pop('add_post_redirect', None)

    listOfCategories = [
        "Home",
        "Politics",
        "Tech",
        "Entertainment",
        "Travel",
        "Sports",
    ]
    content = {"user": request.user, "categories": listOfCategories}
    return render(request, "addpost.html", context=content)


@login_required(login_url='/login/')
def generatePosts(request):
    for _ in range(10):
        user = User.objects.order_by('?').first()
        title = fake.sentence()
        content = fake.paragraph(max(10, 100))

        created_at = fake.date_time_between(
            start_date='-1y', end_date='now', tzinfo=datetime.timezone.utc)
        updated_at = fake.date_time_between(
            start_date='+1d', end_date='+1y', tzinfo=datetime.timezone.utc)
        is_published = fake.boolean(chance_of_getting_true=50)
        slug = fake.slug()
        image_url = fake.image_url()

        image_name = os.path.basename(image_url)
        image_path = os.path.join(settings.MEDIA_ROOT, image_name)
        response = requests.get(image_url)
        with open(image_path, 'wb') as f:
            f.write(response.content)

        category = choice(listOfCategories)

        Post.objects.create(
            author=user,
            title=title,
            content=content,
            created_at=created_at,
            updated_at=updated_at,
            is_published=is_published,
            slug=slug,
            image=image_name,
            category=category,
        )
    return redirect("/")


def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username)

        if user.exists():
            messages.error(request, "Username already taken !")
            request.session['first_name'] = first_name
            request.session['last_name'] = last_name
            request.session['username'] = username
            return redirect('/register/')

        user = User.objects.create(
            last_name=last_name, first_name=first_name, username=username
        )
        user.set_password(password)
        user.save()
        messages.success(request, "User has been created successfully")
        return redirect('/login/')
    return render(request, 'register.html')


def login_user(request):
    next_url = "/"
    if request.method == "POST":
        if 'next' in request.GET:
            next_url = request.GET['next']

        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        if not User.objects.filter(username=username).exists():
            messages.error(request, "User doesn't exist!")
            request.session['login_username'] = username
            return redirect(reverse('Login'))

        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, 'Incorrect password!')
            request.session['login_username'] = username
            return redirect(reverse('Login'))
        else:
            login(request=request, user=user)
            if remember_me:
                response = redirect(next_url)
                response.set_cookie('remember_username',
                                    username, max_age=3600 * 24 * 30)
                response.set_cookie('remember_password',
                                    password, max_age=3600 * 24 * 30)
                return response
            else:
                response = redirect(next_url)
                response.delete_cookie('remember_username')
                response.delete_cookie('remember_password')
                return response

    return render(request, 'login.html', context={'page': "Login"})


def logout_user(request):
    logout(request)
    return redirect('/')


def forgotpass(request):
    return render(request, "forgotpass.html")


def category_view(request, category):
    posts = Post.objects.filter(category=category)
    content = {"posts": posts, 'page': category}
    return render(request, 'category_view.html', context=content)
