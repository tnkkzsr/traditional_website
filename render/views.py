from django.shortcuts import render
from django.contrib.auth import get_user_model


User = get_user_model()

def index(request):
    
    return render(request, "render/index.html")


def asahiyaki(request):
    user = User.objects.get(username="aaaaaa")
    numbers = list(range(1,25))
    context = {
        "user": user,
        "numbers": numbers,
    }
    return render(request, "render/asahiyaki.html", context)

def mokkogei(request):
    user = User.objects.get(username="aaaaaa")
    numbers = list(range(1,25))
    context = {
        "user": user,
        "numbers": numbers,
    }
    return render(request, "render/mokkogei.html", context)