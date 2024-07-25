from sklearn.metrics import f1_score, cohen_kappa_score, classification_report
from .models import User, Asahiyaki, AsahiyakiEvaluation, Nakagawa, NakagawaEvaluation, EvaluationSession, BaseEvaluation,AsahiyakiEvaluationResult


def calculate_and_save_evaluation_results(session, is_learned):
    evaluations = AsahiyakiEvaluation.objects.filter(session=session, is_learned=is_learned).exclude(evaluation="")

    true_y = [eval.asahiyaki.correct_evaluation for eval in evaluations]
    pred_y = [eval.evaluation for eval in evaluations]

    accuracy = sum(1 for true, pred in zip(true_y, pred_y) if true == pred) / len(evaluations) * 100 if evaluations else 0
    f1 = f1_score(true_y, pred_y, average='weighted') if evaluations else 0
    qwk = cohen_kappa_score(true_y, pred_y, weights='quadratic') if evaluations else 0
    report = classification_report(true_y, pred_y, output_dict=True) if evaluations else {}

    # Create or update the result
    result, created = AsahiyakiEvaluationResult.objects.update_or_create(
        session=session,
        is_learned=is_learned,
        defaults={
            'accuracy': accuracy,
            'f1_score': f1,
            'qwk': qwk,
            'classification_report': report
        }
    )
    return result
