from django import forms
from Users.models import User


class UserCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """

    class Meta:
        model = User
        fields = ('email', 'FirstName', 'LastName', 'password', 'MultiFA')

    email = forms.EmailField()
    FirstName = forms.CharField(label="FirstName",max_length=25)
    LastName = forms.CharField(label="LastName",max_length=25)
    MultiFA = forms.BooleanField(label='Enable 2-FA',required=False)
    is_admin = forms.BooleanField(label='Administrator',required=False)
    is_staff = forms.BooleanField(label='Staff',required=False)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)
    is_verified = forms.BooleanField(label='Verified',required=False)


    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2


    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm,self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user