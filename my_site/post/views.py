from django.shortcuts import render, redirect
from .models import Post
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import PostCreateForm
from django.contrib.auth.models import User
import markdown
# Create your views here.


def post_list(request):
    if request.user.is_superuser:
        posts = Post.objects.all()
    else:
        posts = Post.objects.filter(is_public=True)
    context = {
        'posts': posts,
    }
    return render(request, 'post/list.html', context=context)


def post_detail(request, id):
    post = Post.objects.get(id=id)
    if post.is_public:
        post.views += 1
        post.save(update_fields=['views'])
        post.body = markdown.markdown(post.body, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            ])
        context = {
            'post': post,
        }
        return render(request, 'post/detail.html', context=context)
    else:
        if request.user.is_superuser:
            context = {
                'post': post,
            }
            return render(request, 'post/detail.html', context=context)
        else:
            return redirect('post:post_list')


@login_required(login_url='userprofile:login')
def post_create(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            post_create_form = PostCreateForm(data=request.POST)
            if post_create_form.is_valid():
                new_post = post_create_form.save(commit=False)
                new_post.user = User.objects.get(id=request.user.id)
                new_post.save()
                post_create_form.save_m2m()  # tags保存方法
                return redirect("post:post_list")
            else:
                return HttpResponse("<script>alert('输入不合规');</script>")
        elif request.method == 'GET':
            return render(request, 'post/create.html')
        else:
            return HttpResponse('<script>please use POST or GET method</script>')
    else:
        return redirect('post:post_list')


@login_required(login_url='userprofile:login')
def post_update(request, id):
    post = Post.objects.get(id=id)
    if request.user.is_superuser:
        if request.method == 'POST':
            post_create_form = PostCreateForm(data=request.POST)
            if post_create_form.is_valid():
                post_data = post_create_form.cleaned_data  # 不清洗数据，在获取 is_public 时会报错，可能是 radio 控件在未勾选提交表单时不会提交数据，导致KeyError错误
                post.title = post_data['title']
                post.body = post_data['body']
                post.is_public = post_data['is_public']
                # post.tags = request.POST['tags']
                post.save()
                # post_create_form.save_m2m()
                return redirect('post:post_detail', id=id)
            else:
                return HttpResponse('input  content error')
        elif request.method == 'GET':
            context = {
                'post': post,
            }
            return render(request, 'post/update.html', context=context)
        else:
            return HttpResponse("<script>please use POST or GET method</script>")
    else:
        return redirect('post:post_list')


def post_delete(request, id):
    pass
