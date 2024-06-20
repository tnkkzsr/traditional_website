from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth import get_user_model
from .forms import UUIDForm
from .models import User,Asahiyaki,AsahiyakiEvaluation
import json
from django.http import JsonResponse
import random
from django.db.models import F

from django.db.models import Count



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
    # asahiyakis_not_example = Asahiyaki.objects.filter(is_example=False).order_by('?')[:12]
    # NOTE: 動作確認用に順序を固定
    asahiyakis_not_example = list(Asahiyaki.objects.filter(is_example=False).order_by('id')[:6] )
    random.shuffle(asahiyakis_not_example)
    
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
    
    # asahiyakis_not_example = Asahiyaki.objects.filter(is_example=False).order_by('?')[:3] # ランダムな順序で取得
    # NOTE: 動作確認用に個数を制限
    asahiyakis_not_example = list(Asahiyaki.objects.filter(is_example=False).order_by('id')[:6])
    random.shuffle(asahiyakis_not_example)
     
    
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
        "user_uuid": user.uuid,
    }
    return render(request, "render/asahiyaki_learn.html", context)

def mokkogei(request):
    numbers = list(range(1,25))
    context = {
        "numbers": numbers,
    }
    return render(request, "render/mokkogei.html", context)


from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import User, Asahiyaki, AsahiyakiEvaluation
import json


def evaluation_results(request, user_uuid):
    user = User.objects.get(uuid=user_uuid)
    
    evaluations_before_learning = AsahiyakiEvaluation.objects.filter(user=user, is_learned=False).order_by('asahiyaki__id')
    evaluations_after_learning = AsahiyakiEvaluation.objects.filter(user=user, is_learned=True).order_by('asahiyaki__id')
    
    results_before_learning = []
    results_after_learning = []
    
    correct_count_before = 0
    correct_count_after = 0

    def calculate_image_difference(front_image_name):
        image_number = int(front_image_name.split(".")[0])
        difference = abs(image_number - 1)
        return min(difference, 24 - difference)  # 最大のズレは12

    for evaluation in evaluations_before_learning:
        asahiyaki = evaluation.asahiyaki
        is_correct = evaluation.evaluation == asahiyaki.correct_evaluation
        if is_correct:
            correct_count_before += 1
        image_difference = calculate_image_difference(evaluation.front_image_name)
        result = {
            'asahiyaki_id': asahiyaki.id,
            'name': asahiyaki.name,
            'user_evaluation': evaluation.evaluation,
            'correct_evaluation': asahiyaki.correct_evaluation,
            'is_correct': is_correct,
            'front_image_name': evaluation.front_image_name,
            'image_difference': image_difference
        }
        results_before_learning.append(result)
       

    for evaluation in evaluations_after_learning:
        asahiyaki = evaluation.asahiyaki
        is_correct = evaluation.evaluation == asahiyaki.correct_evaluation
        if is_correct:
            correct_count_after += 1
        image_difference = calculate_image_difference(evaluation.front_image_name)
        result = {
            'asahiyaki_id': asahiyaki.id,
            'name': asahiyaki.name,
            'user_evaluation': evaluation.evaluation,
            'correct_evaluation': asahiyaki.correct_evaluation,
            'is_correct': is_correct,
            'front_image_name': evaluation.front_image_name,
            'image_difference': image_difference
        }
        results_after_learning.append(result)
        
    total_before = len(results_before_learning)
    total_after = len(results_after_learning)
    accuracy_before = (correct_count_before / total_before * 100) if total_before > 0 else 0
    accuracy_after = (correct_count_after / total_after * 100) if total_after > 0 else 0

    context = {
        'user': user,
        'results_before_learning': results_before_learning,
        'results_after_learning': results_after_learning,
        'accuracy_before': accuracy_before,
        'accuracy_after': accuracy_after,
       
    }

    return render(request, 'render/evaluation_results.html', context)