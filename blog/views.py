from django.shortcuts import render
from .models import Post

def index(request):
    num_posts = 3
    latest_posts = Post.objects.order_by('-pub_date')[:num_posts]
    return render(
        request, 
        'blog/index.html', 
        {'latest_posts': latest_posts}
    )

def post(request, post_id):
    # check if the requested post exists
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        raise Http404(f'Blog post {post_id} does not exist')
    return render(
        request, 
        'blog/post.html', 
        {'post': post}
    )

def comment(request, post_id):
    return HttpResponse(f'Commenting on {post_id}')


