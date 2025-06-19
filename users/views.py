from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm
from django.contrib.auth import login
from django.contrib.auth.models import User

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})

def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'users/profile.html', {'profile_user': user})
# users/views.py
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from .models import Profile
from .forms import ProfileUpdateForm

@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'users/profile_edit.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'username': self.request.user.username})

# users/views.py
from django.contrib import messages

# inside the class ProfileUpdateView
def form_valid(self, form):
    messages.success(self.request, 'Your profile was successfully updated!')
    return super().form_valid(form)
