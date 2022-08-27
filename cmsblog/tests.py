from django.test import TestCase

import json
import datetime
from django.utils import timezone
from django.urls import reverse

from wagtail.test.utils.form_data import nested_form_data, streamfield
from wagtail.test.utils import WagtailPageTests
from wagtail.core.models import Site

from .models import BlogPost, Comment, Thread, BlogIndex


# remember to prefix any test functions with "test_"

class BlogPostModelTests(WagtailPageTests):
    def test_hierarchy(self):
        self.assertCanCreateAt(BlogIndex, BlogPost)

tracker = 0
def create_post(title='title', body='Lorem ipsum dolor sit amet', days_offset=0):
    global tracker
    time = timezone.now() + datetime.timedelta(days=days_offset)

    # alternatively, we could just wipe out the db before each test
    index = BlogIndex.objects.create(path=f"/{tracker}", depth=1, title="blog idx", slug=f'blg_{tracker}')
    post = BlogPost(title=title, path=f'/p_{tracker}', pub_date=time, edit_date=time, author='test',
            depth=1, intro='intro', slug='slag')
    post.body = json.dumps(
            [
                {'type': 'text', 'value': body}
            ]
        )
    post.save()
    post.save_revision().publish()
    tracker += 1

    site = Site.objects.get(id=1)
    site.root_page = post
    site.save()

    return post
    #return BlogPost.objects.create(parent=index, title=title, body=body, pub_date=time, 
    #        edit_date=time, author='automated_test', path="p", depth=1, intro="intro")

class BlogPostDetailViewTests(TestCase):
    def test_past_post(self):
        post = create_post(days_offset=-1000)
        print(f'get site is {post.get_site()}')
        resp = self.client.get(post.url_path)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, post.body)

def create_post_and_thread(self, first_comment):
    # create a post and start a comment thread on it
    post = create_post(days_offset = -1)
    resp = self.client.post(reverse('blog:comment', args=(post.pk, 'new')), {'comment': first_comment})
    thread = Thread.objects.get(post_id = post.pk)
    print(post.full_url)
    redir = self.client.get(resp.url) # POST redirects to the blog post page
    return (thread, redir)

class CommentBlogPostTests(TestCase):
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
        change = 'comment, redux'
        c = Comment.objects.get(thread_id = thread.pk)
        c.comment_text = change
        c.save()
        print('******')
        print(thread.post.full_url)
        print('******')
        updated_post = self.client.get(thread.post.full_url)
        self.assertContains(updated_post, change) # check that the new comment made it onto the blog page

    def test_comment_gone_on_post_deletion(self):
        thread, redir = create_post_and_thread(self, 'first comment')
        BlogPost.objects.get(pk = thread.post_id).delete()
        self.assertEqual(len(Thread.objects.all()), 0)
        self.assertEqual(len(Comment.objects.all()), 0)

    
