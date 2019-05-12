from weixin.models import *
from pay.models import *
import time
# 向订单表中写入数据
def writeToOrders(czId, czType, czMoney):
    try:
        OrdersInfo.objects.create(订单号=czId, 充值类型=czType, 充值金额=float(czMoney))
    except:
        return False

    return True
    #OrdersInfo.objects.create(订单号=czId, 充值类型=czType, 充值金额=float(czMoney))
    #return False

# 向订单学生信息表中写入数据
def writeToSOW(czId, czStuID):
    try:
        czid_object = OrdersInfo.objects.get(订单号=czId)
        name = StudentsInfo.objects.get(学号=czStuID)
        OrderSOWInfo.objects.create(订单号=czid_object, 学号=czStuID, 姓名=name.姓名)
    except:
        return False

    return True

# 向订单宿舍信息表中写入数据
def writeToDorm(czId, dromID):
    '''try:
        address = getAddress(dromID)
        czid_object = OrdersInfo.objects.get(订单号=czId)
        OrderDormInfo.objects.create(订单号=czid_object, 住址=address)
    except:
        return False'''
    address = getAddress(dromID)
    czid_object = OrdersInfo.objects.get(订单号=czId)
    OrderDormInfo.objects.create(订单号=czid_object, 住址=address)
    return True

# 更新支付状态
def updateStatus(czId, result):
    try:
        obj = OrdersInfo.objects.get(订单号=czId)
        obj.支付状态 = result
        obj.save()
    except:
        return False

    return True

# 更新学生金额
def updateSOW(czType, czStuID, czMoney):
    try:
        student = StudentsInfo.objects.get(学号=czStuID)
        obj = StudentsBalance.objects.get(学号=student)
        
        if czType == '学生卡充值':
            obj.卡上余额 = obj.卡上余额 + float(czMoney)
        else:
            obj.水费余额 = obj.水费余额 + float(czMoney)
        obj.上次充值时间 = getTime()
        obj.save()
    except:
        return False

    return True

# 更新寝室电费
def updateElec(dromID, czMoney):
    '''try:
        dromObj = DormsInfo.objects.get(住址编号 = dromID)
        dromObj.剩余电量 += float(czMoney)
        dromObj.上次充值时间 = getTime()
        dromObj.save()
    except:
        return False'''
    dromObj = DormsInfo.objects.get(住址编号 = dromID)
    dromObj.剩余电量 += float(czMoney)
    dromObj.上次充值时间 = getTime()
    dromObj.save()
    return True
ADDRESS = {
    'X1': '行建轩一栋',
    'X2': '行建轩二栋',
    'X3': '行建轩三栋',
    'X4': '行建轩四栋',
    'X5': '行建轩五栋',
    'X6': '行建轩六栋',
    'H1': '弘毅轩一栋',
    'H2': '弘毅轩二栋',
    'H3': '弘毅轩三栋',
    'H4': '弘毅轩四栋',
    'Z1': '致诚轩一栋',
    'Z2': '致诚轩二栋',
    'Z3': '致诚轩三栋',
    'Z4': '致诚轩四栋'
}
# 地址编号转地址
def getAddress(dromID):
    address = ADDRESS[ dromID[:2] ] + dromID[2] + '区' + dromID[3:] + '号'
    return address


# 获取当前时间
def getTime():
    Time = time.localtime()
    date = '%04d-%02d-%02d %02d:%02d'%(Time[0], Time[1], Time[2], Time[3], Time[4])
    return date
