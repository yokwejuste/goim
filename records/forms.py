from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, DateInput

from records.models import *


class EventForm(ModelForm):
    class Meta:
        model = Event
        # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {
            'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)


class UserRegistrationForm(UserCreationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    password1 = forms.CharField(label="Password", max_length=20,
                                widget=forms.PasswordInput(
                                    attrs={"class": 'form-control form-control-user'
                                           }
                                )
                                )
    password2 = forms.CharField(label="Confirm Password", max_length=20,
                                widget=forms.PasswordInput(
                                    attrs={"class": 'form-control form-control-user'
                                           }
                                )
                                )

    class Meta:
        model = GoUser
        fields = ('username', 'name', 'email', 'phone', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
            'name': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
            'email': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
            'phone': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
        }


class UserLoginForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    password = forms.CharField(label='password', widget=forms.PasswordInput(
        attrs={"class": 'form-control form-control-user'}
    ))
    username = forms.CharField(label='username', widget=forms.TextInput(
        attrs={"class": 'form-control form-control-user', }
    ))

    class Meta:
        model = GoUser
        fields = ('username', 'password', 'captcha')

    def clean(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            password = self.cleaned_data["password"]

            if not authenticate(username=username, password=password):
                raise forms.ValidationError('Invalid Entries')


class GoCustomerRegistrationForm(forms.ModelForm):
    class Meta:
        model = GoCustomerRegistration
        fields = '__all__'
        TYPE_CHOICES = (
            ('', 'Select a customer type'),
            ('student', 'STUDENT'),
            ('worker', 'WORKER'),
            ('tourist', 'TOURIST'),)
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control w - 30 form-control-user ',
                       'placeholder': 'Enter Customer\'s name', },
            ),
            'email': forms.TextInput(
                attrs={'class': 'form-control w - 30 form-control-user',
                       'placeholder': 'Enter Customer\'s email'},
            ),
            'age': forms.TextInput(
                attrs={'class': 'form-control form-control-user',
                       'placeholder': 'What\'s his age'},
            ),
            'type': forms.Select(
                choices=TYPE_CHOICES,
                attrs={'class': 'form-control form-control-user',
                       'placeholder': 'Which type of Customer is he/she'},
            ),
            'destination': forms.TextInput(
                attrs={'class': 'form-control form-control-user',
                       'placeholder': 'What is his/her Destination'}
            ),
            'photo': forms.ClearableFileInput(
                attrs={'class': 'btn btn-primary d - block btn-user w-100  m-lg-2',
                       'placeholder': 'Drop his/her` picture', },
            ),
            'documents': forms.FileInput(
                attrs={'multiple': False, 'class': ' mb-lg-2 btn btn-primary  m-lg-2'
                                                   ' d-block btn-user w-100',
                       'placeholder': 'Drop his files at once here'},
            ),
            'phone_number': forms.NumberInput(
                attrs={'class': 'form-control form-control-user',
                       'placeholder': 'What is his/her Phone number'}
            ),
        }


class UserProfile(forms.ModelForm):
    class Meta:
        model = GoUser
        fields = ['profile']
        widgets = {
            'profile': forms.ClearableFileInput(
                attrs={'class': 'btn btn-primary d - block btn - user w - 100  m-lg-2',
                       'placeholder': 'Drop his/her` picture', }, )
        }


class GoCustomerStatusForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(GoCustomerStatusForm, self).__init__(*args, **kwargs)
        self.fields['documents'].required = False

    class Meta:
        model = GoCustomerStatus
        fields = '__all__'
        VALUE_CHOICES = (
            ('', 'How far has the customer gone?'),
            (10, '10%'),
            (20, '20%'),
            (30, '30%'),
            (40, '40%'),
            (50, '50%'),
            (60, '60%'),

            (70, '70%'),
            (80, '80%'),
            (90, '90%'),
            (100, 'Felicitations 100%'),
        )
        widgets = {
            'name': forms.Select(
                attrs={'class': 'form-control w - 30 form-control-user ',
                       'placeholder': 'Enter Customer\'s name', },
            ),
            'value': forms.Select(
                choices=VALUE_CHOICES,
                attrs={'class': 'form-control form-control-user',
                       'placeholder': 'Which type of Customer is he/she'},
            ),
            'documents': forms.FileInput(
                attrs={'multiple': False, 'blank': True,
                       'required': False,
                       'class': ' mb-lg-2 btn btn-success  m-lg-2'
                                ' d-block btn-user w-100',
                       'placeholder': 'Drop his files at once here'},
            ),
        }
