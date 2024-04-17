from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.shortcuts import render, redirect


def signup(request):
    if request.method == "GET":
        return render(request, "signup.html")

    elif request.method == "POST":
        form_data = {
            "username": request.POST.get("username"),
            "email": request.POST.get("email"),
            "password1": request.POST.get("password1"),
            "password2": request.POST.get("password2")
        }

        if User.objects.filter(username=form_data["username"]).exists():
            messages.add_message(
                request,
                constants.ERROR,
                "O nome de usuário já existe. Por favor, tente novamente!"
            )
            return redirect("signup")

        elif form_data['password1'] != form_data['password2']:
            messages.add_message(
                request,
                constants.ERROR,
                "As senhas não correspondem. Por favor, tente novamente!"
            )
            return redirect("signup")

        elif len(form_data['password1']) < 8:
            messages.add_message(
                request,
                constants.ERROR,
                "A senha deve ter pelo menos 8 caracteres. Por favor, tente novamente!"
            )
            return redirect("signup")

        else:
            try:
                user = User.objects.create_user(
                    form_data["username"],
                    form_data["email"],
                    form_data["password1"]
                )
                user.save()

                messages.add_message(
                    request,
                    constants.SUCCESS,
                    "O usuário foi criado com sucesso!"
                )

                return redirect("login")

            except Exception as e:
                messages.add_message(
                    request,
                    constants.ERROR,
                    f"Erro ao criar usuário: {str(e)}"
                )

                return redirect("signup")


def login(request):
    if request.method == "GET":
        return render(request, "login.html")

    elif request.method == "POST":
        form_data = {
            "username": request.POST.get("username"),
            "password": request.POST.get("password")
        }

        user = auth.authenticate(
            request,
            username=form_data["username"],
            password=form_data["password"]
        )

        if user:
            auth.login(request, user)

            messages.add_message(
                request,
                constants.SUCCESS,
                "Login realizado com sucesso!"
            )

            return redirect("home")

        else:
            messages.add_message(
                request,
                constants.ERROR,
                "Credenciais inválidas. Por favor, tente novamente!"
            )

            return redirect("login")
