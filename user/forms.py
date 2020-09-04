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


class ProfileForm(forms.ModelForm):
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['address'].initial = user.address
            self.fields['bio'].initial = user.bio
            self.fields['profile_picture'].initial = user.profile_picture

    bio = forms.CharField(widget=forms.Textarea(
        attrs={'rows': 4}), required=False)
    profile_picture = forms.ImageField(required=False)
    address = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'address', 'bio', 'profile_picture',)

    def save(self, user=None):
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        if first_name:
            first_name = first_name.title()
        if last_name:
            last_name = last_name.title()
        address = self.cleaned_data.get('address')
        if address:
            address = address.title()
        user, created = User.objects.update_or_create(username=user.username, email=user.email, defaults={
            'first_name': first_name,
            'last_name': last_name,
            'address': address,
            'bio': self.cleaned_data.get('bio'),
            'profile_picture': self.cleaned_data.get('profile_picture')
        })
        return user
