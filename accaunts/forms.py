from django import forms
from django.contrib.auth import authenticate,get_user_model
User=get_user_model()

class UserLoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput())

    def clean(self,*args, **kwargs):
        username=self.cleaned_data.get('username')
        password=self.cleaned_data.get('password')

        if username and password:
            try:
                user=User.objects.get(username=username)
            except:
                user=None
            if not user:
                raise forms.ValidationError("User does not exist with this username")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect password.")
            if not user.is_active:
                raise forms.ValidationError("This user is not active.")
        return super(UserLoginForm,self).clean(*args, **kwargs)

    
class UserRegistrationForm(forms.ModelForm):
    email=forms.EmailField(label='Email address',required=True)
    password=forms.CharField(widget=forms.PasswordInput)
    password2=forms.CharField(widget=forms.PasswordInput,label='Confirm Password')
    
    class Meta:
        model=User
        fields=['username',
                'email',
                'password',
                'password2']
    
    def clean_email(self):
        email=self.cleaned_data.get('email')
        try:
            user=Uer.objects.get(email=email)
        except:
            user=None
        if user:
            raise forms.ValidationError('User exists with this email.')
        return email

    

    def clean_password2(self):
        password=self.cleaned_data.get('password')
        password2=self.cleaned_data.get('password2')

        if password!=password2:
            raise forms.ValidationError('Passwords does not match.')

        return password2
    def clean_password(self):
        password=self.cleaned_data.get('password')
        if len(password)<5:
            raise forms.ValidationError('Password is too short. It must contain at least 5 chars.')
        if password.isdigit() or password.isalpha():
            raise forms.ValidationError('Password must contain at least one letter and one digit.')
        return password
