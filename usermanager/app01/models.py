from django.db import models

# Create your models here.
class Department(models.Model):
     #部门表
    title = models.CharField(verbose_name="标题",max_length=32)

    def __str__(self):
        return self.title

class UserInfo(models.Model):
    #员工表
    name = models.CharField(verbose_name="姓名",max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额", max_digits=10,decimal_places=2,default=0)
    create_time = models.DateTimeField(verbose_name="创建时间")
    gender_choices = ((1,"男"),(2,"女"))
    gender = models.SmallIntegerField(verbose_name="性别",choices=gender_choices)
    #1.有约束的字段 ,与Department中的id关联
    #depart = models.ForeignKey(to="Department",to_field=id)
    #2.django自动生成
    #  - depart
    #  - 数据库表中生成depart_id
    #3.部门表被删除
    #3.1-级联删除
    depart = models.ForeignKey(verbose_name="所属部门",to="Department",to_field="id", on_delete=models.CASCADE)
    #3.2-置空 表的该字段可以为空，表单可以传空，
    #depart = models.ForeignKey(to="Department",null=True,blank=True, to_field="id", on_delete=models.SET_NULL)

class Number(models.Model):
    mobile = models.CharField(verbose_name="手机",max_length=11)
    price = models.DecimalField(verbose_name="价格",max_digits=10,decimal_places=2,default=0)
    level_choices = ((3,"高"),(2,"中"),(1,"低"))
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices)
    status_choices = ((1,"已占用"),(2,"未占用"))
    status = models.SmallIntegerField(verbose_name="是否占用",choices=status_choices)

class admin(models.Model):
    username = models.CharField(max_length=32, verbose_name="用户名")
    password = models.CharField(verbose_name="密码",max_length=64)
    def __str__(self):
        return self.username

class order(models.Model):
    num = models.CharField(verbose_name="订单号",max_length=64)
    title = models.CharField(verbose_name="商品名称",max_length=32)
    price = models.DecimalField(verbose_name="价格",max_digits=10,decimal_places=2,default=0)

    status_choices = (
        (0,"未支付"),
        (1,"已支付")
    )
    status = models.SmallIntegerField(verbose_name="支付状态",choices=status_choices,default=0)
    admin = models.ForeignKey(verbose_name="管理员",to="admin",on_delete=models.SET_NULL,null=True)


class Boss(models.Model):
    name = models.CharField(verbose_name="姓名",max_length=32)
    age = models.IntegerField(verbose_name="年龄")
    img = models.CharField(verbose_name="头像",max_length=128)


class City(models.Model):
    name = models.CharField(verbose_name="城市",max_length=64)
    count = models.IntegerField(verbose_name="人口")
    img = models.FileField(verbose_name="logo",max_length=128,upload_to="city/")