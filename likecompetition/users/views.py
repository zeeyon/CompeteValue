from django.shortcuts import render ,redirect, get_object_or_404, HttpResponse
from django.contrib.auth import authenticate, login as signin, logout as signout, tokens
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.crypto import salted_hmac, constant_time_compare
from django.conf import settings
from django.utils.http import base36_to_int, int_to_base36
from django.core.mail import EmailMessage
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
			ts_b36, _, pk_b36 = token.split("-")
		except:
			return False
		try:
			ts = base36_to_int(ts_b36)
			pk = base36_to_int(pk_b36)//79
			#print(pk)
			now_user = get_object_or_404(User, pk=pk)
		except:
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
			_, _, pk_b36 = token.split("-")
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
		hash_string = salted_hmac(
			self.key_salt,
			self._make_hash_value(user, timestamp),
			secret=self.secret,
		).hexdigest()[::2]  # Limit to 20 characters to shorten the URL.
		return "%s-%s-%s" % (ts_b36, hash_string, pk_b36)

	#def _nextday(self):
	#	return date.fromtimestamp(time()+86400*1) # one-day: 60*60*24

def check_email(user):
	print(user.is_verified)
	try:
		if user.is_verified:
			return True
		return False
	except:
		return False


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
				send_email_auth(user)
				return redirect('index')
			else:
				err_msg ='비밀번호를 확인.'
		else:
			err_msg = '이미 가입된 이메일.'

	form = SignupForm()
	return render(request, 'signup.html', {"signupForm": form, 'err_msg':err_msg})

#class HasherTest(Argon2PasswordHasher):
#	def decode(self, password, salt):
#		return 

@login_required
def test(request):
	# 임시 뷰
	#day_unit = 60*60*24
	b = MyTokenGenerator().make_token(request.user)
	c = MyTokenGenerator().check_token(b)
	d = MyTokenGenerator().decode_token(b)
	#encoded = encode({"user_email":"ssw3095@naver.com"}, 'eeeee9', 'HS256')#Argon2PasswordHasher().encode("ssw3095@naver.com", "kong245675")
	#decoded = decode(encoded, 'eeeee9', 'HS256')['user_email']#Argon2PasswordHasher()._decode(encoded)
	#t1, t2 = b.split('-')
	#t1 = base36_to_int(t1)
	#t2 = base36_to_int(t2)

	#tes = date.fromtimestamp(time()-day_unit)
	#res = tokens.PasswordResetTokenGenerator().check_token(request.user, tes)
	#tttttt = get_object_or_404(User, pk=request.user.pk)

	return HttpResponse([b, '</br>', c, d])#[encoded.split('.'), "</br>", decoded])

def email_auth(request, token):
	generator = MyTokenGenerator()
	if generator.check_token(token):
		user = get_object_or_404(User, pk=generator.decode_token(token))
		#print(user, user.is_verified)
		user.is_verified = True
		user.save()
		#print(user, user.is_verified)
		return HttpResponse(generator.check_token(token))
	else:
		return redirect('index')

def send_email_auth(user):
	token = MyTokenGenerator().make_token(user)
	auth_url = 'http://127.0.0.1:8000/users/activate/'+token
	email_title = "[공가치] 이메일 인증 테스트"
	email_content = """
	이메일 인증 테스트 메일입니다.
	링크:"""+auth_url
	email = EmailMessage(email_title, email_content, to=[user.email])
	email.send()


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


@login_required
@user_passes_test(check_email, login_url='index')
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
