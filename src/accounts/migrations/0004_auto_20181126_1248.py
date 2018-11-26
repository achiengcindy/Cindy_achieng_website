# Generated by Django 2.1.3 on 2018-11-26 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20181120_1142'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='city',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='customuser',
            name='postal_code',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='address',
            field=models.CharField(default='', max_length=250),
        ),
    ]