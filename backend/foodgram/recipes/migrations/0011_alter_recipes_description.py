# Generated by Django 3.2 on 2023-06-08 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0010_alter_recipes_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipes',
            name='description',
            field=models.TextField(verbose_name='Описание рецепта'),
        ),
    ]
