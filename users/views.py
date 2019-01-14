# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import DeleteView, ListView
from django.contrib.auth.models import User
from django.views import View

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, MessageNewForm
from .models import Profile, Messages


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,
                                         request.FILES, # to jest do zapisywania jpg
                                         instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'users/profile.html', context)

class UserDeleteForm(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    success_url = '/'

    def test_func(self):
        user = self.get_object()
        if self.request.user == user:
            return True
        return False


class MessagesReceivedListView(LoginRequiredMixin, View):

    def get(self, request):
        msg = Messages.objects.filter(send_to= request.user).order_by('-date_send')
        return render(request, 'users/messages_received.html', {'msg':msg})


class MessagesSentListView(LoginRequiredMixin, View):

    def get(self, request):
        msg = Messages.objects.filter(send_from = request.user).order_by('-date_send')
        return render(request, 'users/messages_sent.html', {'msg':msg})


class MessageNewView(LoginRequiredMixin, View):

    def get(self, request):
        form = MessageNewForm
        return render(request, 'users/messages_form.html', {'form': form})

    def post(self, request):
        form = MessageNewForm(request.POST)
        if form.is_valid():
            send_to = form.cleaned_data.get('send_to')
            title = form.cleaned_data.get('title')
            message = form.cleaned_data.get('message')
            save_form = Messages.objects.create(title=title, message=message, send_from=request.user, send_to=send_to)
            messages.success(request, "Your message has already been sent!")
            return redirect('messages-received')