# Generated by Django 4.0.3 on 2022-04-05 10:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_rating', '0003_alter_useranswer_answer'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TgUser',
            new_name='MyUser',
        ),
    ]