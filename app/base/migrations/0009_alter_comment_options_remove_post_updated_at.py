# Generated by Django 4.1.7 on 2023-05-09 21:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-created_at']},
        ),
        migrations.RemoveField(
            model_name='post',
            name='updated_at',
        ),
    ]