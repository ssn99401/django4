# Generated by Django 2.2 on 2019-06-01 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('blog', '0001_initial'),
        ('customlogin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='u',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='customlogin.User'),
        ),
    ]
