# Generated by Django 4.0.3 on 2022-04-05 22:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_rating', '0007_rename_my_user_id_userquestion_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useranswer',
            old_name='my_user_id',
            new_name='user_id',
        ),
    ]
