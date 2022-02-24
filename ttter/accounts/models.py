from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.validators import MinLengthValidator, RegexValidator


class MyUserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError('Users must have an username')
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    BLOOD_CHOICES = [("A型", "A型"), ("B型", "B型"), ("AB型", "AB型"), ("O型", "O型")]

    username = models.CharField(verbose_name='username',
                                max_length=10,
                                unique=True,
                                validators=[
                                    MinLengthValidator(5, ),
                                    RegexValidator(r'^[a-zA-Z0-9]*$', )
                                ])
    email = models.EmailField(verbose_name='Email', max_length=50, unique=True)
    nickname = models.CharField(verbose_name='ニックネーム',
                                max_length=10,
                                blank=False,
                                null=False)
    date_of_birth = models.DateField(verbose_name="誕生日", blank=True, null=True)
    blood_type = models.TextField(verbose_name="血液型",
                                  choices=BLOOD_CHOICES,
                                  blank=True,
                                  null=True)
    url = models.URLField(verbose_name='リンク', blank=True, null=True)
    introduction = models.TextField(verbose_name='自己紹介',
                                    max_length=300,
                                    blank=True,
                                    null=True)
    date_joined = models.DateTimeField(verbose_name='登録日', auto_now_add=True)
    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    #AbstractBaseUserにはMyUserManagerが必要
    objects = MyUserManager()
    #一意の識別子として使用されます
    USERNAME_FIELD = 'email'
    #ユーザーを作成するときにプロンプ​​トに表示されるフィールド名のリストです。
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
