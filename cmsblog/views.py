from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, reverse
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import BlogPost, Comment, Thread

class IndexView(generic.ListView):
    template_name = 'cmsblog/index.html'
    context_object_name = 'latest_posts'
    num_items = 3

    def get_queryset(self):
        """ return the last 'num_items' posts """
        return Post.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:self.num_items]

class PostView(generic.DetailView):
    template_name = 'cmsblog/post.html'
    context_object_name = 'post'
    model = BlogPost
    def get_queryset(self):
        """ excludes unpublished content """
        return Post.objects.filter(pub_date__lte=timezone.now())

def comment(request, thread_id, post_id):
    try:
        # check if the thread already exists
        if thread_id == 'new': # need to create new thread
            thread = Thread(post_id = post_id)
            thread.save()
        else:
            thread = Thread.objects.get(pk = thread_id)
        comment = Comment(comment_text = request.POST['comment'], thread_id = thread.pk)
    except (KeyError, Post.DoesNotExist, Thread.DoesNotExist):
        return render(request, 'cmsblog/index.html', {
            'error_message': 'Somehow you tried to post a comment on a blog post thread which doesn\'t exist'
        }) 
    comment.save()
    return HttpResponseRedirect(reverse('blog:post', args=(post_id,)))


# Create your views here.
