from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.utils import timezone
from datetime import datetime

from .models import BlogPost, Comment, Thread

def comment(request, thread_id, post_id):
    if request.method == "POST":
        try:
            # check if the thread already exists
            if thread_id == 'new': # need to create new thread
                thread = Thread(post_id = post_id)
                thread.save()
            else:
                thread = Thread.objects.get(pk = thread_id)
            # check if this is an update or a new comment
            if 'comment_pk' in request.POST:
                comment = Comment.objects.get(pk=request.POST['comment_pk'])
                print("here we are")
                if comment.owner == request.user:
                    print("inner")
                    comment.comment_text = request.POST['comment']
                    comment.last_published_at = datetime.now()
                    comment.save()
            else:
                # then verify that the owner is the current user
                comment = Comment(comment_text = request.POST['comment'], 
                        owner = request.user, thread_id = thread.pk)
                comment.save()
        except (KeyError, BlogPost.DoesNotExist, Thread.DoesNotExist, Comment.DoesNotExist):
            return render(request, 'cmsblog/blog_index.html', {
                'error_message': 'Somehow you tried to post a comment on a blog post thread which doesn\'t exist'
            }) 
    page = get_object_or_404(BlogPost, pk=post_id)
    return HttpResponseRedirect(page.get_url())

