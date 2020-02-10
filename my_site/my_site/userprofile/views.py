from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserLoginForm, UserRegisterForm, ProfileForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.http import HttpResponse

# Create your views here.


def user_login(request):
    if request.user.is_authenticated:
        return redirect('post:post_list')  # 必须退出登录才能执行
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            data = user_login_form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return redirect('post:post_list')
            else:
                return HttpResponse("<script>login failed</script>")
        else:
            return HttpResponse("<script>input content error</script>")
    else:
        return render(request, 'userprofile/login.html')


def user_logout(request):
    logout(request)
    return redirect('post:post_list')


def user_register(request):
    if request.user.is_authenticated:
        return redirect('post:post_list')  # 必须退出登录后才能执行
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            return redirect('post:post_list')
        else:
            return HttpResponse("<script>alert('输入不合规');</script>")
    else:
        return render(request, 'userprofile/register.html')


@login_required(login_url='userprofile:login')
def profile_edit(request):

    if Profile.objects.filter(user_id=request.user.id).exists():
        profile = Profile.objects.get(user_id=request.user.id)
    else:
        profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            profile_data = profile_form.cleaned_data
            profile.phone = profile_data['phone']
            profile.bio = profile_data['bio']
            if 'avatar' in request.FILES:
                profile.avatar = profile_data['avatar']
            profile.save()
            return redirect('post:post_list')
        else:
            return HttpResponse("<script>alert('输入不合规');</script>")
    elif request.method == 'GET':
        context = {
            'profile': profile
        }
        return render(request, 'userprofile/edit.html', context)
