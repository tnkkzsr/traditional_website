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
    
    user = User.objects.filter(uuid=uuid).first()
    
    
    context = {}
    context["uuid"] = uuid
    context["user"] = user
    if AsahiyakiEvaluation.objects.filter(user=user).exists():
        # AsahiyakiEvaluationの学習前後のABC評価
        asahiyaki_evaluations_before = user.get_evaluation_results(AsahiyakiEvaluation, 'asahiyaki', is_learned=False)
        asahiyaki_evaluations_after = user.get_evaluation_results(AsahiyakiEvaluation, 'asahiyaki', is_learned=True)

        # NakagawaEvaluationの学習前後のABC評価
        nakagawa_evaluations_before = user.get_evaluation_results(NakagawaEvaluation, 'nakagawa', is_learned=False)
        nakagawa_evaluations_after = user.get_evaluation_results(NakagawaEvaluation, 'nakagawa', is_learned=True)
        
        # AsahiyakiEvaluationの学習前後の正面画像評価
        front_results_asahiyaki_before, avg_difference_asahiyaki_before = user.get_front_image_difference_results(AsahiyakiEvaluation, is_learned=False)
        front_results_asahiyaki_after, avg_difference_asahiyaki_after = user.get_front_image_difference_results(AsahiyakiEvaluation, is_learned=True)

        context["asahiyaki_ABC_before_acuuracy"] = asahiyaki_evaluations_before['accuracy']
        context["asahiyaki_ABC_before_qwk"] = asahiyaki_evaluations_before['qwk']
        context["asahiyaki_ABC_after_acuuracy"] = asahiyaki_evaluations_after['accuracy']
        context["asahiyaki_ABC_after_qwk"] = asahiyaki_evaluations_after['qwk']
        context["nakagawa_ABC_before_acuuracy"] = nakagawa_evaluations_before['accuracy']
        context["nakagawa_ABC_before_qwk"] = nakagawa_evaluations_before['qwk']
        context["nakagawa_ABC_after_acuuracy"] = nakagawa_evaluations_after['accuracy']
        context["nakagawa_ABC_after_qwk"] = nakagawa_evaluations_after['qwk']
        context["front_results_asahiyaki_before"] = front_results_asahiyaki_before
        context["front_results_asahiyaki_after"] = front_results_asahiyaki_after
        context["avg_difference_asahiyaki_before"] = avg_difference_asahiyaki_before
        context["avg_difference_asahiyaki_after"] = avg_difference_asahiyaki_after
    
    return render(request, "render/index.html", context)



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


def asahiyaki_results(request):
    uuid = request.GET.get("uuid")
    if not uuid:
        return redirect("/")
    
    user = get_object_or_404(User, uuid=uuid)
    
    results_before = user.get_evaluation_results(AsahiyakiEvaluation, 'asahiyaki', is_learned=False)
    results_after = user.get_evaluation_results(AsahiyakiEvaluation, 'asahiyaki', is_learned=True)

    context = {
        'user': user,
        'results_before_learning': results_before['results'],
        'results_after_learning': results_after['results'],
        'accuracy_before': results_before['accuracy'],
        'accuracy_after': results_after['accuracy'],
        'f1_before': results_before['f1'],
        'f1_after': results_after['f1'],
        'qwk_before': results_before['qwk'],
        'qwk_after': results_after['qwk'],
        'report_before': results_before['report'],
        'report_after': results_after['report'],
    }

    return render(request, 'render/asahiyaki_results.html', context)

def mokkogei_results(request):
    uuid = request.GET.get("uuid")
    if not uuid:
        return redirect("/")
    
    user = get_object_or_404(User, uuid=uuid)

    results_before = user.get_evaluation_results(NakagawaEvaluation, 'nakagawa', is_learned=False)
    results_after = user.get_evaluation_results(NakagawaEvaluation, 'nakagawa', is_learned=True)
    
    context = {
        'user': user,
        'results_before_learning': results_before['results'],
        'results_after_learning': results_after['results'],
        'accuracy_before': results_before['accuracy'],
        'accuracy_after': results_after['accuracy'],
        'f1_before': results_before['f1'],
        'f1_after': results_after['f1'],
        'qwk_before': results_before['qwk'],
        'qwk_after': results_after['qwk'],
        'report_before': results_before['report'],
        'report_after': results_after['report'],
    }

    return render(request, 'render/mokkogei_results.html', context)




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
    
    results_before, avg_difference_before = user.get_front_image_difference_results(AsahiyakiEvaluation, is_learned=False)
    results_after, avg_difference_after = user.get_front_image_difference_results(AsahiyakiEvaluation, is_learned=True)

    context = {
        'user': user,
        'results_before_learning': results_before,
        'results_after_learning': results_after,
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

    reorderd_images = random_image_list()

    context = {
        "mokkogeis": mokkogeis,
        "user": user,
        'reordered_images': reorderd_images,
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
    
    reorderd_images = random_image_list()
    
    context = {
        "mokkogei_examples": mokkogei_examples,
        "mokkogei_not_example": mokkogei_not_example,
        "user": user,
        "reordered_images": reorderd_images,
    }
    return render(request, "render/mokkogei_learn.html", context)

