# Generated by Django 3.1.6 on 2021-06-22 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_image',
            field=models.ImageField(upload_to='images'),
        ),
    ]