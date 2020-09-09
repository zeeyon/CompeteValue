from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, email, nickname, new_email, password=None):
        if not email:
            raise ValueError('이메일값이 필요합니다.')

        user = self.model(
            email=self.normalize_email(email),
            new_email=self.normalize_email(email),
            nickname=nickname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password):
        user = self.create_user(
            email=email,
            password=password,
            nickname=nickname,
            new_email=email,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email',
        max_length=50,
        unique=True,
    )
    nickname = models.CharField(
        verbose_name='nickname',
        max_length = 15,
        unique=True,
    )
    
    new_email = models.EmailField(max_length=50, null=True)
    new_mail_auth = models.IntegerField(default=1)


    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    def __str__(self):
        return self.nickname

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    introduction = models.TextField(blank=True, null=True, max_length=100, default='')
    birth = models.DateField(blank=True, null=True)
    gender = models.BooleanField(blank=True, null=True, choices=((False, '남자'), (True, '여자'), (None, '선택안함')), default=None)
    profile_img = models.ImageField(blank=True, null=True, upload_to="profile")
    background_img = models.ImageField(blank=True, null=True, upload_to="background")