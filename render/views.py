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
    
    user = get_object_or_404(User, uuid=uuid)
    asahiyakis = Asahiyaki.objects.filter(is_example=False)[:3]
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            asahiyaki = Asahiyaki.objects.get(id=data['asahiyaki'])
            evaluation = data['evaluation']
            asahiyaki_evaluation = AsahiyakiEvaluation.objects.filter(user=user, asahiyaki=asahiyaki, is_learned=False)
            
            if asahiyaki_evaluation.exists():
                asahiyaki_evaluation.update(evaluation=evaluation)
            else:
                AsahiyakiEvaluation.objects.create(user=user, asahiyaki=asahiyaki, evaluation=evaluation, is_learned=False)
            
            return JsonResponse({'status': 'success', 'message': 'データが正常に保存されました。'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    context = {
        "asahiyakis": asahiyakis,
        "user": user,
    }
    return render(request, "render/asahiyaki.html", context)


def asahiyaki_learn(request):
    uuid = request.GET.get("uuid")
    
    if not uuid:
        return redirect("/")
    
    user = get_object_or_404(User, uuid=uuid)
    asahiyaki_samples_a = Asahiyaki.objects.filter(is_example=True, correct_evaluation='A')
    asahiyaki_samples_b = Asahiyaki.objects.filter(is_example=True, correct_evaluation='B')
    asahiyaki_samples_c = Asahiyaki.objects.filter(is_example=True, correct_evaluation='C')
    
    asahiyakis_not_example = Asahiyaki.objects.filter(is_example=False).order_by('id')[:3] 
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            asahiyaki = Asahiyaki.objects.get(id=data['asahiyaki'])
            evaluation = data['evaluation']
            asahiyaki_evaluation = AsahiyakiEvaluation.objects.filter(user=user, asahiyaki=asahiyaki, is_learned=True)
            
            if asahiyaki_evaluation.exists():
                asahiyaki_evaluation.update(evaluation=evaluation)
            else:
                AsahiyakiEvaluation.objects.create(user=user, asahiyaki=asahiyaki, evaluation=evaluation, is_learned=True)
            
            return JsonResponse({'status': 'success', 'message': 'データが正常に保存されました。'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
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


from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import User, Asahiyaki, AsahiyakiEvaluation
import json




from django.shortcuts import render, get_object_or_404
from .models import User, Asahiyaki, AsahiyakiEvaluation
from sklearn.metrics import f1_score, cohen_kappa_score, confusion_matrix, classification_report
import json
import os
from django.conf import settings
import matplotlib.pyplot as plt
import numpy as np

def save_confusion_matrix_image(cm, labels, title, filename):
    plt.figure(figsize=(8, 6))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(labels))
    plt.xticks(tick_marks, labels)
    plt.yticks(tick_marks, labels)
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

    image_path = os.path.join(settings.MEDIA_ROOT, filename)
    plt.savefig(image_path)
    
    return os.path.join(settings.MEDIA_URL, filename)

def evaluation_results(request, user_uuid):
    user = get_object_or_404(User, uuid=user_uuid)
    
    evaluations_before_learning = AsahiyakiEvaluation.objects.filter(user=user, is_learned=False).order_by('asahiyaki__id')
    evaluations_after_learning = AsahiyakiEvaluation.objects.filter(user=user, is_learned=True).order_by('asahiyaki__id')
    
    results_before_learning = []
    results_after_learning = []
    
    true_y_before = []
    pred_y_before = []
    true_y_after = []
    pred_y_after = []
    
    def calculate_image_difference(front_image_name):
        if not front_image_name:
            return 0  # もしくは他の適切なデフォルト値
        image_number = int(front_image_name.split(".")[0])
        difference = abs(image_number - 1)
        return min(difference, 24 - difference)  # 最大のズレは12

    for evaluation in evaluations_before_learning:
        asahiyaki = evaluation.asahiyaki
        true_y_before.append(asahiyaki.correct_evaluation)
        pred_y_before.append(evaluation.evaluation)
        is_correct = evaluation.evaluation == asahiyaki.correct_evaluation
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
        true_y_after.append(asahiyaki.correct_evaluation)
        pred_y_after.append(evaluation.evaluation)
        is_correct = evaluation.evaluation == asahiyaki.correct_evaluation
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
    
    # 学習前の評価
    accuracy_before = (sum([r['is_correct'] for r in results_before_learning]) / len(results_before_learning) * 100) if results_before_learning else 0
    f1_before = f1_score(true_y_before, pred_y_before, average='weighted') if results_before_learning else 0
    qwk_before = cohen_kappa_score(true_y_before, pred_y_before, weights='quadratic') if results_before_learning else 0
    cm_before = confusion_matrix(true_y_before, pred_y_before, labels=["A", "B", "C"]).tolist()
    report_before = classification_report(true_y_before, pred_y_before, output_dict=True)
    cm_before_image_url = save_confusion_matrix_image(cm_before, ["A", "B", "C"], "学習前の混同行列", f"cm_before_{user.uuid}.png")

    # 学習後の評価
    accuracy_after = (sum([r['is_correct'] for r in results_after_learning]) / len(results_after_learning) * 100) if results_after_learning else 0
    f1_after = f1_score(true_y_after, pred_y_after, average='weighted') if results_after_learning else 0
    qwk_after = cohen_kappa_score(true_y_after, pred_y_after, weights='quadratic') if results_after_learning else 0
    cm_after = confusion_matrix(true_y_after, pred_y_after, labels=["A", "B", "C"]).tolist()
    report_after = classification_report(true_y_after, pred_y_after, output_dict=True)
    cm_after_image_url = save_confusion_matrix_image(cm_after, ["A", "B", "C"], "学習後の混同行列", f"cm_after_{user.uuid}.png")

    context = {
        'user': user,
        'results_before_learning': results_before_learning,
        'results_after_learning': results_after_learning,
        'accuracy_before': accuracy_before,
        'accuracy_after': accuracy_after,
        'f1_before': f1_before,
        'f1_after': f1_after,
        'qwk_before': qwk_before,
        'qwk_after': qwk_after,
        'cm_before': cm_before,
        'cm_after': cm_after,
        'cm_before_image_url': cm_before_image_url,
        'cm_after_image_url': cm_after_image_url,
        'report_before': report_before,
        'report_after': report_after,
    }

    return render(request, 'render/evaluation_results.html', context)


def asahiyaki_select_front(request):
    uuid = request.GET.get("uuid")
    
    if not uuid:
        return redirect("/")
    
    user = get_object_or_404(User, uuid=uuid)
    asahiyakis_a = Asahiyaki.objects.filter(correct_evaluation='A', is_example=False)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            asahiyaki = Asahiyaki.objects.get(id=data['asahiyaki'])
            selected_image = data['selected_image']
            
            asahiyaki_evaluation = AsahiyakiEvaluation.objects.filter(user=user, asahiyaki=asahiyaki, is_learned=False)
            
            if asahiyaki_evaluation.exists():
                asahiyaki_evaluation.update(front_image_name=selected_image,)
            else:
                AsahiyakiEvaluation.objects.create(user=user, asahiyaki=asahiyaki, front_image_name=selected_image, evaluation=evaluation, is_learned=True)
            return JsonResponse({'status': 'success', 'message': 'データが正常に保存されました。'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    context = {
        "asahiyakis_a": asahiyakis_a,
        "user": user,
    }
    return render(request, "render/asahiyaki_select_front.html", context)


def asahiyaki_front_select_learn(request):
    uuid = request.GET.get("uuid")
    
    if not uuid:
        return redirect("/")
    
    user = get_object_or_404(User, uuid=uuid)
    asahiyaki_samples_a = Asahiyaki.objects.filter(is_example=True, correct_evaluation='A')
    asahiyaki_samples_b = Asahiyaki.objects.filter(is_example=True, correct_evaluation='B')
    asahiyaki_samples_c = Asahiyaki.objects.filter(is_example=True, correct_evaluation='C')
    
    asahiyakis_not_example = Asahiyaki.objects.filter(is_example=False).order_by('id')[:3] 
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            asahiyaki = Asahiyaki.objects.get(id=data['asahiyaki'])
            selected_image = data['selected_image']
            asahiyaki_evaluation = AsahiyakiEvaluation.objects.filter(user=user, asahiyaki=asahiyaki, is_learned=True)
            
            if asahiyaki_evaluation.exists():
                asahiyaki_evaluation.update(front_image_name=selected_image)
            else:
                AsahiyakiEvaluation.objects.create(user=user, asahiyaki=asahiyaki, front_image_name=selected_image, is_learned=True)
            return JsonResponse({'status': 'success', 'message': 'データが正常に保存されました。'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    context = {
        "asahiyaki_samples_a": asahiyaki_samples_a,
        "asahiyaki_samples_b": asahiyaki_samples_b,
        "asahiyaki_samples_c": asahiyaki_samples_c,
        "asahiyakis_not_example": asahiyakis_not_example,
        "user": user,
        "user_uuid": user.uuid,
    }
    return render(request, "render/asahiyaki_front_select_learn.html", context)