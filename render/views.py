from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth import get_user_model
from .forms import UUIDForm
from .models import User




def index(request):
    if request.method == "POST":
        form = UUIDForm(request.POST)
        if form.is_valid():
            uuid = form.cleaned_data["uuid"]
            return redirect("asahiyaki",uuid)
    else:
        form = UUIDForm()
        
    context = {
        "form": form,
        
    }
    return render(request, "render/index.html",context)


def asahiyaki(request,uuid):
    user = get_object_or_404(User, uuid=uuid)   
    numbers = list(range(1,25))
    context = {
        "numbers": numbers,
        "user": user,
    }
    return render(request, "render/asahiyaki.html", context)

def mokkogei(request):
    numbers = list(range(1,25))
    context = {
        "numbers": numbers,
    }
    return render(request, "render/mokkogei.html", context)

