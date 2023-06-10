# Generated by Django 3.2 on 2023-05-31 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_remove_subscription_unique_user_author'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favorites',
            options={'ordering': ['id'], 'verbose_name': 'Избранный рецепт', 'verbose_name_plural': 'Избранные рецепты'},
        ),
        migrations.AddConstraint(
            model_name='subscription',
            constraint=models.UniqueConstraint(fields=('user', 'author'), name='unique_user_author'),
        ),
    ]