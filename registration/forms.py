from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

# https://ordinarycoders.com/blog/article/django-user-register-login-logout
''' add the email field to the user creation form '''
class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-register-form'
        #self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'register'
        self.helper.add_input(Submit('submit', 'Register'))
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

