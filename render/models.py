from django.db import models
import uuid

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
    
    session = models.ForeignKey('EvaluationSession', on_delete=models.CASCADE, null=True, blank=True)
    
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

class EvaluationSession(models.Model):
    """
    評価セッションを識別するためのモデル
    """
    session_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Session {self.session_id} for User {self.user.username} at {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
    

class AsahiyakiEvaluationResult(models.Model):
    session = models.ForeignKey(EvaluationSession, on_delete=models.CASCADE, related_name='evaluation_results')
    is_learned = models.BooleanField(default=False)  # 学習前はFalse、学習後はTrue
    accuracy = models.FloatField(default=0.0)
    f1_score = models.FloatField(default=0.0)
    qwk = models.FloatField(default=0.0)
    classification_report = models.JSONField()

    def __str__(self):
        learning_phase = "After Learning" if self.is_learned else "Before Learning"
        return f"{self.session.user.username} - {learning_phase} - Accuracy: {self.accuracy}, F1 Score: {self.f1_score}"
    
    