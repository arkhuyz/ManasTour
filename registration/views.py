import re

from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError, transaction
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import EditProfileForm


User = get_user_model()


def login_view(request):
      if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(
                  request,
                  username=username,
                  password=password
            )

            if user is not None:
                  login(request, user)
                  return redirect("home")

            return render(
                  request,
                  "registration/login.html",
                  {"form": {"errors": True}}
            )

      return render(request, "registration/login.html")



def register_view(request):
      if request.user.is_authenticated:
            return redirect("home")

      if request.method == "POST":
            username = request.POST.get("username", "").strip()
            email = request.POST.get("email", "").strip().lower()

            password1 = request.POST.get("password1", "")
            password2 = request.POST.get("password2", "")

            agreement = request.POST.get("agreement")

            errors = {}

            # =========================
            # USERNAME
            # =========================

            if not username:
                  errors["username"] = "Введите логин."

            elif len(username) < 3:
                  errors["username"] = (
                  "Логин должен содержать минимум 3 символа."
                  )

            elif len(username) > 150:
                  errors["username"] = "Логин слишком длинный."

            elif not re.match(r"^[\w.@+-]+$", username):
                  errors["username"] = (
                  "Логин может содержать только буквы, "
                  "цифры и символы @ . + - _"
                  )

            elif User.objects.filter(
                  username__iexact=username
            ).exists():
                  errors["username"] = (
                  "Пользователь с таким логином уже существует."
                  )

            # =========================
            # EMAIL
            # =========================

            if not email:
                  errors["email"] = "Введите Email."

            else:
                  
                  try:  
                        validate_email(email)

                  except ValidationError:
                        errors["email"] = (
                              "Введите корректный Email."
                        )

                  else:
                        if User.objects.filter(
                              email__iexact=email
                        ).exists():
                              errors["email"] = (
                                    "Пользователь с таким Email "
                                    "уже зарегистрирован."
                              )

            # =========================
            # ПАРОЛЬ
            # =========================

            if not password1:
                  errors["password1"] = "Введите пароль."

            elif len(password1) < 8:
                  errors["password1"] = (
                  "Пароль должен содержать минимум 8 символов."
                  )

            if not password2:
                  errors["password2"] = "Повторите пароль."

            elif password1 != password2:
                  errors["password2"] = "Пароли не совпадают."

            # =========================
            # ПРОВЕРКА DJANGO
            # =========================

            if (
                  password1
                  and password2
                  and password1 == password2
            ):
                  temp_user = User(
                  username=username,
                  email=email,
                  )

                  try:
                        validate_password(
                              password1,
                              user=temp_user
                        )

                  except ValidationError as error:
                        errors["password1"] = " ".join(
                              error.messages
                        )

            # =========================
            # СОГЛАСИЕ
            # =========================

            if not agreement:
                  errors["agreement"] = (
                  "Необходимо принять правила сайта."
                  )

            # =========================
            # ЕСЛИ ЕСТЬ ОШИБКИ
            # =========================

            if errors:
                  context = {
                  "errors": errors,
                  "form_data": {
                        "username": username,
                        "email": email,
                  }
                  }

                  return render(
                  request,
                  "registration/register.html",
                  context
                  )

            # =========================
            # СОЗДАНИЕ ПОЛЬЗОВАТЕЛЯ
            # =========================

            try:
                  with transaction.atomic():
                        user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password1,
                  )

            except IntegrityError:
                  messages.error(
                  request,
                  "Не удалось создать аккаунт. "
                  "Проверьте введённые данные."
                  )

                  return render(
                  request,
                  "registration/register.html",
                  {
                        "form_data": {
                              "username": username,
                              "email": email,
                        }
                  }
                  )

            login(request, user)

            messages.success(
                  request,
                  "Регистрация успешно завершена!"
            )

            return redirect("home")

      return render(
            request,
            "registration/register.html"
      )


@login_required
def profile_view(request):
      return render(request, "registration/profile.html")


def logout_view(request):
      logout(request)
      return redirect("home")


@login_required(login_url="registration:login")
def edit_profile_view(request):
      if request.method == "POST":
            form = EditProfileForm(
                  request.POST,
                  request.FILES,
                  instance=request.user,
            )

            if form.is_valid():
                  form.save()
            messages.success(request, "Профиль успешно обновлён.")
            return redirect("registration:profile")
      else:
            form = EditProfileForm(instance=request.user)

      return render(
            request,
            "registration/edit-profile.html",
            {"form": form},
      )
