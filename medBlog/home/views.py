from django.shortcuts import render, HttpResponse, redirect
from .models import Contact, Relationship
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from blogs.models import Post
# Create your views here.

def home(request):

    return render(request, 'home/home.html')
    #return render(request, 'home/home.html')

def contact(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        contact = Contact(name=name, email = email, message = message)
        contact.save()
    return render(request, 'home/contact.html')

def search(request):
    query = request.GET['query']
    if len(query) < 1:
        return redirect('/blogs')
    else:
        allPost = Post.objects.filter(title__icontains=query)
        params = {'allPost':allPost, 'query':query}
        return render(request,"home/search.html",params)

def handleSignup(request):
    if request.method=='POST':
        fname = request.POST['fname']
        email = request.POST['email']
        pass1 = request.POST['pass1']

        myuser = User.objects.create_user(fname, email, pass1)
        myuser.save()
        return redirect('home')
    else:
        return HttpResponse("Please retry correctly")

def handleLogin(request):
    if request.method=='POST':
        loginUsername = request.POST['loginUsername']
        loginPass = request.POST['loginPass']

        user = authenticate( username=loginUsername,  password=loginPass)
        if user is not None:
            login(request, user)
            return redirect(home)
        else:
            return redirect(home)
    else:
        return HttpResponse('need post req.')



def handleLogout(request):
    logout(request)
    return redirect(home)
@login_required
def handleAccPass(request):
    if request.method=="POST":
        newPass = request.POST['newPass']
        userr = request.user
        userr.set_password(newPass)
        userr.save()
        logout(request)
        return redirect(home)
def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    context = {'post': post}
    return render(request, 'blog/blogPost.html', context)
def follow(req):
    follow_user = req.POST.get('follow')
    if User.objects.filter(username = follow_user).exists():
        followed = User.objects.get(username = follow_user)
        follower = req.user
        relation, created = Relationship.objects.get_or_create(whom=followed, who=follower)
        if created:
            return HttpResponse(follower.username + " followed " + followed.username)
        return HttpResponse(follower.username + " already followed " + followed.username)
    else:
        print('else')
        return redirect(home)
def following(req):
    following_users = Relationship.objects.filter(who = req.user).values('whom')
    result = []
    for items in following_users:
        result.append(User.objects.get(id = items['whom']).username)
    return HttpResponse(result)
