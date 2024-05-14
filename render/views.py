from django.shortcuts import render
from django.contrib.auth import get_user_model


User = get_user_model()

def index(request):
    user = User.objects.get(username="aaaaaa")
    return render(request, "render/index.html", {"user":user})
