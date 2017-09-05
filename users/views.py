from django.shortcuts import get_object_or_404, redirect, reverse
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
from typing import Dict

from .models import User
from .forms import RegistrationForm


class UserRegistration(CreateView):
    model = User
    form_class = RegistrationForm
    # TODO: redirect to main page
    disallowed_url = None
    template_name = "registration/registration.html"

    @method_decorator(sensitive_post_parameters('password'))
    def dispatch(self, request, *args, **kwargs):
        if not self.registration_allowed():
            return redirect(self.disallowed_url)
        return super(UserRegistration, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        # TODO: redirect to main page
        pass

    def form_valid(self, form):
        return super(UserRegistration, self).form_valid(form)

    def registration_allowed(self):
        return self.request.user.is_anonymous
