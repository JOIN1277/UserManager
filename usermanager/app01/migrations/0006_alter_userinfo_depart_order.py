# Generated by Django 4.0.4 on 2022-05-13 01:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0005_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='depart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.department', verbose_name='所属部门'),
        ),
        migrations.CreateModel(
            name='order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.CharField(max_length=64, verbose_name='订单号')),
                ('title', models.CharField(max_length=32, verbose_name='商品名称')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='价格')),
                ('status', models.SmallIntegerField(choices=[(0, '未支付'), (1, '已支付')], default=0, verbose_name='支付状态')),
                ('admin', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app01.admin', verbose_name='管理员')),
            ],
        ),
    ]