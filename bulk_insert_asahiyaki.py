import os
import django

# Djangoプロジェクトの設定モジュールを設定
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from render.models import Asahiyaki
Asahiyaki.objects.all().delete()

# データのリスト
data = [
    {'ID': 1, 'Name': 'A', 'Image Path': 'asahiyaki/export_20220223173209/', 'Correct Evaluation': 'A'},
    {'ID': 2, 'Name': 'A', 'Image Path': 'asahiyaki/export_20220223173553/', 'Correct Evaluation': 'A'},
    {'ID': 3, 'Name': 'A', 'Image Path': 'asahiyaki/export_20220223174624/', 'Correct Evaluation': 'A'},
    {'ID': 4, 'Name': 'A見本１', 'Image Path': 'asahiyaki/export_20220507171554/', 'Correct Evaluation': 'A'},
    {'ID': 5, 'Name': 'A見本2', 'Image Path': 'asahiyaki/export_20230922134139/', 'Correct Evaluation': 'A'},
    {'ID': 6, 'Name': 'A', 'Image Path': 'asahiyaki/export_20220507160946/', 'Correct Evaluation': 'A'},
    {'ID': 7, 'Name': 'B見本１', 'Image Path': 'asahiyaki/export_20220507162726/', 'Correct Evaluation': 'B'},
    {'ID': 8, 'Name': 'B見本2', 'Image Path': 'asahiyaki/export_20220507162923/', 'Correct Evaluation': 'B'},
    {'ID': 9, 'Name': 'B', 'Image Path': 'asahiyaki/export_20220223175214/', 'Correct Evaluation': 'B'},
    {'ID': 10, 'Name': 'B', 'Image Path': 'asahiyaki/export_20220507161217/', 'Correct Evaluation': 'B'},
    {'ID': 11, 'Name': 'B', 'Image Path': 'asahiyaki/export_20220507161451/', 'Correct Evaluation': 'B'},
    {'ID': 12, 'Name': 'B', 'Image Path': 'asahiyaki/export_20220507161921/', 'Correct Evaluation': 'B'},
    {'ID': 14, 'Name': 'C見本２', 'Image Path': 'asahiyaki/export_20220914143514/', 'Correct Evaluation': 'C'},
    {'ID': 13, 'Name': 'C見本', 'Image Path': 'asahiyaki/export_20220914144058/', 'Correct Evaluation': 'C'},
    {'ID': 15, 'Name': 'C', 'Image Path': 'asahiyaki/export_20220914104359/', 'Correct Evaluation': 'C'},
    {'ID': 18, 'Name': 'C', 'Image Path': 'asahiyaki/export_20220914135509/', 'Correct Evaluation': 'C'},
    {'ID': 17, 'Name': 'C', 'Image Path': 'asahiyaki/export_20220914134013/', 'Correct Evaluation': 'C'},
    {'ID': 16, 'Name': 'C', 'Image Path': 'asahiyaki/export_20220914101558/', 'Correct Evaluation': 'C'},
    {'ID': 19, 'Name': 'A見本3', 'Image Path': 'asahiyaki/export_20220507161704/', 'Correct Evaluation': 'A'},
    {'ID': 20, 'Name': 'A見本4', 'Image Path': 'asahiyaki/export_20220507170746/', 'Correct Evaluation': 'A'},
]

# データを一括で挿入
asahiyaki_objects = [
    Asahiyaki(id=item['ID'], name=item['Name'], image_path=item['Image Path'], correct_evaluation=item['Correct Evaluation'])
    for item in data
]

Asahiyaki.objects.bulk_create(asahiyaki_objects)

print("データを一括で挿入しました。")
