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
    
    class Meta:
        abstract = True

    def __str__(self):
        return f"Evaluation by {self.user.username}"


    
class Asahiyaki(models.Model):
    """
    朝日焼のモデル
    """
    name = models.CharField(max_length=100)
    # 画像フォルダのパス
    image_path = models.CharField(max_length=255)
    
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

class Nakagawa(models.Model):
    """中川木工芸のモデル"""
    name = models.CharField(max_length=100)
    # 画像フォルダのパス
    image_path = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name


class NakagawaEvaluation(BaseEvaluation):
    """
    中川木工芸の評価モデル
    ・	ABC評価のみ
    """
    # Nakagawaモデルへの外部キー
    nakagawa = models.ForeignKey('Nakagawa', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{super().__str__()} - {self.nakagawa.name} - {self.evaluation}"
