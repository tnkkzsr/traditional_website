# load_initial_data.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from render.models import Asahiyaki

# 初期データの挿入
asahiyaki1 = Asahiyaki(name="Asahiyaki 1", image_path="/path/to/image1")
asahiyaki1.save()

asahiyaki2 = Asahiyaki(name="Asahiyaki 2", image_path="/path/to/image2")
asahiyaki2.save()

asahiyaki3 = Asahiyaki(name="Asahiyaki 3", image_path="/path/to/image3")
asahiyaki3.save()
