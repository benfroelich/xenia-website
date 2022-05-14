from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, reverse
from .models import Post, Comment

def index(request):
    num_posts = 3
    latest_posts = Post.objects.order_by('-pub_date')[:num_posts]
    return render(request, 'blog/index.html', 
            {'latest_posts': latest_posts}
    )

def post(request, post_id):
    # check if the requested post exists
    post = get_object_or_404(Post, pk=post_id)
    comments = list(Comment.objects.filter(post_id=post_id))
    return render(request, 'blog/post.html', {'post': post, 'comments': comments})

def comment(request, post_id):
    try:
        comment = Comment(comment_text = request.POST['comment'], post_id = post_id)
    except (KeyError, Post.DoesNotExist):
        return render(request, 'blog/index.html', {
            'error_message': 'Somehow you tried to post a comment on a blog post which doesn\'t exist'
        }) 
    comment.save()
    return HttpResponseRedirect(reverse('blog:post', args=(post_id,)))


