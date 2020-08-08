from django import forms

from .models import User


class SignInForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput())
    remember_me = forms.BooleanField(
        required=False, widget=forms.CheckboxInput())


class SignUpForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['username', ]:
            self.fields[fieldname].help_text = None

    password = forms.CharField(min_length=8, widget=forms.PasswordInput(
        attrs={'placeholder': 'password'}))
    confirm_password = forms.CharField(min_length=8, widget=forms.PasswordInput(
        attrs={'placeholder': 'repeat password'}))
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            self.add_error("password", forms.ValidationError(
                "Passwords didn't matched!"))
            self.add_error("confirm_password", forms.ValidationError(
                "Passwords didn't matched!"))
        return cleaned_data

    def save(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        return User.objects.create_user(username=username, email=email, password=password)
