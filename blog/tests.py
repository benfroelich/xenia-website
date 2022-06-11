from django.test import TestCase

import datetime
from django.utils import timezone
from django.urls import reverse

from .models import Post

class PostModelTests(TestCase):
    def test_published_recently_with_future_post(self):
        """ verify that is_recent() returns False for a post
        that was published in the future """
        future = timezone.now() + datetime.timedelta(days=30)
        future_post = Post(pub_date=future, edit_date=future)
        self.assertIs(future_post.is_recent(), False)
    def test_published_recently_with_old_ass_post(self):
        """ verify is_recent() returns False for an old post """
        old_time = timezone.now() + datetime.timedelta(days=-666)
        p = Post(pub_date=old_time, edit_date=old_time)
        self.assertIs(p.is_recent(), False)
    def test_publised_recently_with_new_post(self):
        """ verify is_recent() returns True for a recent post """
        recent_time = timezone.now() - datetime.timedelta(days=2)
        p = Post(pub_date=recent_time, edit_date=recent_time)
        self.assertIs(p.is_recent(), True)

def create_post(title="title", text="fodder", days_offset=0):
    time = timezone.now() + datetime.timedelta(days=days_offset)
    return Post.objects.create(title=title, text=text, pub_date=time, 
            edit_date=time, author='automated_test')

class PostIndexViewTests(TestCase):
    def test_no_posts(self):
        resp = self.client.get(reverse('blog:index'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Nothing is posted")
        self.assertQuerysetEqual(resp.context['latest_posts'], [])

    def test_prev_posts(self):
        post1 = create_post(days_offset=0)
        post2 = create_post(days_offset=-200)
        resp = self.client.get(reverse('blog:index'))
        self.assertQuerysetEqual(resp.context['latest_posts'], [post1, post2])
                
    def test_future_post(self):
        create_post(days_offset=0.01) # future post
        post_past = create_post(days_offset=-1)
        resp = self.client.get(reverse('blog:index'))
        self.assertQuerysetEqual(resp.context['latest_posts'], [post_past])

class PostDetailViewTests(TestCase):
    def test_invalid_pk(self):
        resp = self.client.get(reverse('blog:post', args=(1,)))
        self.assertEqual(resp.status_code, 404)

    def test_future_post(self):
        post = create_post(days_offset=0.01)
        resp = self.client.get(reverse('blog:post', args=(post.pk,)))
        self.assertEqual(resp.status_code, 404)

    def test_past_post(self):
        post = create_post(days_offset=-1000)
        resp = self.client.get(reverse('blog:post', args=(post.pk,)))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, post.text)


