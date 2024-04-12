from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils import timezone
import jwt, uuid


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        self.model = CustomUser
        email = self.normalize_email(email)
        user = self.model(username=email, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email    

    
class RefreshToken(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=64)
    expired = models.DateTimeField()
    
    @classmethod
    def create(cls, user):
        expired = timezone.now() + timezone.timedelta(days=30)
        return cls(user=user, token=uuid.uuid1(), expired=expired)
    
    def update(self):
        expired = timezone.now() + timezone.timedelta(days=30)
        self.expired = expired
        self.save()
        
    
class AccessToken:
    SECRET_KEY = 'SECRET'
    
    @classmethod
    def create(cls, user_id=0):
        expired = timezone.now() + timezone.timedelta(seconds=3600)
        data = {'expired': expired.timestamp(), 'user_id': user_id}
        token = jwt.encode(data, key=cls.SECRET_KEY, algorithm='HS256')
        return token

    @classmethod
    def decode(cls, token):
        """Decodes and checks the expiration"""
        try:
            data = jwt.decode(token, key=cls.SECRET_KEY, algorithms=['HS256'])
            now = timezone.now().timestamp()
            data['is_valid'] = (now < data['expired'])
            return data
        except ValueError:
            return False
    
    
   
    def __str__(self):
        return self.token