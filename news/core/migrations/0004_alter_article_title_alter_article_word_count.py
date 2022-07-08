# Generated by Django 4.0.5 on 2022-06-21 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_rename_headline_article'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='word_count',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
