from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth import get_user_model
from .forms import UUIDForm
from .models import User,Asahiyaki,AsahiyakiEvaluation
import json
from django.http import JsonResponse


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
    
    if not uuid:
        return redirect("/")
    
    asahiyakis = Asahiyaki.objects.all()
    # ユーザーが存在しない場合は新規作成
    if not User.objects.filter(uuid=uuid).exists():
        User.objects.create(uuid=uuid)
    user = User.objects.get(uuid=uuid)   
    
    if request.method == 'POST':
        data = json.loads(request.body)
        asahiyaki = Asahiyaki.objects.get(id=data['asahiyaki'])
        selected_image = data['selected_image']        
        evaluation = data['evaluation']
        akashiyaki_evaluation = AsahiyakiEvaluation.objects.filter(user=user, asahiyaki=asahiyaki)
        # すでに評価が存在する場合は更新、存在しない場合は新規作成
        if akashiyaki_evaluation.exists():
            akashiyaki_evaluation.update(front_image_name=selected_image, evaluation=evaluation)
        else:
            evaluation = AsahiyakiEvaluation.objects.create(user=user, asahiyaki=asahiyaki, front_image_name=selected_image, evaluation="A")
        return JsonResponse({'status': 'success', 'message': 'データが正常に保存されました。'})

    
    
    numbers = list(range(1,25))
    context = {
        "numbers": numbers,
        "asahiyakis": asahiyakis,
        "user": user,
    }
    return render(request, "render/asahiyaki.html", context)

def mokkogei(request):
    numbers = list(range(1,25))
    context = {
        "numbers": numbers,
    }
    return render(request, "render/mokkogei.html", context)

