# Generated by Django 4.0.5 on 2022-06-20 15:00

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_headline_channel'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Headline',
            new_name='Article',
        ),
    ]