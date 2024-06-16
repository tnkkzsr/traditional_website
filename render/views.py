from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth import get_user_model
from .forms import UUIDForm
from .models import User,Asahiyaki,AsahiyakiEvaluation
import json
from django.http import JsonResponse
import random
from django.db.models import F


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
    
    # お手本の朝日焼を取得
    asahiyakis_example = Asahiyaki.objects.filter(is_example=True)
    #　お手本以外の朝日焼を取得
    asahiyakis_not_example = Asahiyaki.objects.filter(is_example=False).order_by('?')[:3] # ランダムな順序で取得
    
    # ユーザーが存在しない場合は新規作成
    if not User.objects.filter(uuid=uuid).exists():
        User.objects.create(uuid=uuid)
    user = User.objects.get(uuid=uuid)   
    
    if request.method == 'POST':
        data = json.loads(request.body)
        asahiyaki = Asahiyaki.objects.get(id=data['asahiyaki'])
        selected_image = data['selected_image']        
        evaluation = data['evaluation']
        akashiyaki_evaluation = AsahiyakiEvaluation.objects.filter(user=user, asahiyaki=asahiyaki,is_learned=False)
        # すでに評価が存在する場合は更新、存在しない場合は新規作成
        if akashiyaki_evaluation.exists():
            akashiyaki_evaluation.update(front_image_name=selected_image, evaluation=evaluation)
        else:
            evaluation = AsahiyakiEvaluation.objects.create(user=user, asahiyaki=asahiyaki, front_image_name=selected_image, evaluation=evaluation,is_learned=False)
        return JsonResponse({'status': 'success', 'message': 'データが正常に保存されました。'})

    
    
    numbers = list(range(1,25))
    context = {
        "numbers": numbers,
        "asahiyakis_example": asahiyakis_example,
        "asahiyakis_not_example": asahiyakis_not_example,
        "user": user,
    }
    return render(request, "render/asahiyaki.html", context)

def asahiyaki_learn(request):
    
    uuid = request.GET.get("uuid")
    
    if not uuid:
        return redirect("/")
    
    user = User.objects.get(uuid=uuid)   
    asahiyaki_samples_a = Asahiyaki.objects.filter(is_example=True, correct_evaluation='A')
    asahiyaki_samples_b = Asahiyaki.objects.filter(is_example=True, correct_evaluation='B')
    asahiyaki_samples_c = Asahiyaki.objects.filter(is_example=True, correct_evaluation='C')
    
    asahiyakis_not_example = Asahiyaki.objects.filter(is_example=False).order_by('?')[:3] # ランダムな順序で取得
    
    if request.method == 'POST':
        data = json.loads(request.body)
        asahiyaki = Asahiyaki.objects.get(id=data['asahiyaki'])
        selected_image = data['selected_image']        
        evaluation = data['evaluation']
        akashiyaki_evaluation = AsahiyakiEvaluation.objects.filter(user=user, asahiyaki=asahiyaki,is_learned=True)
        # すでに評価が存在する場合は更新、存在しない場合は新規作成
        if akashiyaki_evaluation.exists():
            akashiyaki_evaluation.update(front_image_name=selected_image, evaluation=evaluation)
        else:
            evaluation = AsahiyakiEvaluation.objects.create(user=user, asahiyaki=asahiyaki, front_image_name=selected_image, evaluation=evaluation,is_learned=True)
        return JsonResponse({'status': 'success', 'message': 'データが正常に保存されました。'})
    
    
    context = {
        "asahiyaki_samples_a": asahiyaki_samples_a,
        "asahiyaki_samples_b": asahiyaki_samples_b,
        "asahiyaki_samples_c": asahiyaki_samples_c,
        "asahiyakis_not_example": asahiyakis_not_example,
        "user": user,
    }
    return render(request, "render/asahiyaki_learn.html", context)

def mokkogei(request):
    numbers = list(range(1,25))
    context = {
        "numbers": numbers,
    }
    return render(request, "render/mokkogei.html", context)

