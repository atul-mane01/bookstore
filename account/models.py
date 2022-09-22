from unicodedata import name
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


CLASS_CHOICES = (
    ("1 st", "1 st"),
    ("2 nd", "2 nd"),
    ("3 rd", "3 rd"),
    ("4 th", "4 th"),
    ("5 th", "5 th"),
    ("6 th", "6 th"),
    ("7 th", "7 th"),
    ("8 th", "8 th"),
)


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, password2=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

# class Book_Store(models.Model):


class Category(models.Model):
	name = models.CharField(max_length=100)
	slug = models.SlugField(max_length=150, unique=True, db_index=True)
	icon = models.FileField(upload_to="category/")
	create_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name


class Book(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	price = models.IntegerField()
	stock = models.IntegerField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	totalreview = models.IntegerField(default=1)
	totalrating = models.IntegerField(default=5)
	status = models.IntegerField(default=0)
	description = models.TextField()


	def __str__(self):
	    return self.name
 
class Student(models.Model):
    student_id=models.AutoField(primary_key=True)
    book_id=models.ForeignKey(Book, on_delete = models.CASCADE)
    student_name=models.CharField(max_length = 100)
    student_class=models.CharField(max_length = 100,choices=CLASS_CHOICES)
    
    def __str__(self):
	    return self.student_name
