# Generated by Django 4.0.4 on 2022-05-18 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0008_boss_alter_order_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='城市')),
                ('count', models.IntegerField(verbose_name='人口')),
                ('img', models.FileField(max_length=128, upload_to='city/', verbose_name='logo')),
            ],
        ),
    ]
