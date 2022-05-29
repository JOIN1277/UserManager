# Generated by Django 4.0.4 on 2022-05-04 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='number',
            name='level',
            field=models.SmallIntegerField(choices=[(1, '高'), (2, '中'), (3, '低')], verbose_name='级别'),
        ),
        migrations.AlterField(
            model_name='number',
            name='status',
            field=models.SmallIntegerField(choices=[(1, '已占用'), (2, '未占用')], verbose_name='是否占用'),
        ),
    ]