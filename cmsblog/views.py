from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, reverse
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import BlogPost, Comment, Thread

def comment(request, thread_id, post_id):
    try:
        # check if the thread already exists
        if thread_id == 'new': # need to create new thread
            thread = Thread(post_id = post_id)
            thread.save()
        else:
            thread = Thread.objects.get(pk = thread_id)
        comment = Comment(comment_text = request.POST['comment'], owner = request.user, 
                thread_id = thread.pk)
    except (KeyError, BlogPost.DoesNotExist, Thread.DoesNotExist):
        return render(request, 'cmsblog/blog_index.html', {
            'error_message': 'Somehow you tried to post a comment on a blog post thread which doesn\'t exist'
        }) 
    comment.save()
    page = get_object_or_404(BlogPost, pk=post_id)
    return HttpResponseRedirect(page.get_url())

