# Generated by Django 5.1.7 on 2025-05-13 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_category_country_remove_user_groups_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
