# Generated by Django 3.2.16 on 2025-01-11 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_post_group'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-pub_date']},
        ),
    ]
