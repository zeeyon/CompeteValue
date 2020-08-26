from django.shortcuts import render ,redirect, get_object_or_404, HttpResponse
from django.contrib.auth import authenticate, login as signin, logout as signout, tokens
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.crypto import salted_hmac, constant_time_compare
from django.conf import settings
from django.utils.http import base36_to_int, int_to_base36
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from .forms import *
from .models import *

class MyTokenGenerator(tokens.PasswordResetTokenGenerator):
	def make_token(self, user):
		"""
		Return a token that can be used once to do a password reset
		for the given user.
		"""
		return self._make_token_with_timestamp(user, self._num_days(self._today()))
	
	def check_token(self, token):
		"""
		Check that a password reset token is correct for a given user.
		"""
		if not token:
			return False
		# Parse the token
		try:
			ts_b36, _, pk_b36, auth_36 = token.split("-")
		except:
			return False
		try:
			ts = base36_to_int(ts_b36)
			pk = base36_to_int(pk_b36)//79
			auth = base36_to_int(auth_36)//11
			#print(pk)
			now_user = get_object_or_404(User, pk=pk)
		except:
			return False

		if not auth == now_user.new_mail_auth:
			return False

		if not constant_time_compare(self._make_token_with_timestamp(now_user, ts), token):
			return False
		# Check the timestamp is within limit. Timestamps are rounded to
		# midnight (server time) providing a resolution of only 1 day. If a
		# link is generated 5 minutes before midnight and used 6 minutes later,
		# that counts as 1 day. Therefore, PASSWORD_RESET_TIMEOUT_DAYS = 1 means
		# "at least 1 day, could be up to 2."
		if (self._num_days(self._today()) - ts) > settings.PASSWORD_RESET_TIMEOUT_DAYS:
			#print(4)
			return False
		return True

	def decode_token(self, token):
		try:
			_, _, pk_b36, _ = token.split("-")
		except ValueError:
			return None
		try:
			pk = base36_to_int(pk_b36)
		except ValueError:
			return None
		return pk//79

	def _make_token_with_timestamp(self, user, timestamp):
		# timestamp is number of days since 2001-1-1.  Converted to
		# base 36, this gives us a 3 digit string until about 2121
		ts_b36 = int_to_base36(timestamp)
		pk_b36 = int_to_base36(user.pk*79)
		auth_36 = int_to_base36(user.new_mail_auth*11)
		hash_string = salted_hmac(
			self.key_salt,
			self._make_hash_value(user, timestamp),
			secret=self.secret,
		).hexdigest()[::2]  # Limit to 20 characters to shorten the URL.
		return "%s-%s-%s-%s" % (ts_b36, hash_string, pk_b36, auth_36)


def check_email(user):
	# 사용법:
	# @user_passes_test(check_email, login_url='index')
	#print(user.is_verified)
	try:
		if user.is_verified:
			return True
		return False
	except:
		return False

def email_auth(request, token):
	generator = MyTokenGenerator()
	if generator.check_token(token):
		user = get_object_or_404(User, pk=generator.decode_token(token))
		#print(user, user.is_verified)
		#print('---------------')
		#print(user)
		#print(user.email, user.new_email)
		#print('---------------')
		if not user.email == user.new_email:
			user.email = user.new_email
		user.is_verified = True
		user.save()
		#print(user, user.is_verified)
	return redirect('index')

def send_email_auth(user):
	token = MyTokenGenerator().make_token(user)
	domain = 'http://127.0.0.1:8000'
	auth_url = domain+'/users/activate/'+token
	email_title = "[공가치] 이메일을 인증해주세요"
	email_content = render_to_string('email_form.html', {'url':auth_url})
	email = EmailMessage(email_title, email_content, to=[user.new_email])
	email.content_subtype = "html"
	email.send()

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
					new_email=email,
				)
				#user.new_mail = user.email
				#user.save()
				Profile.objects.create(user=user)
				signin(request, user)
				send_email_auth(user)
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


def set_profile(request):
	profile = get_object_or_404(Profile, user=request.user)
	user = get_object_or_404(User, id=request.user.pk)
	if request.method == 'POST':
		form = ProfileForm(request.POST, request.FILES, instance=profile)
		
		if form.is_valid():
			print('asd', form.cleaned_data['image_profile'])	
			form.save()
		#profile.image_profile = request.FILES['image_profile']
		#profile.save()
		
		return redirect('mypage', user_name=user.nickname)
	else:
		form = ProfileForm(instance = profile)
	return render(request, 'setting.html', {'form':form})

def set_account(request):
	user = get_object_or_404(User, id=request.user.pk)
	if request.method == 'POST':
		form = AccountForm(request.POST, instance=user)
		if form.is_valid():
			if not user.email == form.cleaned_data['new_email']:
				user.new_mail_auth+=1
				user.save()
				#print(request.user.email, form.cleaned_data['new_email'])
				#form.email='asdkj'
				#user.save()
				send_email_auth(user)
			form.save()
			print(user.email, user.new_email,form.cleaned_data['new_email'])
			#print(form.cleaned_data['nickname'], user.nickname)
			return redirect('set_account')#('mypage', user_name=user.nickname)
	else:
		form = AccountForm(instance=user, initial={'new_email':user.email})
	return render(request, 'setting.html', {'form':form})

def set_password(request):
	user = get_object_or_404(User, id=request.user.pk)
	# 프로필 수정 폼을 눌렀다면
	if request.method == 'POST':
		form = NewPasswordForm(request.POST)
		
		if form.is_valid():
			p_o = form.cleaned_data['password_conf']
			p_n = form.cleaned_data['password_new']
			p_n_c = form.cleaned_data['password_new_conf']
			
			if p_n == p_n_c and authenticate(email=request.user.email if request.user.is_authenticated else '', password=p_o):
				user = get_object_or_404(User, email=request.user.email)
				user.set_password(p_n)
				user.save()
		return redirect('mypage', user_name=user.nickname)
	else:
		form = NewPasswordForm()
	return render(request, 'setting.html', {'form':form})
#@user_passes_test(check_email, login_url='index')
def test(request):
	print(request.user.is_verified)
	print(request.user.email, request.user.new_email)
	#print(request.user.is_authenticated)
	#print(request.user.is_verified)
	#if request.user.is_authenticated:
	#	print('hello')
	profile = get_object_or_404(Profile, user=request.user)
	return render(request, 'test.html', {'profile':profile})
	#return HttpResponse(authenticate(email=request.user.email if request.user.is_authenticated else '', password='testtest'))

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


"""
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
				if not request.user.email == account_form.cleaned_data['email']:
					user.is_verified=False
					user.save()
					send_email_auth(user)
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
"""