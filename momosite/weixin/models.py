from django.db import models

# Create your models here.
class DormsInfo(models.Model):
    住址编号 = models.CharField(max_length=15, unique=True)
    住址 = models.TextField(null=False)
    剩余电量 = models.FloatField(null=False)
    上次充值时间 = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.住址
    
class StudentsInfo(models.Model):
    GENDER_CHOICES = (
        (u'男', u'男'),
        (u'女', u'女')
    )
    学号 = models.CharField(max_length=15, unique=True)
    姓名 = models.CharField(max_length=15, null=False)
    性别 = models.CharField(max_length=2, choices=GENDER_CHOICES)
    住址编号 = models.ForeignKey(DormsInfo, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.学号
class StudentsBalance(models.Model):
    学号 = models.OneToOneField(StudentsInfo, on_delete=models.DO_NOTHING)
    #学号 = models.CharField(max_length=15, unique=True)
    卡上余额 = models.FloatField(null=False)
    水费余额 = models.FloatField(null=False)
    上次充值时间 = models.DateTimeField(auto_now_add=True)
    
class Questions(models.Model):
    联系人 = models.CharField(max_length=15)
    联系方式 = models.CharField(max_length=100, null=False)
    问题 = models.TextField(null=False)
    提交时间 = models.DateTimeField(auto_now_add=True)
    是否解决 = models.BooleanField(default=False)


