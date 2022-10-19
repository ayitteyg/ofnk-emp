from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class signupForm(UserCreationForm):
    email = forms.EmailField(max_length=250, required=False)
    def __init__(self, *args, **kwargs):
        super(signupForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields= ('username', 'email', 'password1', 'password2')
