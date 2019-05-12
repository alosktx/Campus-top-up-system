from django.db import models

# Create your models here.
# 一张订单表, 两张充值信息表
class OrdersInfo(models.Model):
    订单号 = models.CharField(max_length=100, unique=True)
    充值类型 = models.CharField(max_length=20)
    充值金额 = models.FloatField()
    创建时间 = models.DateTimeField(auto_now_add=True)
    支付状态 = models.BooleanField(default=False)

    def __str__(self):
        return self.订单号

class OrderSOWInfo(models.Model):
    订单号 = models.ForeignKey(OrdersInfo, on_delete=models.CASCADE)
    学号 = models.CharField(max_length=15)
    姓名 = models.CharField(max_length=15)

class OrderDormInfo(models.Model):
    订单号 = models.ForeignKey(OrdersInfo, on_delete=models.CASCADE)
    住址 = models.TextField(null=False)
