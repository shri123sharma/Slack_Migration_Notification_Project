# Generated by Django 4.2 on 2023-04-11 10:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slack_app', '0019_rename_country_country_model_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='category_last_update',
        ),
    ]
