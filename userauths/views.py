from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm, ProfileForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User
from userauths.models import Profile



User = settings.AUTH_USER_MODEL


# To register users
def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            userame = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {userame} successfully!")
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            return redirect("core:index")
        
    else:
        form = UserRegisterForm()
    
    context = {
        'form': form
    }
    return render(request, "userauths/sign-up.html", context)


# To login users
def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, f"You are already logged in")
        return redirect("core:index")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
       
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {user.username}!")   
            return redirect("core:index")
            
        else:
            messages.warning(request, f"User with {email} does not exist, Create an account")        
    
    return render(request, "userauths/sign-in.html")
            

# To logout users
def logout_view(request):
    logout(request)
    messages.success(request, "You logged out successfully!")
    return redirect("userauths:sign-in")


# To edit user profile
def profile_update(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            new_profile = form.save(commit=False)
            new_profile.user = request.user
            new_profile.save()
            messages.success(request, "Profile updated successfully")
            return redirect("core:user-profile")
        
    else:
        form = ProfileForm(instance=profile)
    
    context = {
        'form': form,
        'profile': profile,
        
    }
    return render (request, "userauths/profile-edit.html", context)