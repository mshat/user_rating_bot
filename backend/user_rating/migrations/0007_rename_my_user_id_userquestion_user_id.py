# Generated by Django 4.0.3 on 2022-04-05 22:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_rating', '0006_rename_user_id_useranswer_my_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userquestion',
            old_name='my_user_id',
            new_name='user_id',
        ),
    ]
