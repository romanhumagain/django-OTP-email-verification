from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from MyApp.models import *
from MyApp.utils import *
import uuid


def emailVerification(request):
    if request.method == "POST":
        data = request.POST

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        token = str(uuid.uuid4())

        user = User.objects.create(username=username, email=email)
        user.set_password(password)

        profile = Profile.objects.create(user=user, email_token=str(uuid.uuid4()))

        sendEmailToken(email, profile.email_token)

    return render(request, "index.html")


def verify(request, token):
    try:
        profile = Profile.objects.get(email_token=token)
        profile.is_verified = True
        profile.save()

        return HttpResponse("your account successfully verified")

    except Exception as e:
        return HttpResponse("sorry ! your account couldnt registered")
