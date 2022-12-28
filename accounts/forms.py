from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User


GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'))


class EmployeeRegistrationForm(UserCreationForm):
    # gender = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=GENDER_CHOICES)

    def __init__(self, *args, **kwargs):
        super(EmployeeRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['gender'].required = True
        self.fields['first_name'].label = "First Name"
        self.fields['last_name'].label = "Last Name"
        self.fields['province'].label = "Province"
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Confirm Password"
        self.fields['image'].label = "Profile Picture"
        self.fields['resume'].label = "Resume"

        self.fields['first_name'].widget.attrs.update(
            {
                'placeholder': 'Enter First Name',
            }
        )
        self.fields['last_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Last Name',
            }
        )
        self.fields['province'].widget.attrs.update(
            {
                'placeholder': 'Enter Province',
            }
        )
        self.fields['username'].widget.attrs.update(
            {
                'placeholder': 'Enter Username',
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': 'Enter Email',
            }
        )
        self.fields['password1'].widget.attrs.update(
            {
                'placeholder': 'Enter Password',
            }
        )
        self.fields['password2'].widget.attrs.update(
            {
                'placeholder': 'Confirm Password',
            }
        )
        self.fields['image'].widget.attrs.update(
            {
                'accept': 'image/png, image/gif, image/jpeg',
            }
        )
        self.fields['resume'].widget.attrs.update(
            {
                'accept': 'application/msword, application/pdf',
            }
        )

    class Meta:
        model = User
        fields = [ 'image','first_name', 'last_name','province', 'username', 'email', 'password1', 'password2', 'gender', 'resume']
        error_messages = {
            'first_name': {
                'required': 'First name is required',
                'max_length': 'Name is too long'
            },
            'last_name': {
                'required': 'Last name is required',
                'max_length': 'Last Name is too long'
            },
            'gender': {
                'required': 'Gender is required'
            }
        }

    def clean_gender(self):
        gender = self.cleaned_data.get('gender')
        if not gender:
            raise forms.ValidationError("Gender is required")
        return gender

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.role = "employee"
        if commit:
            user.save()
        return user


class EmployerRegistrationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(EmployerRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = "Company Name"
        self.fields['skill'].label = "Company Description"
        self.fields['experience'].label = "Company Website"
        self.fields['last_name'].label = "Company Address"
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Confirm Password"
        self.fields['image'].label = "Company Profile"

        self.fields['first_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Company Name',
            }
        )
        self.fields['skill'].widget.attrs.update(
            {
                'placeholder': 'Enter Company Description',
            }
        )
        self.fields['experience'].widget.attrs.update(
            {
                'placeholder': 'Enter Company Website',
            }
        )
        self.fields['last_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Company Address',
            }
        )
        self.fields['username'].widget.attrs.update(
            {
                'placeholder': 'Enter Username',
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': 'Enter Email',
            }
        )
        self.fields['password1'].widget.attrs.update(
            {
                'placeholder': 'Enter Password',
            }
        )
        self.fields['password2'].widget.attrs.update(
            {
                'placeholder': 'Confirm Password',
            }
        )

    class Meta:
        model = User
        fields = ['image', 'first_name',"skill" ,"experience", 'last_name', 'username', 'email', 'password1', 'password2']
        error_messages = {
            'first_name': {
                'required': 'First name is required',
                'max_length': 'Name is too long'
            },
            'last_name': {
                'required': 'Last name is required',
                'max_length': 'Last Name is too long'
            }
        }

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.role = "employer"
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.fields['username'].widget.attrs.update({'placeholder': 'Enter username'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Enter password'})

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            self.user = authenticate(username=username, password=password)

            if self.user is None:
                raise forms.ValidationError("User Does Not Exist.")
            if not self.user.check_password(password):
                raise forms.ValidationError("Password Does not Match.")
            if not self.user.is_active or self.user.role == 'inactive-employee' or self.user.role == 'inactive-employer':
                raise forms.ValidationError("User is not Active.")
            
            

        return super(UserLoginForm, self).clean(*args, **kwargs)

    def get_user(self):
        return self.user


class EmployeeProfileUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EmployeeProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update(
            {
                'placeholder': 'Enter First Name',
            }
        )
        self.fields['last_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Last Name',
            }
        )

        self.fields['skill'].widget.attrs.update(
            {
                'placeholder': 'Enter your skill/s.',
            }
        )
        self.fields['experience'].widget.attrs.update(
            {
                'placeholder': 'Enter your experience/s.',
            }
        )
        self.fields['qualification'].widget.attrs.update(
            {
                'placeholder': 'Enter your qualification/s.',
            }
        )

    class Meta:
        model = User
        fields = ["image", "first_name", "last_name", 'province', "gender", 'username', 'email', "skill", "experience", "qualification", 'resume']

        
class EmployerProfileUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EmployerProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = "Company Name"
        self.fields['skill'].label = "Company Description"
        self.fields['experience'].label = "Company Website"
        self.fields['last_name'].label = "Company Address"
        self.fields['image'].label = "Company Profile"

        self.fields['first_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Company Name',
            }
        )
        self.fields['skill'].widget.attrs.update(
            {
                'placeholder': 'Enter Company Description',
            }
        )
        self.fields['experience'].widget.attrs.update(
            {
                'placeholder': 'Enter Company Website',
            }
        )
        self.fields['last_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Company Address',
            }
        )

    class Meta:
        model = User
        fields = ["image","first_name","skill" ,"experience" ,"last_name", "username", "email"]
