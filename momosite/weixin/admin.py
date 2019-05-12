from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(StudentsInfo)
class StudentsInfoAdmin(admin.ModelAdmin):
    list_display = ("id", "学号", "姓名", "性别")
    ordering = ("id",)
    search_fields =('学号', '姓名') #搜索字段
@admin.register(StudentsBalance)
class StudentsBalanceAdmin(admin.ModelAdmin):
    list_display = ("id", "学号", "卡上余额", "水费余额", "上次充值时间")
    ordering = ("id",)
    search_fields =(('学号',)) #搜索字段
    
@admin.register(DormsInfo)
class DormsInfoAdmin(admin.ModelAdmin):
    list_display = ("id", "住址", "剩余电量", "上次充值时间")
    ordering = ("id", )
    search_fields =(('住址',)) #搜索字段
    
@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ("id", "联系人", "问题", "提交时间", "是否解决")
    ordering = ("id",)
    search_fields =(('联系人',)) #搜索字段
    
    
