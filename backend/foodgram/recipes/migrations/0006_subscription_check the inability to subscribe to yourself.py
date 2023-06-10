# Generated by Django 3.2 on 2023-06-04 16:25

import django.db.models.expressions
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_auto_20230531_2232'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='subscription',
            constraint=models.CheckConstraint(check=models.Q(_negated=True, author=django.db.models.expressions.F('user')), name='Check the inability to subscribe to yourself'),
        ),
    ]