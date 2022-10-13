from django.test import TestCase

import json
import datetime
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import mail

from wagtail.test.utils.form_data import nested_form_data, streamfield
from wagtail.test.utils import WagtailPageTests
from wagtail.core.models import Site, Page

from htmlvalidator.client import ValidatingClient

from .models import BlogPost, Comment, Thread, BlogIndex

# remember to prefix any test functions with "test_"

class BlogPostModelTests(WagtailPageTests):
    def test_hierarchy(self):
        self.assertCanCreateAt(BlogIndex, BlogPost)

class CommentModelTests(TestCase):
    def test_creation(self):
        pass

def create_post(title='post title', body='Lorem ipsum dolor sit amet', days_offset=0):
    # first, create a user who will be the owner of the post
    uname = 'test'
    pw = 'aBadPassword123!'
    user = User.objects.create_user(uname, 't@est.com', pw)

    time = timezone.now() + datetime.timedelta(days=days_offset)

    root = Page.objects.get(id=1).specific
    # alternatively, we could just wipe out the db before each test
    index = BlogIndex(path=f"/test_path", depth=1, 
            title="blog idx", slug=f'blog', owner=user)
    post = BlogPost(title=title, 
            first_published_at=time, last_published_at=time, owner=user,
            intro='intro', slug='some-post')
    post.body = json.dumps(
            [
                {'type': 'text', 'value': body}
            ]
        )
    root.add_child(instance=index)
    index.add_child(instance=post)
    site = Site.objects.get(id=1)
    site.root_page = index
    site.save()

    return (uname, pw, post)

#class BlogPostDetailViewTests(TestCase):
#    def test_past_post(self):
#        post = create_post(days_offset=-1000)
#        print(f'get site is {post.get_site()}')
#        resp = self.client.get(post.url_path)
#        self.assertEqual(resp.status_code, 200)
#        self.assertContains(resp, post.body)
#
def create_post_and_thread(self, first_comment):
    # create a post and start a comment thread on it
    (uname, pw, post) = create_post(days_offset = -1)
    self.client.login(username=uname, password=pw)

    resp = self.client.post(reverse('blog:comment', args=(post.pk, 'new')), {'comment': first_comment})
    thread = Thread.objects.get(post_id = post.pk)
    redir = self.client.get(resp.url) # POST should redirect back to the edited page
    return (thread, redir)

class CommentBlogPostTests(TestCase):
    def setUp(self):
        super(type(self), self).setUp()
        self.client = ValidatingClient()

    def test_new_thread(self):
        comment = 'test comment'
        thread, redir = create_post_and_thread(self, comment)
        self.assertContains(redir, comment) # check that the new comment made it onto the blog page

    def test_thread_response(self):
        # create a post and start a comment thread on it
        thread, redir = create_post_and_thread(self, 'hello werld')
        cr = 'test comment response'
        resp = self.client.post(reverse('blog:comment', args=(thread.post.pk, thread.pk)), {'comment': cr})
        redir = self.client.get(resp.url) # POST redirects to the blog post page
        self.assertContains(redir, cr) # check that the new comment made it onto the blog page

    def test_comment_edit(self):
        thread, redir = create_post_and_thread(self, 'first comment')
        change = 'something else'
        c = Comment.objects.get(thread_id = thread.pk)
        c.comment_text = change
        c.save()
        updated_post = self.client.get(thread.post.full_url)
        self.assertContains(updated_post, change) # check that the new comment made it onto the blog page

    def test_comment_gone_on_post_deletion(self):
        thread, redir = create_post_and_thread(self, 'first comment')
        BlogPost.objects.get(pk = thread.post_id).delete()
        self.assertEqual(len(Thread.objects.all()), 0)
        self.assertEqual(len(Comment.objects.all()), 0)

class CommentFlaggingTests(TestCase):
    def setUp(self):
        super(type(self), self).setUp()
        self.client = ValidatingClient()

    def test_comment_flagging(self):
        thread, redir = create_post_and_thread(self, 'first comment')
        c = Comment.objects.get(thread_id = thread.pk)
        self.assertEqual(c.flagged_count, 0)
        resp = self.client.post(reverse('blog:comment-flag', args=(c.thread.post.pk,)), {'comment_id': c.pk})
        c.refresh_from_db()
        self.assertEqual(c.flagged_count, 1)
        self.assertEqual(resp.status_code, 302)

    def test_comment_flagging_notification(self):
        thread, redir = create_post_and_thread(self, 'first comment')
        c = Comment.objects.get(thread_id = thread.pk)
        self.assertEqual(c.flagged_count, 0)
        resp = self.client.post(reverse('blog:comment-flag', args=(c.thread.post.pk,)), {'comment_id': c.pk})
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(c.owner.username, mail.outbox[0].body)
        self.assertIn(resp.wsgi_request.user.username, mail.outbox[0].body)
    
