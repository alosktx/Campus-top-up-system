from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(OrdersInfo)
class OrdersInfoAdmin(admin.ModelAdmin):
    list_display = ("订单号","充值类型", "充值金额","创建时间", "支付状态")
    ordering = ("创建时间",)
    search_fields = ("订单号", "充值类型", "充值金额")

@admin.register(OrderSOWInfo)
class OrderSOWInfoAdmin(admin.ModelAdmin):
    list_display = ("id", "订单号", "学号", "姓名")
    ordering = ("id",)
    search_fields = ("订单号", "学号", "姓名")


@admin.register(OrderDormInfo)
class OrderDormInfoAdmin(admin.ModelAdmin):
    list_display = ("id", "订单号", "住址")
    ordering = ("id", )
    search_fields = ("订单号", "住址")
