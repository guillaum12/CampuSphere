# Generated by Django 4.0.3 on 2022-08-21 12:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_alter_post_liked'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='value',
        ),
    ]
