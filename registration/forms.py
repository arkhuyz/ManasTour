from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class EditProfileForm(forms.ModelForm):
      class Meta:
            model = User
            fields = ["username", "email", "first_name", "last_name"]

            labels = {
                  "username": "Имя пользователя",
                  "email": "Электронная почта",
                  "first_name": "Имя",
                  "last_name": "Фамилия",
            }

            widgets = {
                  "username": forms.TextInput(attrs={
                  "placeholder": "Например: aikhan",
                  }),
                  "email": forms.EmailInput(attrs={
                  "placeholder": "example@mail.com",
                  }),
                  "first_name": forms.TextInput(attrs={
                  "placeholder": "Твоё имя",
                  }),
                  "last_name": forms.TextInput(attrs={
                  "placeholder": "Твоя фамилия",
                  }),
            }