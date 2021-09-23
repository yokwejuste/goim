from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.urls import reverse

User = settings.AUTH_USER_MODEL


class GoUserManager(BaseUserManager):
    # defining a function or method that will create user
    def create_user(self, username, email, name, phone, password):
        if not username:
            raise ValueError("Username is required")
        if not email:
            raise ValueError('Email is required')
        if not phone:
            raise ValueError('An appropriate phone number is required')
        if not name:
            raise ValueError("Enter your correct names")

        user = self.model(
            username=username,
            email=email,
            phone=phone,
            name=name,
            password=password
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Creating our superuser
    def create_superuser(self, username, email, phone, name, password):
        user = self.create_user(
            username=username,
            email=email,
            phone=phone,
            password=password,
            name=name
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class GoUser(AbstractBaseUser):
    username = models.CharField(verbose_name='Username', max_length=60, unique=True)
    email = models.EmailField(verbose_name='Email Address', max_length=60, unique=True)
    name = models.CharField(verbose_name='Full Name', max_length=200, unique=True)
    phone = models.CharField(verbose_name="Phone Number", max_length=20, null=False)
    date_joined = models.DateTimeField(verbose_name='Created On', auto_now_add=True)
    profile = models.ImageField(verbose_name='Picture', upload_to=f'profiles/%Y/{username}',
                                default='profile1.png',
                                null=False)
    last_login = models.DateTimeField(verbose_name='Last login', auto_now=True, null=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    # Fields to login to app
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'phone', 'email']

    def __str__(self):
        return self.username

    objects = GoUserManager()

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    class Meta:
        verbose_name = "User"
        verbose_name_plural = 'Users'


class GoCustomerRegistration(models.Model):
    name = models.CharField(max_length=300, verbose_name='Full name')
    type = models.CharField(max_length=20, verbose_name='Customer Type')
    destination = models.CharField(max_length=30, null=False, verbose_name='Destination')
    time_of_submission = models.DateTimeField(auto_now_add=True, null=False, verbose_name=' Submit Time')
    age = models.IntegerField(verbose_name="Age", null=False)
    photo = models.ImageField(max_length=10000, verbose_name='Customer Picture',
                              null=False, upload_to='customers/profiles/')
    documents = models.FileField(upload_to='%Y/customers/documents/')
    phone_number = models.IntegerField(verbose_name='Phone number')
    email = models.EmailField(null=False)

    class Meta:
        ordering = ["time_of_submission"]
        verbose_name = "Customer Registration"
        verbose_name_plural = "Customers Registration"

    def __str__(self):
        return self.name


class GoCustomerStatus(models.Model):
    name = models.OneToOneField(GoCustomerRegistration,
                                max_length=300, verbose_name='Full name',
                                on_delete=models.CASCADE, primary_key=True,
                                null=False,
                                )
    value = models.IntegerField(default=0, verbose_name='Level', null=False, primary_key=False)

    class Meta:
        verbose_name_plural = 'Customers Status'
        verbose_name = 'Customer\'s Status'

    def __str__(self):
        return self.name.name


class Event(models.Model):
    customer = models.OneToOneField(GoCustomerRegistration,
                                    primary_key=True,
                                    unique=True,
                                    verbose_name='Customer\'s name',
                                    on_delete=models.CASCADE, )
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    @property
    def get_html_url(self):
        url = reverse('event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'

    def __str__(self):
        return self.title
