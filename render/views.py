from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Count, F
from sklearn.metrics import f1_score, cohen_kappa_score, confusion_matrix, classification_report
import json
import random
import os
import matplotlib.pyplot as plt
import numpy as np
from .forms import UUIDForm
from .models import User, Asahiyaki, AsahiyakiEvaluation, Nakagawa, NakagawaEvaluation


def index(request):
    
    uuid = request.GET.get("uuid")
    if not uuid:
        return redirect("/login")
    
    return render(request, "render/index.html",{ "uuid": uuid})

def login(request):
    if request.method == "POST":
        form = UUIDForm(request.POST)
        if form.is_valid():
            uuid = form.cleaned_data["uuid"]
            return redirect(f"{reverse('index')}?uuid={uuid}")
    else:
        form = UUIDForm()
        
    return render(request, "render/login.html", {"form": form})

def asahiyaki(request):
    uuid = request.GET.get("uuid")
    if not uuid:
        return redirect("/")
    
    user = User.objects.filter(uuid=uuid)
    if not user.exists():
        user = User.objects.create(uuid=uuid)
    else:
        user = user.first()
    
        
    # asahiyakis = Asahiyaki.objects.filter(is_example=False)[:12]
    asahiyakis = list(Asahiyaki.objects.filter(is_example=False).order_by('id')[:12])
    random.shuffle(asahiyakis)
    
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)  # デバッグ出力
            asahiyaki = Asahiyaki.objects.get(id=data['asahiyaki'])
            evaluation = data['evaluation']
            asahiyaki_evaluation = AsahiyakiEvaluation.objects.filter(user=user, asahiyaki=asahiyaki, is_learned=False)
            
            if asahiyaki_evaluation.exists():
                asahiyaki_evaluation.update(evaluation=evaluation)
            else:
                AsahiyakiEvaluation.objects.create(user=user, asahiyaki=asahiyaki, evaluation=evaluation, is_learned=False)
            
            return JsonResponse({'status': 'success', 'message': 'データが正常に保存されました。'})
        except Exception as e:
            print(f"Exception: {e}")  # 例外の詳細を出力
            import traceback
            traceback.print_exc()  # スタックトレースを出力
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
    
    # asahiyaki_examples = Asahiyaki.objects.filter(is_example=True)
    asahiyaki_examples_a = Asahiyaki.objects.filter(correct_evaluation='A',is_example=True).order_by('id')[:2]
    asahiyaki_examples_b = Asahiyaki.objects.filter(correct_evaluation='B',is_example=True).order_by('id')[:2]
    asahiyaki_examples_c = Asahiyaki.objects.filter(correct_evaluation='C',is_example=True).order_by('id')[:2]
    
    asahiyakis_not_example = list(Asahiyaki.objects.filter(is_example=False).order_by('id')[:12])
    random.shuffle(asahiyakis_not_example)
    
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
        # "asahiyaki_examples": asahiyaki_examples,
        "asahiyakis_not_example": asahiyakis_not_example,
        "user": user,
        "asahiyaki_examples_a": asahiyaki_examples_a,
        "asahiyaki_examples_b": asahiyaki_examples_b,
        "asahiyaki_examples_c": asahiyaki_examples_c,
    }
    return render(request, "render/asahiyaki_learn.html", context)


def evaluation_results(request):
    uuid = request.GET.get("uuid")
    if not uuid:
        return redirect("/")
    
    user = get_object_or_404(User, uuid=uuid)
    
    # 学習前の評価をフィルタリング
    evaluations_before_learning = AsahiyakiEvaluation.objects.filter(
        user=user, is_learned=False
    ).exclude(evaluation="").order_by('asahiyaki__id')

    # 学習後の評価をフィルタリング
    evaluations_after_learning = AsahiyakiEvaluation.objects.filter(
        user=user, is_learned=True
    ).exclude(evaluation="").order_by('asahiyaki__id')

    
    results_before_learning = []
    results_after_learning = []
    
    true_y_before = []
    pred_y_before = []
    true_y_after = []
    pred_y_after = []
    
    

    for evaluation in evaluations_before_learning:
        asahiyaki = evaluation.asahiyaki
        true_y_before.append(asahiyaki.correct_evaluation)
        pred_y_before.append(evaluation.evaluation)
        is_correct = evaluation.evaluation == asahiyaki.correct_evaluation
        
        result = {
            'asahiyaki_id': asahiyaki.id,
            'name': asahiyaki.name,
            'user_evaluation': evaluation.evaluation,
            'correct_evaluation': asahiyaki.correct_evaluation,
            'is_correct': is_correct,
            'front_image_name': evaluation.front_image_name,
            "image_path": asahiyaki.image_path
        }
        results_before_learning.append(result)

    for evaluation in evaluations_after_learning:
        asahiyaki = evaluation.asahiyaki
        true_y_after.append(asahiyaki.correct_evaluation)
        pred_y_after.append(evaluation.evaluation)
        is_correct = evaluation.evaluation == asahiyaki.correct_evaluation
        
        result = {
            'asahiyaki_id': asahiyaki.id,
            'name': asahiyaki.name,
            'user_evaluation': evaluation.evaluation,
            'correct_evaluation': asahiyaki.correct_evaluation,
            'is_correct': is_correct,
            'front_image_name': evaluation.front_image_name,
            "image_path": asahiyaki.image_path
        }
        results_after_learning.append(result)
    
    # 学習前の評価
    accuracy_before = (sum([r['is_correct'] for r in results_before_learning]) / len(results_before_learning) * 100) if results_before_learning else 0
    accuracy_before = round(accuracy_before, 2)
    f1_before = f1_score(true_y_before, pred_y_before, average='weighted') if results_before_learning else 0
    qwk_before = cohen_kappa_score(true_y_before, pred_y_before, weights='quadratic') if results_before_learning else 0
    qwk_before_rounded = round(qwk_before, 4)
    report_before = classification_report(true_y_before, pred_y_before, output_dict=True)

    # 学習後の評価
    accuracy_after = (sum([r['is_correct'] for r in results_after_learning]) / len(results_after_learning) * 100) if results_after_learning else 0
    accuracy_after = round(accuracy_after, 2)
    f1_after = f1_score(true_y_after, pred_y_after, average='weighted') if results_after_learning else 0
    qwk_after = cohen_kappa_score(true_y_after, pred_y_after, weights='quadratic') if results_after_learning else 0
    qwk_after_rounded = round(qwk_after, 4)
    report_after = classification_report(true_y_after, pred_y_after, output_dict=True)

    context = {
        'user': user,
        'results_before_learning': results_before_learning,
        'results_after_learning': results_after_learning,
        'accuracy_before': accuracy_before,
        'accuracy_after': accuracy_after,
        'f1_before': f1_before,
        'f1_after': f1_after,
        'qwk_before': qwk_before_rounded,
        'qwk_after': qwk_after_rounded,
        'report_before': report_before,
        'report_after': report_after,
    }

    return render(request, 'render/evaluation_results.html', context)


def random_image_list():
    """
    画像名のリストの最初の要素をランダムに選択し、その位置からリストを再構成する
    """
      # 画像リストの作成
    images = [f"{str(i).zfill(2)}.png" for i in range(1, 25)]

    # ランダムな開始位置を決定
    start_index = random.randint(0, len(images) - 1)

    # リストを再構成
    reordered_images = images[start_index:] + images[:start_index]
    return reordered_images

def asahiyaki_select_front(request):
    uuid = request.GET.get("uuid")
    
    if not uuid:
        return redirect("/")
    
    
    user = get_object_or_404(User, uuid=uuid)
    
    
    asahiyakis_a = list(Asahiyaki.objects.filter(correct_evaluation='A', is_example=False)[:12])
    random.shuffle(asahiyakis_a)
    
    reordered_images = random_image_list()

    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            asahiyaki = Asahiyaki.objects.get(id=data['asahiyaki'])
            selected_image = data['selected_image']
            
            asahiyaki_evaluation = AsahiyakiEvaluation.objects.filter(user=user, asahiyaki=asahiyaki, is_learned=False)
            
            if asahiyaki_evaluation.exists():
                asahiyaki_evaluation.update(front_image_name=selected_image,)
            else:
                AsahiyakiEvaluation.objects.create(user=user, asahiyaki=asahiyaki, front_image_name=selected_image, is_learned=False)
            return JsonResponse({'status': 'success', 'message': 'データが正常に保存されました。'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    context = {
        "asahiyakis_a": asahiyakis_a,
        "user": user,
        'reordered_images': reordered_images,
    }
    return render(request, "render/asahiyaki_select_front.html", context)

def asahiyaki_front_select_learn(request):
    uuid = request.GET.get("uuid")
    
    if not uuid:
        return redirect("/")
    
    user = get_object_or_404(User, uuid=uuid)
    asahiyaki_examples_a = Asahiyaki.objects.filter(is_example=True,correct_evaluation='A')
    
    asahiyakis_a = list(Asahiyaki.objects.filter(correct_evaluation='A', is_example=False)[:12])
    random.shuffle(asahiyakis_a)

    reordered_images = random_image_list()

    
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
        "asahiyaki_examples_a": asahiyaki_examples_a,
        "asahiyakis_not_example": asahiyakis_a,
        "user": user,
        "user_uuid": user.uuid,
        "reordered_images": reordered_images,
    }
    return render(request, "render/asahiyaki_front_select_learn.html", context)

def asahiyaki_front_select_result(request):
    """
    AsahiyakiEvaluationからfront_image_nameを取得し、正面画像との差分を計算して表示する
    各朝日焼きに対して、正面画像との差分を計算してテーブル形式で表示する。
    
    AsahiyakiEvaluationのメソッドを呼び出す。
    """
    uuid = request.GET.get("uuid")
    if not uuid:
        return redirect("/")

    user = get_object_or_404(User, uuid=uuid)
    
    evaluations_before_learning = AsahiyakiEvaluation.objects.filter(user=user, is_learned=False).exclude(front_image_name="").order_by('asahiyaki__id')
    evaluations_after_learning = AsahiyakiEvaluation.objects.filter(user=user, is_learned=True).exclude(front_image_name="").order_by('asahiyaki__id')
    
    results_before_learning = []
    results_after_learning = []

    total_difference_before = 0
    total_difference_after = 0

    for evaluation in evaluations_before_learning:
        asahiyaki = evaluation.asahiyaki
        difference = evaluation.calculate_image_difference()
        total_difference_before += difference
        result = {
            'asahiyaki_id': asahiyaki.id,
            'name': asahiyaki.name,
            'front_image_name': evaluation.front_image_name,
            'image_path': asahiyaki.image_path,
            'difference': difference,
        }
        results_before_learning.append(result)
    
    for evaluation in evaluations_after_learning:
        asahiyaki = evaluation.asahiyaki
        difference = evaluation.calculate_image_difference()
        total_difference_after += difference
        result = {
            'asahiyaki_id': asahiyaki.id,
            'name': asahiyaki.name,
            'front_image_name': evaluation.front_image_name,
            'image_path': asahiyaki.image_path,
            'difference': difference,
        }
        results_after_learning.append(result)

    # 平均値を計算
    avg_difference_before = total_difference_before / len(evaluations_before_learning) if evaluations_before_learning else 0
    avg_difference_after = total_difference_after / len(evaluations_after_learning) if evaluations_after_learning else 0

    context = {
        'user': user,
        'results_before_learning': results_before_learning,
        'results_after_learning': results_after_learning,
        'avg_difference_before': avg_difference_before,
        'avg_difference_after': avg_difference_after,
    }   
    
    return render(request, 'render/asahiyaki_front_image_result.html', context)


def mokkogei(request):
    uuid = request.GET.get("uuid")
    if not uuid:
        return redirect("/")

    user = User.objects.filter(uuid=uuid)
    if not user.exists():
        user = User.objects.create(uuid=uuid)
    else:
        user = user.first()

    mokkogeis = list(Nakagawa.objects.filter(is_example=False).order_by('id')[:12])
    random.shuffle(mokkogeis)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            nakagawa = Nakagawa.objects.get(id=data['mokkogei'])
            evaluation = data['evaluation']
            nakagawa_evaluation = NakagawaEvaluation.objects.filter(user=user, nakagawa=nakagawa, is_learned=False)

            if nakagawa_evaluation.exists():
                nakagawa_evaluation.update(evaluation=evaluation)
            else:
                NakagawaEvaluation.objects.create(user=user, nakagawa=nakagawa, evaluation=evaluation, is_learned=False)

            return JsonResponse({'status': 'success', 'message': 'データが正常に保存されました。'})
        except Exception as e:
            print(f"Exception: {e}")  # 例外の詳細を出力
            import traceback
            traceback.print_exc()  # スタックトレースを出力
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    context = {
        "mokkogeis": mokkogeis,
        "user": user,
    }
    return render(request, "render/mokkogei.html", context)

def mokkogei_learn(request):
    uuid = request.GET.get("uuid")
    
    if not uuid:
        return redirect("/")
    
    user = get_object_or_404(User, uuid=uuid)
    
    mokkogei_examples = Nakagawa.objects.filter(is_example=True)
    
    mokkogei_not_example = list(Nakagawa.objects.filter(is_example=False).order_by('id')[:12] )
    random.shuffle(mokkogei_not_example)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            mokkogei = Nakagawa.objects.get(id=data['mokkogei'])
            evaluation = data['evaluation']
            mokkogei_evaluation = NakagawaEvaluation.objects.filter(user=user, nakagawa=mokkogei, is_learned=True)
            if mokkogei_evaluation.exists():
                mokkogei_evaluation.update(evaluation=evaluation)
                
            else:
                NakagawaEvaluation.objects.create(user=user, nakagawa=mokkogei, evaluation=evaluation, is_learned=True)
            
            return JsonResponse({'status': 'success', 'message': 'データが正常に保存されました。'})
        except Exception as e:
            print(f"Exception: {e}")  # 例外の詳細を出力
            import traceback
            traceback.print_exc()  # スタックトレースを出力
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    context = {
        "mokkogei_examples": mokkogei_examples,
        "mokkogei_not_example": mokkogei_not_example,
        "user": user,
    }
    return render(request, "render/mokkogei_learn.html", context)

def mokkogei_result(request):
    uuid = request.GET.get("uuid")
    if not uuid:
        return redirect("/")
    
    user = get_object_or_404(User, uuid=uuid)

    evaluations_before_learning = NakagawaEvaluation.objects.filter(user=user, is_learned=False).order_by('nakagawa__id')
    evaluations_after_learning = NakagawaEvaluation.objects.filter(user=user, is_learned=True).order_by('nakagawa__id')
    
    results_before_learning = []
    results_after_learning = []
    
    true_y_before = []
    pred_y_before = []
    true_y_after = []
    pred_y_after = []
    
    

    for evaluation in evaluations_before_learning:
        nakagawa = evaluation.nakagawa
        true_y_before.append(nakagawa.correct_evaluation)
        pred_y_before.append(evaluation.evaluation)
        is_correct = evaluation.evaluation == nakagawa.correct_evaluation
        
        result = {
            'nakagawa_id': nakagawa.id,
            'name': nakagawa.name,
            'user_evaluation': evaluation.evaluation,
            'correct_evaluation': nakagawa.correct_evaluation,
            'is_correct': is_correct,
            'image_path': nakagawa.image_path
            
        }
        results_before_learning.append(result)

    for evaluation in evaluations_after_learning:
        nakagawa = evaluation.nakagawa
        true_y_after.append(nakagawa.correct_evaluation)
        pred_y_after.append(evaluation.evaluation)
        is_correct = evaluation.evaluation == nakagawa.correct_evaluation
        
        result = {
            'nakagawa_id': nakagawa.id,
            'name': nakagawa.name,
            'user_evaluation': evaluation.evaluation,
            'correct_evaluation': nakagawa.correct_evaluation,
            'is_correct': is_correct,
            'image_path': nakagawa.image_path
            
        }
        results_after_learning.append(result)
    
    # 学習前の評価
    accuracy_before = (sum([r['is_correct'] for r in results_before_learning]) / len(results_before_learning) * 100) if results_before_learning else 0
    accuracy_before = round(accuracy_before, 2)
    f1_before = f1_score(true_y_before, pred_y_before, average='weighted') if results_before_learning else 0
    qwk_before = cohen_kappa_score(true_y_before, pred_y_before, weights='quadratic') if results_before_learning else 0
    qwk_before = round(qwk_before, 4)
    report_before = classification_report(true_y_before, pred_y_before, output_dict=True)
    

    # 学習後の評価
    accuracy_after = (sum([r['is_correct'] for r in results_after_learning]) / len(results_after_learning) * 100) if results_after_learning else 0
    accuracy_after = round(accuracy_after, 2)
    f1_after = f1_score(true_y_after, pred_y_after, average='weighted') if results_after_learning else 0
    qwk_after = cohen_kappa_score(true_y_after, pred_y_after, weights='quadratic') if results_after_learning else 0
    qwk_after = round(qwk_after, 4)
    report_after = classification_report(true_y_after, pred_y_after, output_dict=True)
    

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
        'report_before': report_before,
        'report_after': report_after,
    }

    return render(request, 'render/mokkogei_result.html', context)
