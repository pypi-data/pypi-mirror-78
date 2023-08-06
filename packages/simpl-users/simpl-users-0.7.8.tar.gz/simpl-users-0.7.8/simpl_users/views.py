# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.http import Http404
from django.views.generic import RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from .forms import UserCreationForm, UserChangeForm
from .models import User


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserCreationForm
    fields = ['password', 'last_login', 'is_superuser', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined', 'name', 'external_id', 'data']
    template_name = 'users/user_create.html'
    success_message = '%(name)s was created successfully'

    def get_success_url(self):
        return reverse('users:detail', args=(self.object.email,))


class UserDeleteView(DeleteView):
    model = User
    template_name = 'users/user_delete.html'
    context_object_name = 'user'
    success_message = 'User was deleted successfully'

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse('users:list')


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User

    def get_object(self, queryset=None):
        try:
            user = User.objects.get(email=self.kwargs.get('email'))
            return user
        except User.DoesNotExist:
            raise Http404("User does not exist")


class UserListView(LoginRequiredMixin, ListView):
    model = User
    ordering = ('pk',)

    # TODO: template_name = 'users/user_list.html'
    # TODO: paginate_by = 20
    # TODO: context_object_name = 'user_list'
    # TODO: allow_empty = True


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail",
                       kwargs={"email": self.request.user.email})


class UserUpdateView(LoginRequiredMixin, UpdateView):

    fields = ['name', ]

    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse("users:detail",
                       kwargs={"email": self.request.user.email})

        # TODO: return reverse('users:user_detail', args=(self.object.pk,))

    def get_object(self, queryset=None):
        return self.request.user


class ManageUserUpdateView(UpdateView):
    model = User
    form_class = UserChangeForm
    template_name = 'users/user_update.html'
    context_object_name = 'user'
    success_message = '%(name)s was updated successfully'

    def get_success_url(self):
        return reverse('users:detail', args=(self.object.email,))

    def get_object(self, queryset=None):
        try:
            user = User.objects.get(email=self.kwargs.get('email'))
            return user
        except User.DoesNotExist:
            raise Http404("User does not exist")
