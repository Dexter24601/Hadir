# Generated by Django 4.1.4 on 2022-12-20 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HadirApp', '0002_user_reg_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='img',
            field=models.ImageField(default='', upload_to=''),
        ),
    ]