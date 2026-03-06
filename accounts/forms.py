from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class SignupForm(forms.ModelForm):

  password = forms.CharField(widget=forms.PasswordInput)
  confirm_password = forms.CharField(widget=forms.PasswordInput)

  class Meta:
    model = User
    fields = ["username", "email", "password"]

  def clean_username(self):
    username = self.cleaned_data.get("username")
    if User.objects.filter(username=username).exists():
      raise forms.ValidationError("This username is already taken")
    
    return username
  
  def clean_email(self):
    email = self.cleaned_data.get("email")
    if User.objects.filter(email=email).exists():
      raise forms.ValidationError("This email is already registered")
    
    return email
  
  def clean_password(self):
    password = self.cleaned_data.get("password")
    if len(password) < 8:
      raise forms.ValidationError("Password must be atleast 8 characters long")
    
    return password

  def clean(self):
    cleaned_data = super().clean()
    password = cleaned_data.get("password")
    confirm_password = cleaned_data.get("confirm_password")

    if password and confirm_password and password != confirm_password:
      self.add_error("confirm_password", "Passwords do not match")
    
    return cleaned_data

class LoginForm(AuthenticationForm):

  username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username"}))

  password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))

  def clean(self):
    cleaned_data = super().clean()
    username = cleaned_data.get("username")
    password = cleaned_data.get("password")

    if username and not User.objects.filter(username=username).exists():
      self.add_error("username", "This username does not exist")

    if username and password:
      user = User.objects.filter(username=username).first()
      if user and not user.check_password(password):
        self.add_error("password", "Incorrect password")
    
    return cleaned_data
