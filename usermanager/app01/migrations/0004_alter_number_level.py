# Generated by Django 4.0.4 on 2022-05-04 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_alter_number_level_alter_number_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='number',
            name='level',
            field=models.SmallIntegerField(choices=[(3, '高'), (2, '中'), (1, '低')], verbose_name='级别'),
        ),
    ]