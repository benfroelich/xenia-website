from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import mail

def make_test_user(name = 'test_user', email = 'test@email.com', 
        password = 'notagoodPassword123!', **kwargs):
    user = User.objects.create_user(name, 
            email, password, **kwargs)
    user.save()
    return user

# integration test of password reset, including email sending
class PasswordResetTests(TestCase):
    def test_reset_for_valid_user(self):
        ''' verify that password reset is working '''
        email = 'test@email.com'
        user = make_test_user(email = email)
        resp = self.client.post(reverse('password_reset'), {'email': email})
        self.assertEqual(resp.status_code, HTTPStatus.FOUND)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [email])


