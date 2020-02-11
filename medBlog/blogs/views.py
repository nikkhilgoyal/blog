from django.shortcuts import render, HttpResponse, redirect
from blogs.models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

def blogHome(request):
    allPosts = Post.objects.all()
    paginator = Paginator(allPosts, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'allPosts' : allPosts,'page_obj': page_obj}
    return render(request, "blog/blog.html", context)


def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    context = {'post': post}
    return render(request, 'blog/blogPost.html', context)
def writeBlog(request):
    return render(request, 'blog/newBlog.html')

def addBlog(request):
    if request.method=="POST":
        postTitle = request.POST['postTitle']
        postcontent = request.POST['postContent']
        postAuthorName = request.user#request.POST['postAuthorName']
        postSlug = postTitle.replace(' ','-')
        post = Post(title = postTitle, author = postAuthorName, content = postcontent, slug = postSlug)
        post.save()
        return redirect('/blogs')
    else:
        return redirect('home')
