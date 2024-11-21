from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from .models import Contact
from .token import token
from email.message import EmailMessage
import ssl
import smtplib


def index(request):
    if request.user.is_authenticated:
        return render(request, "home.html")
    else:
        return redirect("/login")


@login_required
def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        contact = Contact(name=name, email=email, phone=phone, message=message)
        contact.save()
        messages.success(request, "Your message has been sent")
    return render(request, "contact.html")


@csrf_exempt
def signup(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')

        if User.objects.filter(username=username).exists():
            messages.success(request, "Username is taken")
            return redirect("/signup")

        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name,
                                        last_name=last_name)
        login(request, user)
        messages.success(request, "Account Created")
        return redirect("/login")

    return render(request, "signup.html")


@csrf_exempt
def loginuser(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"{username} logged in")
            return redirect("/")

        try:
            User.objects.get(username=username)
            messages.success(request, "Incorrect password")
        except ObjectDoesNotExist:
            messages.success(request, "Username not found")

    return render(request, "Login.html")


@csrf_exempt
def forgot(request):
    if request.method == "POST":
        username = request.POST.get('username')

        try:
            user = User.objects.get(username=username)
            email_sender = "malhotraarnav70@gmail.com"
            email_password = "sdor dkpk iigf gwha"
            email_reciever = user.email
            subject = "Forgot password link"
            body = f"{user.username}, click here to reset your password: http://127.0.0.1:8000/forgotpass/{token}"
            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_reciever
            em['Subject'] = subject
            em.set_content(body)

            context = ssl.create_default_context()

            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_reciever, em.as_string())
                messages.success(request, f"Email sent to {email_reciever}")
        except ObjectDoesNotExist:
            messages.success(request, f"No user found with username: {username}")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

    return render(request, "forgot.html")


@login_required
def deleteuser(request):
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, f"User({user.username}) has been deleted")

    return render(request, "deleteuser.html")


@csrf_exempt
def forgotpass(request):
    if request.method == "POST":
        username = request.POST.get('username')
        new_pass = request.POST.get('new_pass')

        try:
            user = User.objects.get(username=username)
            user.set_password(new_pass)
            user.save()
            messages.success(request, f"Password changed for {username}")
            return redirect("/reset")
        except ObjectDoesNotExist:
            messages.success(request, f"No user found with username: {username}")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

    return render(request, "forgotpass.html")


@csrf_exempt
def resetpass(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get("oldpass")
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        user = authenticate(username=username, password=password)

        if user is not None and pass1 == pass2:
            user.set_password(pass1)
            user.save()
            messages.success(request, f"Password changed for {username}")
            return redirect("/reset")

    return render(request, "resetpass.html")


@login_required
def loguserout(request):
    logout(request)
    return render(request, "Logout.html")


def reset(request):
    return render(request, "reset.html")


@login_required
def changemail(request):
    if request.method == "POST":
        username = request.POST.get('username')
        oldpass = request.POST.get("oldpass")
        newmail = request.POST.get("newmail")
        user = authenticate(username=username, password=oldpass)

        if user is not None:
            user.email = newmail
            user.save()
            messages.success(request, "Email address updated successfully")
            return redirect("/account")

    return render(request, "changemail.html")


@login_required
def account(request):
    user = request.user
    email = user.email
    firstname = user.first_name
    lastname = user.last_name
    info = {"username": user.username, "email": email, "firstname": firstname, "lastname": lastname}

    return render(request, "account.html", info)
