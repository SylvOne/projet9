# Generated by Django 4.2.1 on 2023-05-22 14:08

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_post_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
    ]
