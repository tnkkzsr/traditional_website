import os
import django
from django.core.management.base import BaseCommand
from render.models import Nakagawa

class Command(BaseCommand):
    help = 'Import Nakagawa data into the database'

    def handle(self, *args, **kwargs):
        # Djangoプロジェクトの設定モジュールを設定
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
        django.setup()

        # 既存のデータを削除
        Nakagawa.objects.all().delete()

        # データのリスト
        data = [
            {'Name': 'video0039', 'Image Path': 'mokkogei/export_20220318194022/', 'Correct Evaluation': 'A', 'Is Example': True},
            {'Name': 'video0014', 'Image Path': 'mokkogei/export_20220318200205/', 'Correct Evaluation': 'A', 'Is Example': True},
            {'Name': 'video0018', 'Image Path': 'mokkogei/export_20220318195900/', 'Correct Evaluation': 'A', 'Is Example': False},
            {'Name': 'video0024', 'Image Path': 'mokkogei/export_20220318195359/', 'Correct Evaluation': 'A', 'Is Example': False},
            {'Name': 'video0036', 'Image Path': 'mokkogei/export_20220318194316/', 'Correct Evaluation': 'A', 'Is Example': False},
            {'Name': 'video0037', 'Image Path': 'mokkogei/export_20220318194225/', 'Correct Evaluation': 'A', 'Is Example': False},
            {'Name': 'video001', 'Image Path': 'mokkogei/export_20220318201416/', 'Correct Evaluation': 'B', 'Is Example': True},
            {'Name': 'video002', 'Image Path': 'mokkogei/export_20220318201228/', 'Correct Evaluation': 'B', 'Is Example': True},
            {'Name': 'video0042', 'Image Path': 'mokkogei/export_20220318193513/', 'Correct Evaluation': 'B', 'Is Example': False},
            {'Name': 'video004', 'Image Path': 'mokkogei/export_20220318201058/', 'Correct Evaluation': 'B', 'Is Example': False},
            {'Name': 'video005', 'Image Path': 'mokkogei/export_20220318201009/', 'Correct Evaluation': 'B', 'Is Example': False},
            {'Name': 'video0043', 'Image Path': 'mokkogei/export_20220318193420/', 'Correct Evaluation': 'B', 'Is Example': False},
            {'Name': 'video0217', 'Image Path': 'mokkogei/export_20220316150449/', 'Correct Evaluation': 'C', 'Is Example': True},
            {'Name': 'video0150', 'Image Path': 'mokkogei/export_20220316135617/', 'Correct Evaluation': 'C', 'Is Example': True},
            {'Name': 'video0104', 'Image Path': 'mokkogei/export_20220316143000/', 'Correct Evaluation': 'C', 'Is Example': False},
            {'Name': 'video0060', 'Image Path': 'mokkogei/export_20220318191618/', 'Correct Evaluation': 'C', 'Is Example': False},
            {'Name': 'video0029', 'Image Path': 'mokkogei/export_20220318194929/', 'Correct Evaluation': 'C', 'Is Example': False},
            {'Name': 'video0272', 'Image Path': 'mokkogei/export_20220317093648/', 'Correct Evaluation': 'C', 'Is Example': False},
        ]

        # データを一括で挿入
        nakagawa_objects = [
            Nakagawa(
                name=item['Name'],
                image_path=item['Image Path'],
                correct_evaluation=item['Correct Evaluation'],
                is_example=item['Is Example']
            )
            for item in data
        ]

        Nakagawa.objects.bulk_create(nakagawa_objects)

        self.stdout.write(self.style.SUCCESS("データを一括で挿入しました。"))
