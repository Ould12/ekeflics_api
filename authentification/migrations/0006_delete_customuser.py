# Generated by Django 5.1 on 2024-09-09 00:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0005_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
