from django.shortcuts import render,redirect
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
				err_msg ='비밀번호를 확인.'
		else:
			err_msg = '이미 가입된 이메일.'

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
			err_msg = '가입하지 않은 아아디, 혹은 잘못된 비밀번호.'
			
	form = LoginForm()
	return render(request, 'login.html', {"loginForm": form, 'err_msg':err_msg})

@login_required
def logout(request):
	signout(request)
	return redirect('index')

def mypage(request):
    return render(request, 'mypage.html')