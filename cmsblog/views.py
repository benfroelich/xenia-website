from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.utils import timezone
from datetime import datetime

from .models import BlogPost, Comment, Thread

#def comment_delete(request, comment_id):
#    if request.method == "DELETE":
#        try:
#            comment = Comment.objects.get(pk=comment_id)
#            comment.delete()
#        except (KeyError, Comment.DoesNotExist):
#            return render(request, 'cmsblog/blog_index.html', {
#                'error_message': 'Could not delete this comment'
#            }) 
#    page = get_object_or_404(BlogPost, pk=post_id)
#    return HttpResponseRedirect(page.get_url())

def comment(request, thread_id, post_id):
    # this api uses POST for updates and new comments
    if request.method == "POST":
        try:
            # check if we are working with an existing post, meaning
            # either edit (PUT) or deletion (DELETE)
            if 'comment_id' in request.POST:
                comment = Comment.objects.get(pk=request.POST['comment_id'])
                # verify that the owner is the current user
                if comment.owner == request.user:
                    # handle deletion
                    if request.POST.get('_method', '').lower() == "delete":
                        # update these here because the form action url uses
                        # dummy pks
                        post_id = request.POST.get('post_id', '').lower()
                        thread_id = request.POST.get('thread_id', '').lower()
                        print(f'setting post_id to {post_id} and thread_id to {thread_id}')
                        comment.comment_text = "This comment has been deleted."
                    else: # handle edit
                        comment.comment_text = request.POST['comment']

                    comment.last_published_at = datetime.now()
                    comment.save()
            else:
                # check if the thread already exists
                if thread_id == 'new': # need to create new thread
                    thread = Thread(post_id = post_id)
                    thread.save()
                else:
                    thread = Thread.objects.get(pk = thread_id)
                # new comment
                comment = Comment(comment_text = request.POST['comment'], 
                        owner = request.user, thread_id = thread.pk)
                comment.save()
        except (KeyError, BlogPost.DoesNotExist, Thread.DoesNotExist, Comment.DoesNotExist):
            return render(request, 'cmsblog/blog_index.html', {
                'error_message': 'Somehow you tried to post a comment on a blog post thread which doesn\'t exist'
            }) 
    page = get_object_or_404(BlogPost, pk=post_id)
    return HttpResponseRedirect(page.get_url())

