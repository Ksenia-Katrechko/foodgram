# Generated by Django 4.2.14 on 2024-07-19 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(blank=True, help_text='Можете загрузить картинку', null=True, upload_to='media', verbose_name='картинка'),
        ),
    ]
