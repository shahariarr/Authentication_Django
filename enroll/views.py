from django.shortcuts import render, HttpResponseRedirect
from .forms import SignUpForm, EditUserProfileForm, \
EditAdminProfileForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, \
PasswordChangeForm, SetPasswordForm, UserChangeForm
from django.contrib.auth import authenticate, login, logout, \
update_session_auth_hash
from django.contrib.auth.models import User

def sign_up(request):
    if request.method == "POST":
        fm = SignUpForm(request.POST)
        if fm.is_valid():
            messages.success(request, 'Account created successfully')
            fm.save()
            return HttpResponseRedirect('/login/')
    else:
        fm = SignUpForm()
    return render(request, 'enroll/signup.html', {'form': fm})

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = AuthenticationForm(request=request, data=request.POST)
            if fm.is_valid():
                user_name = fm.cleaned_data['username']
                user_password = fm.cleaned_data['password']
                user = authenticate(username=user_name, password=user_password)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in successfully !!')
                    return HttpResponseRedirect('/profile/')
        else:
            fm = AuthenticationForm()
        return render(request, 'enroll/userlogin.html', {'form': fm})
    else:
        return HttpResponseRedirect('/profile/')

def user_profile(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            if request.user.is_superuser == True:
                fm = EditAdminProfileForm(request.POST, instance=request.user)
                users = User.objects.all()
            else:
                fm = EditUserProfileForm(request.POST, instance=request.user)
                users = None
            if fm.is_valid():
                messages.success(request, 'Profile updated')
                fm.save()
        else:
            if request.user.is_superuser == True:
                fm = EditAdminProfileForm(instance=request.user)
                users = User.objects.all()
            else:
                fm = EditUserProfileForm(instance=request.user)
                users = None
        return render(request, 'enroll/profile.html', 
            {'name': request.user.username, 'form': fm, 'users': users})
    else:
        return HttpResponseRedirect('/login/')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')

# Change password with old password
def user_change_password(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            fm = PasswordChangeForm(user=request.user, data=request.POST)
            if fm.is_valid():
                fm.save()
                # Update user session
                update_session_auth_hash(request, fm.user)
                messages.success(request, 'Password changed successfully')
                return HttpResponseRedirect('/profile/')
        else:
            fm = PasswordChangeForm(user=request.user)
        return render(request, 'enroll/changePassword.html', {'form': fm})
    else:
        return HttpResponseRedirect('/login/')

# Change password without old password
def user_change_password2(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            fm = SetPasswordForm(user=request.user, data=request.POST)
            if fm.is_valid():
                fm.save()
                # Update user session
                update_session_auth_hash(request, fm.user)
                messages.success(request, 'Password changed successfully')
                return HttpResponseRedirect('/profile/')
        else:
            fm = SetPasswordForm(user=request.user)
        return render(request, 'enroll/changePassword2.html', {'form': fm})
    else:
        return HttpResponseRedirect('/login/')

def user_detail(request, id):
    if request.user.is_authenticated:
        pi = User.objects.get(pk=id)
        fm = EditAdminProfileForm(instance=pi)
        return render(request, 'enroll/userdetail.html', 
            {'name': request.user.username,'form': fm})
    else:
        return HttpResponseRedirect('/login/')