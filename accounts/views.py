# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Profile
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
# Handle user registration

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Don't create Profile manually here
            messages.success(request, 'Account created! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})




@login_required
def profile(request):
    return render(request, 'accounts/profile.html')




from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ProfileUpdateForm

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the same page after successful update
    else:
        form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'accounts/profile.html', {'form': form})

def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    return render(request, 'accounts/profile.html', {'profile': profile})
    ...

from django.contrib.auth.views import LogoutView

class LogoutViewAllowGet(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile', username=request.user.username)
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'accounts/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserUpdateForm, ProfileUpdateForm

@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile', username=request.user.username)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'accounts/edit_profile.html', {
        'u_form': u_form,
        'p_form': p_form
    })

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ProfileForm  # Your custom form class

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=request.user.profile)

    return render(request, 'accounts/edit_profile.html', {'form': form})

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile  # get Profile instance

    return render(request, 'accounts/profile.html', {
        'profile_user': user,
        'profile': profile
    })

def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    return render(request, 'accounts/profile.html', {
        'profile_user': user,
        'profile': profile,
    })
