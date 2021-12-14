# Generated by Django 4.0 on 2021-12-14 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exambase', '0004_remove_question_question_image_path'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='option',
            options={},
        ),
        migrations.AlterUniqueTogether(
            name='option',
            unique_together={('question', 'option')},
        ),
        migrations.AlterField(
            model_name='option',
            name='option',
            field=models.CharField(max_length=1, verbose_name='Choice'),
        ),
        migrations.RemoveField(
            model_name='option',
            name='position',
        ),
    ]
