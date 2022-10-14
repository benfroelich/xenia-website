from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.utils import timezone
from datetime import datetime
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings


from .models import BlogPost, Comment, Thread

def clear_messages(request):
    list(messages.get_messages(request))

# create, update, and delete comments
def comment(request, thread_id, post_id):
    if request.user.is_authenticated:
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
        else:
            messages.error(request, "you must be logged in to use comments")
    page = get_object_or_404(BlogPost, pk=post_id)
    return HttpResponseRedirect(page.get_url())

def notify_admins(comment, request):
    send_mail(
            subject=f'[{get_current_site(request).name}] - Comment Flagged',
            message=f'{request.user} flagged the following comment by {comment.owner} \'{comment.comment_text}\'',
            recipient_list=settings.ADMINS,
            from_email=None
        )

# flag a comment: this marks it as flagged in the database
# and sends details to admins
def flag_comment(request):
    # this is the only method used
    post_id = None
    if request.method == "POST" and request.user.is_authenticated:
        try:
            if 'comment_id' in request.POST and 'post_id' in request.POST:
                post_id = request.POST['post_id']
                comment = Comment.objects.get(pk=request.POST['comment_id'])
                comment.flagged_count += 1
                comment.save()
                messages.success(request, "comment flagged for review, thanks for notifying us")
                notify_admins(comment, request)
            else:
                message.error(request, "must pass comment_id and post_id, please contact administration")
        except (KeyError, BlogPost.DoesNotExist, Comment.DoesNotExist):
            clear_messages(request)
            messages.error(request, 
                    "the post {post_id}, or comment {comment.pk} does not exist")
            return render(request, 'cmsblog/blog_index.html') 
    else:
        messages.error(request, "please log in or register to flag a comment")
    page = get_object_or_404(BlogPost, pk=post_id)
    return HttpResponseRedirect(page.get_url())
