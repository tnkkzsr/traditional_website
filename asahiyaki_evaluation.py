import numpy as np
from sklearn.metrics import cohen_kappa_score
from django.db.models import Q
from render.models import Asahiyaki, AsahiyakiEvaluation, User

# スコアの割り当て
score_map = {'A': 3, 'B': 2, 'C': 1}

# 対象とするUUIDのリスト
user_uuids = [
    "ff297395-8464-43ad-9f82-ee254846b641",
    "e21a9995-f150-4611-9b16-828f8a2b2508",
    "9b6b15d7-8992-4a55-8a89-ed4bbf7acea5",
    "8ce7108b-3b52-4ddc-928c-7da6e98fe9a3",
    "46996c8f-172d-4ad6-934d-ea9ddff08af7",
    "456cf555-3185-4ca3-a358-4697db754064",
    "18934fb1-68c1-41c7-b2b7-6f2dd3eea57c",
    "0ba46038-2903-4f6e-8c67-eb2b1b9166f9",
    "14bcc8ea-31ce-430e-930f-e7654e622fa5",
    "fe7c78c6-3045-4105-8d07-5df14624b61a",
]

# 対象のユーザーをフィルタリング
users = User.objects.filter(uuid__in=user_uuids)

# Asahiyakiごとに評価を集計して表示
for asahiyaki in Asahiyaki.objects.filter(is_example=False)[:18]:
    print(f"Image Path: {asahiyaki.image_path}")
    print(f"正解の評価: {asahiyaki.correct_evaluation}")
    
    true_labels_before = []
    pred_labels_before = []
    true_labels_after = []
    pred_labels_after = []
    
    # is_learnedがFalseのもの
    unlearned_evaluations = AsahiyakiEvaluation.objects.filter(user__in=users, asahiyaki=asahiyaki, is_learned=False)
    if unlearned_evaluations.exists():
        print("  学習前の評価 (is_learned=False):")
        print(" ".join([evaluation.evaluation for evaluation in unlearned_evaluations]))
        unlearned_scores = [score_map[evaluation.evaluation] for evaluation in unlearned_evaluations]
        unlearned_average = sum(unlearned_scores) / len(unlearned_scores)
        unlearned_std = np.std(unlearned_scores, ddof=1)  # 標準偏差の計算
        
        # 正答率の計算
        correct_count_before = sum(1 for evaluation in unlearned_evaluations if evaluation.evaluation == asahiyaki.correct_evaluation)
        accuracy_before = correct_count_before / len(unlearned_evaluations) * 100
        
        print(f"学習前の平均得点: {unlearned_average:.2f}")
        print(f"学習前の標準偏差: {unlearned_std:.2f}")
        print(f"学習前の正答率: {accuracy_before:.2f}%")
        
        # QWKのために正解と予測をリストに追加
        true_labels_before = [asahiyaki.correct_evaluation] * len(unlearned_evaluations)
        pred_labels_before = [evaluation.evaluation for evaluation in unlearned_evaluations]
        
    # is_learnedがTrueのもの
    learned_evaluations = AsahiyakiEvaluation.objects.filter(user__in=users, asahiyaki=asahiyaki, is_learned=True)
    if learned_evaluations.exists():
        print("  学習後 (is_learned=True):")
        print(" ".join([evaluation.evaluation for evaluation in learned_evaluations]))
        learned_scores = [score_map[evaluation.evaluation] for evaluation in learned_evaluations]
        learned_average = sum(learned_scores) / len(learned_scores)
        learned_std = np.std(learned_scores, ddof=1)  # 標準偏差の計算
        
        # 正答率の計算
        correct_count_after = sum(1 for evaluation in learned_evaluations if evaluation.evaluation == asahiyaki.correct_evaluation)
        accuracy_after = correct_count_after / len(learned_evaluations) * 100
        
        print(f"学習後の平均得点: {learned_average:.2f}")
        print(f"学習後の標準偏差: {learned_std:.2f}")
        print(f"学習後の正答率: {accuracy_after:.2f}%")
        
        # QWKのために正解と予測をリストに追加
        true_labels_after = [asahiyaki.correct_evaluation] * len(learned_evaluations)
        pred_labels_after = [evaluation.evaluation for evaluation in learned_evaluations]
    
    # QWKの計算と表示
    if true_labels_before and pred_labels_before:
        qwk_before = cohen_kappa_score(true_labels_before, pred_labels_before, weights='quadratic')
        print(f"学習前のQWK: {qwk_before:.2f}")
        
    if true_labels_after and pred_labels_after:
        qwk_after = cohen_kappa_score(true_labels_after, pred_labels_after, weights='quadratic')
        print(f"学習後のQWK: {qwk_after:.2f}")
    
    print()  # 改行で区切る
