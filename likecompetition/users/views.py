from django.shortcuts import render ,redirect, get_object_or_404
from django.contrib.auth import authenticate, login as signin, logout as signout
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *

def signup(request):
	err_msg = '' # 에러 메세지
	if request.method == 'POST':
		form = SignupForm(request.POST)

		if form.is_valid():
			email = form.cleaned_data['email'] # 유효성이 검증된 email값
			nickname = form.cleaned_data['nickname'] # ... nickname값
			password = form.cleaned_data['password'] # ... password값
			password_conf = form.cleaned_data['password_conf'] # 유효성이 검증된 password_conf값
			
			if password == password_conf:
				objects = UserManager()
				user = User.objects.create_user( 
					email = email,
					nickname = nickname,
					password = password,
				)
				signin(request, user)
				return redirect('index')
			else:
				err_msg ='비밀번호를 확인하세요'
		else:
			err_msg = '이미 가입된 이메일입니다'

	form = SignupForm()
	return render(request, 'signup.html', {"signupForm": form, 'err_msg':err_msg})
	
def login(request):
	# 로그인된 유저정보는 다음과 같이 가져오면 된다.
	# request.user.값
	err_msg = '' # 에러 메세지
	if request.method == 'POST':
		email = request.POST['email'] # email값(로그인에서는 유효성 검증 없이)
		password = request.POST['password'] # password값
		is_user = authenticate(email=email, password=password) # 사용자 확인

		if is_user:
			signin(request, is_user) # 로그인
			return redirect('index')
		else:
			err_msg = '아이디 혹은 비밀번호가 잘못되었습니다 :3'
			
	form = LoginForm()
	return render(request, 'login.html', {"loginForm": form, 'err_msg':err_msg})

@login_required
def logout(request):
	signout(request)
	return redirect('index')


@login_required
def mypage(request):
	if request.method == 'POST':
		form = MypageForm(request.POST)
		if form.is_valid():
			birth = form.cleaned_data['birth']
			user = get_object_or_404(User, email=request.user.email)
			user.birth = birth
			user.save()
	else:
		form = MypageForm(instance = request.user)
	return render(request, 'mypage.html', {"mypageForm":form})

"""
class PostEditView(LoginRequiredMixin, BaseView):
    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        if not request.user == post.user:
            return redirect('index')
        return render(request, 'post_form.html', {'form': PostForm(instance=post), 'method': 'PUT'})

    def put(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        if not request.user == post.user:
            return redirect('index')
        form = PostForm(request.POST, instance=post)
        if not form.is_valid():
            return render(request, 'post_form.html', {'form': form, 'method': 'PUT', 'error_message': 'Error..'})
        post = form.save(commit=False)
        post.save()
        return redirect('post_detail', post_id=post.id)
"""
