# Generated by Django 4.0 on 2022-02-19 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exambase', '0007_alter_exam_year_alter_option_option'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exam',
            old_name='paper',
            new_name='paper_name',
        ),
        migrations.AddField(
            model_name='exam',
            name='paper_num',
            field=models.IntegerField(null=True),
        ),
    ]
