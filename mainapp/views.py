from django.shortcuts import render, get_object_or_404,redirect
from .models import Message,Post,Comment,Profile
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required



def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # find user by email
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user:
            login(request, user)
            return redirect('home')  # redirect after login
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'login.html')

def signup_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if email already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists. Please log in.")
            return redirect("login")

        # Create a username from the email (before @ part)
        username = email.split("@")[0]

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = name
        user.save()

        messages.success(request, "Account created successfully! Please log in.")
        return redirect("login")

    return render(request, "signup.html")

def chat_view(request):
    username = request.GET.get('username', 'Anonymous')
    messages = Message.objects.all().order_by('timestamp')  # load old messages
    return render(request, 'chat.html', {
        'messages': messages,
        'username': username
    })
def home_view(request):
    posts = Post.objects.all()
    return render(request, 'home.html', {'posts': posts})
def post_create_view(request):
 

    if request.method == "POST":
        image = request.FILES.get('image')
        video = request.FILES.get('video')
        description = request.POST.get('description')

        # save post only if user logged in
        if request.user.is_authenticated:
            Post.objects.create(
                user=request.user,
                image=image,
                video=video,
                description=description
            )
            return redirect('home')
        else:
            return redirect('login')

    return render(request, 'post.html')
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.user:
        post.delete()
        messages.success(request, "Post deleted successfully.")
    else:
        messages.error(request, "You cannot delete this post.")
    return redirect('home')
def add_comment_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Comment.objects.create(user=request.user, post=post, text=text)
    return redirect('home')



@login_required
def profile_view(request, username):
    user = request.user
    profile = getattr(user, 'profile', None)
    
    # Get posts if profile exists
    posts = Post.objects.filter(user=user).order_by('-timestamp') if profile else []

    # Update bio if submitted
    if request.method == "POST" and profile:
        new_bio = request.POST.get('bio')
        if new_bio is not None:
            profile.bio = new_bio
            profile.save()
            return redirect('profile', username=username)

    context = {
        'profile': profile,
        'posts': posts,
    }
    return render(request, 'profile.html', context)
def search_user(request):
    query = request.GET.get('q', '').strip()  # get the search query
    profile = None
    posts = None

    if query:
        try:
            # Search for user by username
            user = User.objects.get(username=query)
            profile = get_object_or_404(Profile, user=user)
            # Get all posts of that user
            posts = Post.objects.filter(user=user).order_by('-timestamp')
        except User.DoesNotExist:
            profile = None
            posts = None

    context = {
        'query': query,
        'profile': profile,
        'posts': posts,
    }
    return render(request, 'search.html', context)