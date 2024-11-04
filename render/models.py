from django.db import models
import uuid
from sklearn.metrics import f1_score, cohen_kappa_score, classification_report


# Create your models here.
class User(models.Model):
    """
    ユーザーを管理するためのモデル
    uuid: ユーザーを一意に識別するためのuuid
    username: ユーザー名
    """
    # ユーザーを一意に識別するためのuuid
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # ユーザー名
    username = models.CharField(max_length=100)
    
    def get_evaluation_results(self, evaluation_model, object_field_name, is_learned=False):
        """
        汎用評価結果取得メソッド
        - evaluation_model: 評価モデル（例: AsahiyakiEvaluation, MokkogeiEvaluation）
        - object_field_name: 評価対象フィールド名（例: 'asahiyaki', 'nakagawa'）
        - is_learned: 学習済みかどうかのフラグ
        """
        evaluations = evaluation_model.objects.filter(
            user=self, is_learned=is_learned
        ).exclude(evaluation="").order_by(f'{object_field_name}__id')
        
        results = []
        true_y = []
        pred_y = []
        
        for evaluation in evaluations:
            obj = getattr(evaluation, object_field_name)  # 'asahiyaki' や 'nakagawa' を取得
            true_y.append(obj.correct_evaluation)
            pred_y.append(evaluation.evaluation)
            is_correct = evaluation.evaluation == obj.correct_evaluation
            
            result = {
                'object_id': obj.id,
                'name': obj.name,
                'user_evaluation': evaluation.evaluation,
                'correct_evaluation': obj.correct_evaluation,
                'is_correct': is_correct,
                'image_path': obj.image_path
            }
            results.append(result)

        # 統計の計算
        accuracy = (sum([r['is_correct'] for r in results]) / len(results) * 100) if results else 0
        accuracy = round(accuracy, 2)
        f1 = f1_score(true_y, pred_y, average='weighted') if results else 0
        qwk = cohen_kappa_score(true_y, pred_y, weights='quadratic') if results else 0
        qwk = round(qwk, 4)
        report = classification_report(true_y, pred_y, output_dict=True)

        return {
            'results': results,
            'accuracy': accuracy,
            'f1': f1,
            'qwk': qwk,
            'report': report,
        }
        
    def get_front_image_difference_results(self, evaluation_model, is_learned=False):
        evaluations = evaluation_model.objects.filter(user=self, is_learned=is_learned).exclude(front_image_name="").order_by('asahiyaki__id')
        
        results = []
        total_difference = 0
        
        for evaluation in evaluations:
            obj = evaluation.asahiyaki if evaluation_model == AsahiyakiEvaluation else evaluation.nakagawa  # モデルに応じて切り替え
            difference = evaluation.calculate_image_difference()
            total_difference += difference
            results.append({
                'id': obj.id,
                'name': obj.name,
                'front_image_name': evaluation.front_image_name,
                'image_path': obj.image_path,
                'difference': difference,
            })
        
        avg_difference = total_difference / len(evaluations) if evaluations else 0
        return results, avg_difference
    
    def __str__(self):
        return str(self.uuid) + ":" + self.username
    
    
class BaseEvaluation(models.Model):
    """
    評価の共通部分を持つ抽象クラス
    """
    EVALUATION_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    ]
    
    # Userモデルへの外部キー
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    # ABC評価
    evaluation = models.CharField(max_length=1, choices=EVALUATION_CHOICES)
    # 作成日時
    created_at = models.DateTimeField(auto_now_add=True)
    # 更新日時
    updated_at = models.DateTimeField(auto_now=True)
    #　学習したかどうか
    is_learned = models.BooleanField(default=False)
    
    class Meta:
        abstract = True

    def __str__(self):
        return f"is_learned:{self.is_learned} {self.user.username}"


    
class Asahiyaki(models.Model):
    """
    朝日焼のモデル
    """
    name = models.CharField(max_length=100)
    # 画像フォルダのパス
    image_path = models.CharField(max_length=255)
    # 正解のABC評価
    correct_evaluation = models.CharField(max_length=1, choices=BaseEvaluation.EVALUATION_CHOICES,null=True, blank=True)
    # お手本かどうか
    is_example = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name+ "_"+self.image_path
    
    
    
    
class AsahiyakiEvaluation(BaseEvaluation):
    """
    朝日焼の評価モデル
    ・	ABC評価
    ・	選択した正面画像
    """
    # Asahiyakiモデルへの外部キー
    asahiyaki = models.ForeignKey('Asahiyaki', on_delete=models.CASCADE)
    # 正面と選択した画像の名前
    front_image_name = models.CharField(max_length=100)
    
    def __str__(self):
    
        return f"{super().__str__()} - {self.asahiyaki.name} - {self.evaluation}"
    
    def calculate_image_difference(self):
        image_number = int(self.front_image_name.split(".")[0])
        difference = abs(image_number - 1)
        return min(difference, 24 - difference)  # 最大のズレは12

class Nakagawa(models.Model):
    """中川木工芸のモデル"""
    name = models.CharField(max_length=100)
    # 画像フォルダのパス
    image_path = models.CharField(max_length=255)
    
    # 正解のABC評価
    correct_evaluation = models.CharField(max_length=1, choices=BaseEvaluation.EVALUATION_CHOICES,null=True, blank=True)
    
    is_example = models.BooleanField(default=False)
    def __str__(self):
        return self.correct_evaluation + "_" + str(self.is_example) + "_" + self.image_path


class NakagawaEvaluation(BaseEvaluation):
    """
    中川木工芸の評価モデル
    ・	ABC評価のみ
    """
    # Nakagawaモデルへの外部キー
    nakagawa = models.ForeignKey('Nakagawa', on_delete=models.CASCADE)
    
    
    
    def __str__(self):
        return f"{super().__str__()} - {self.nakagawa.name} - {self.evaluation}"




class EvaluationResult(models.Model):
    """
    計算された評価結果を保存するモデル
    """
    # ユーザーへの参照
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    # 評価セッションへの参照
    session = models.ForeignKey('EvaluationSession', on_delete=models.CASCADE, related_name='asahiyaki_evaluations')
    # 評価のタイプ（学習前、学習後など）
    evaluation_type = models.CharField(max_length=100, choices=[('before', 'Before Learning'), ('after', 'After Learning')])
    # AsahiyakiEvaluationsオブジェクトへの多対多参照
    asahiyaki_evaluations = models.ManyToManyField('AsahiyakiEvaluation', related_name='evaluation_results')
    # 計算日
    calculation_date = models.DateTimeField(auto_now_add=True)
    # 正確度
    accuracy = models.FloatField()
    # F1スコア
    f1_score = models.FloatField()
    # Quadratic Weighted Kappa
    qwk = models.FloatField()
    # 混同行列の画像URL
    confusion_matrix_image_url = models.URLField()
    # 分類レポート（JSON形式で保存することもできる）
    classification_report = models.JSONField()
    
    def __str__(self):
        return f"{self.user.username} - {self.evaluation_type} - {self.calculation_date.strftime('%Y-%m-%d')}"

class EvaluationSession(models.Model):
    """
    評価セッションを識別するためのモデル
    """
    session_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Session {self.session_id} for User {self.user.username} at {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
