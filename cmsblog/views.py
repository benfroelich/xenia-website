from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.utils import timezone
from datetime import datetime
from django.contrib import messages


from .models import BlogPost, Comment, Thread

def clear_messages(request):
    list(messages.get_messages(request))

# create, update, and delete comments
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

                        if not comment.deleted:
                            comment.deleted = True
                            messages.success(request, "your comment has been deleted")
                        else:
                            messages.error(request, "this comment was already deleted")
                    else: # handle edit
                        if comment.deleted:
                            messages.error(request, "you cannot edit a deleted comment")
                        else:
                            comment.comment_text = (request.POST['comment'])
                            messages.success(request, "successfully updated your comment")

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
                messages.success(request, "your comment has been posted")
        except (KeyError, BlogPost.DoesNotExist, Thread.DoesNotExist, Comment.DoesNotExist):
            clear_messages(request)
            messages.error(request, 
                    "the post {post.pk}, thread {thread.pk}, or comment {comment.pk} does not exist")
            return render(request, 'cmsblog/blog_index.html') 
        except Comment.ProfanityError as err:
            clear_messages(request)
            messages.error(request, "your comment was rejected due to profanity")
            # TODO: log or notify any profanity
    page = get_object_or_404(BlogPost, pk=post_id)
    return HttpResponseRedirect(page.get_url())


