from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth import get_user_model
from .forms import UUIDForm
from .models import User,Asahiyaki




def index(request):
    if request.method == "POST":
        form = UUIDForm(request.POST)
        if form.is_valid():
            uuid = form.cleaned_data["uuid"]
            return redirect(f"/asahiyaki?uuid={uuid}")
    else:
        form = UUIDForm()
        
    context = {
        "form": form,
        
    }
    return render(request, "render/index.html",context)


def asahiyaki(request):
    uuid = request.GET.get("uuid")
    asahiyakis = Asahiyaki.objects.all()
    for asahiyaki in asahiyakis:
        print(asahiyaki.image_path)
    if not uuid:
        return redirect("/")
    user = User.objects.get_or_create(uuid=uuid, defaults={"username": f'User_{uuid}'})   
    numbers = list(range(1,25))
    context = {
        "numbers": numbers,
        "user": user,
        "asahiyakis": asahiyakis,
    }
    return render(request, "render/asahiyaki.html", context)

def mokkogei(request):
    numbers = list(range(1,25))
    context = {
        "numbers": numbers,
    }
    return render(request, "render/mokkogei.html", context)

