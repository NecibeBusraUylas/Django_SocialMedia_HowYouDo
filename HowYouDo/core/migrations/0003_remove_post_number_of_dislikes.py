# Generated by Django 4.1.3 on 2022-11-14 13:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_post_alter_profile_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='number_of_dislikes',
        ),
    ]