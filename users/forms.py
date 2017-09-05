from django import forms

from .models import User


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.PasswordInput()
    ckey = forms.CharField()

    class Meta:
        model = User
        fields = ['ckey', 'email', 'password']

    def clean_ckey(self) -> str:
        """
        Validate that the supplied ckey is unique.
        """
        ckey = self.cleaned_data['ckey'].lower()
        if User.objects.filter(ckey=ckey).exists():
            raise forms.ValidationError("User with provided ckey already exists.")

        return ckey

    def clean_email(self) -> str:
        """
        Validate that the supplied email address is unique.
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']).exists():
            raise forms.ValidationError(
                "This email address is already in use. Please supply a different email address.")

        return self.cleaned_data['email']

    def save(self, commit=True) -> User:
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
