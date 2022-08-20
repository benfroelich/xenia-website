from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, reverse
from django.urls import reverse
from django.views import generic
from django.utils import timezone

#from django.contrib.auth import User

# Create your views here.
class ProfileView(generic.base.TemplateView):
    template_name = 'user_profile/profile.html'
    context_object_name = 'user'
    # TODO, gather info about this user, like number of posts/comments
    # any active projects, etc
    #def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    context['latest_articles'] = Article.objects.all()[:5]
    #    return context

