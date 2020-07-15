from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# post의 상세 내용을 보여줌, 댓글 기능 추가
def post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(post=post)
    if request.method == 'POST':
        form = CommentForm(request.POST) # 입력된 내용을 form 변수에 저장
        if form.is_valid(): # form이 유효하면(models.py에서 정의한 필드에 적합하면)
            comment = form.save(commit=False) # form 데이터를 가져온다
            comment.post = post
            comment.user = request.user
            comment.save() # form 데이터를 db에 저장한다
    form = CommentForm()
    return render(request, 'post.html', {'post':post, 'form':form, 'comments':comments})

# post를 넘겨줌
def index(request, page=1):
    posts = Post.objects.all()
    paginator = Paginator(posts, 5)
    posts = paginator.get_page(page)
    return render(request, 'index.html', {'posts':posts})

# post 만드는 메소드
@login_required
def create_post(request):
    if request.method == 'GET':
        form = PostForm()
        return render(request, 'create.html', {'form': form})
    form = PostForm(request.POST) # 입력된 내용을 form 변수에 저장
    if form.is_valid(): # form이 유효하면(models.py에서 정의한 필드에 적합하면)
        post = form.save(commit=False) # form 데이터를 가져온다
        post.user = request.user
        post.save() # form 데이터를 db에 저장한다
    return redirect('post', post_id=post.id)

# post 수정하는 메소드
@login_required
def update_post(request, post_id): # post_id로 수정하고자 하는 post 객체를 get
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.user:
        return redirect('index')
    if request.method == 'GET':
        form = PostForm(instance=post)
        return render(request, 'update.html', {'form':form})
    form = PostForm(request.POST, instance=post)
    if form.is_valid():
        post = form.save(commit=False)
        post.save()
    return redirect('post', post_id=post.pk)

# post 삭제하는 메소드
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user == post.user:
        post.delete() # Post db에서 post 객체 삭제
    return redirect('index')
