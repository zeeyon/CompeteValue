from django.shortcuts import render ,redirect, get_object_or_404, HttpResponse
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
				Profile.objects.create(user=user)
				signin(request, user)
				return redirect('index')
			else:
				err_msg ='비밀번호를 확인.'
				print(err_msg)
		else:
			err_msg = '이미 가입된 이메일.'
			print(err_msg)

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
			err_msg = '가입하지 않은 아아디, 혹은 잘못된 비밀번호.(문구는 추후 수정~)'
			
	form = LoginForm()
	return render(request, 'login.html', {"loginForm": form, 'err_msg':err_msg})

@login_required
def logout(request):
	signout(request)
	return redirect('index')


#@login_required
def mypage(request, user_name):
	user = get_object_or_404(User, nickname=user_name)
	#if request.method == 'POST':
	#	form = MypageForm(request.POST)
	#	if form.is_valid():
	#		birth = form.cleaned_data['birth']
	#		user = get_object_or_404(User, email=request.user.email)
	#		user.birth = birth
	#		user.save()
	#else:
	#	form = MypageForm(instance = request.user)
	return render(request, 'mypage.html', {'user':user})

@login_required
def setting(request):
	profile = get_object_or_404(Profile, user=request.user)
	user = get_object_or_404(User, id=request.user.pk)

	# 프로필 수정 폼을 눌렀다면
	if request.method == 'POST':
		if 'setting_profile' in request.POST:
			profile_form = ProfileForm(request.POST, instance=profile)
			if profile_form.is_valid():
				profile_form.save()
		elif 'setting_account' in request.POST:
			account_form = AccountForm(request.POST, instance=user)
			if account_form.is_valid():
				account_form.save()
				#이메일 달라졌으면 인증
				#if not request.user.email == account_form.cleaned_data['email']:
		elif 'setting_password' in request.POST:
			new_pass_form = NewPasswordForm(request.POST)
			
			if new_pass_form.is_valid():
				p_o = new_pass_form.cleaned_data['password_conf']
				p_n = new_pass_form.cleaned_data['password_new']
				p_n_c = new_pass_form.cleaned_data['password_new_conf']
				
				if p_n == p_n_c and authenticate(email=request.user.email if request.user.is_authenticated else '', password=p_o):
					user = get_object_or_404(User, email=request.user.email)
					user.set_password(p_n)
					user.save()
		

		return redirect('mypage', user_name=user.nickname)
	else:
		profile_form = ProfileForm(instance = profile)
		new_pass_form = NewPasswordForm()
		account_form = AccountForm(instance=user)
	return render(request, 'setting.html', {'profile_form':profile_form, 'new_pass_form':new_pass_form, 'account_form':account_form})

def test(request):
	print(request.user.is_authenticated)
	#if request.user.is_authenticated:
	#	print('hello')
	return HttpResponse(authenticate(email=request.user.email if request.user.is_authenticated else '', password='testtest'))

"""
프로필 설정:
	(소갯말), 프사, 배사, (생년월일), (성별)
계정 설정:
	(이메일변경), (닉넴변경)
비번 변경:
	(비번변경)

기타:
	비밀번호 재설정
"""