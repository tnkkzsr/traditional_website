# Generated by Django 4.2 on 2024-06-16 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('render', '0004_asahiyaki_correct_evaluation'),
    ]

    operations = [
        migrations.AddField(
            model_name='asahiyaki',
            name='is_example',
            field=models.BooleanField(default=False),
        ),
    ]
