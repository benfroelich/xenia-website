from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import mail

def make_test_user(name = 'test_user', email = 'test@email.com', 
        password = 'password123', **kwargs):
    user = User.objects.create_user(name, 
            email, password, **kwargs)
    user.save()
    return user

class PasswordResetTests(TestCase):
    def test_reset_for_valid_user(self):
        ''' verify that password reset is working '''
        user = make_test_user()
        resp = self.client.post(reverse('password_reset'),
                args=(user,))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertContains(mail.outbox[0].subject, 'Reset')


