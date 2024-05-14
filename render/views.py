from django.shortcuts import render
from django.contrib.auth import get_user_model


User = get_user_model()

def index(request):
    user = User.objects.get(username="aaaaaa")
    numbers = list(range(1,25))
    context = {
        "user": user,
        "numbers": numbers,
    }
    return render(request, "render/index.html", context)


