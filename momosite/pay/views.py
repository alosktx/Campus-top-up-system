from django.shortcuts import render, redirect, HttpResponse, Http404
from django.template.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from alipay import AliPay

from weixin.models import *
from .func.optData import *
import urllib.parse
import time
import re
# 充值类型选择页面
def selectType(request):
    # 如果有POST的值传来
    if request.method == 'POST':
        # 获取充值类型
        select = request.POST.get('select')
        
        # html传参对象, csrf格式化是用于处理cookie问题
        context = csrf(request)
        Dict = dict()
        # 生成一个数值，用于做充值的订单号, 用时间来生成
        order_num = str(int(time.time()))
        
        if select == 'stuOrwater':
            order_num = 'sw'+ order_num
            Dict['order_num']= order_num
            context.update(Dict)
            return render(request, 'chongzhi1.html', context)
        else:
            order_num = 'df' + order_num
            Dict['order_num']= order_num
            context.update(Dict)
            return render(request, 'chongzhi2.html', context)
    else:
        return render(request, 'index.html')


#=========================支付系统=========================================
# 商户的私钥----------------正式修改处
app_private_key_string = open(r"/var/www/momosite/pay/keys/priKey.txt").read()
# 支付宝的公钥----------------正式测试修改处
alipay_public_key_string = open(r"/var/www/momosite/pay/keys/zifuKey.txt").read()

#app_private_key_string = open(r'D:\文档堆\文档\码源世界\代码练习\python\momosite\pay\keys\priKey.txt').read()
#alipay_public_key_string = open(r'D:\文档堆\文档\码源世界\代码练习\python\momosite\pay\keys\zifuKey.txt').read()

# 商户ID----------------正式修改处
APPID = "2016091900547320"

NOTIFY_URL = "http://47.107.187.170/pay/solve/"
RETURN_URL = "http://47.107.187.170/pay/get/"
# 异步回调地址
#NOTIFY_URL = "http://120.0.0.1:8000/"
# 同步回调地址
#RETURN_URL = "http://120.0.0.1:8000/pay/"

# 创建一个alipay对象
def create_alipay():
    alipay = AliPay(
        # 商户appid
        appid= APPID,
        app_notify_url= NOTIFY_URL,    # 默认回调url
        app_private_key_string=app_private_key_string,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",
        debug=True      # 沙盒测试使用True
    )

    return alipay

# 处理学生卡和水卡充值
def czStuOrWater(request):
    # 存放错误集合
    errors = []
    # html传参对象, csrf格式化是用于处理cookie问题
    context = csrf(request)
    # 初始化一个字典
    Dict = dict()
    
    if request.method == 'POST':
        # 获取post过来的表单数据
        # 充值类型
        cztype = request.POST.get('select')
        # 学号
        stuID = request.POST.get('id')
        # 姓名
        name = request.POST.get('name')
        # 充值金额
        money = request.POST.get('money')
        # 订单号
        order_num = request.POST.get('trade_no')

        # 存入查询网页的地址,这个用于error网页里，按钮点击返回查询网页
        Dict['window'] = '/pay/'

        # 所有值不能为空
        if not cztype or not stuID or not name or not money or not order_num:
            # 当有值为空时, 报错，跳转到报错页面
            errors.append("\t\t参数错误, 请重新输入")
            Dict['errors'] = errors
            context.update(Dict)
            return render(request, 'error.html', context)
        else:
            try:
                student = StudentsInfo.objects.get(学号=stuID, 姓名=name)
                balance = student.studentsbalance
            except ObjectDoesNotExist:
                errors.append("\t\t\t输入信息有误\n\t\t\t没该学生信息!!")
                Dict['errors'] = errors
                context.update(Dict)
                return render(request, 'error.html', context)
            except:
                errors.append("\t\t\t发生错误!!")
                Dict['errors'] = errors
                context.update(Dict)
                return render(request, 'error.html', context)
				
            subject = '水费充值'
            #czt = '1'
            if cztype == 'student':
                subject = '学生卡充值'
                #czt = '0'
            
            order_num = order_num+stuID
            # 获取支付授权url
            pay_url = pay(subject, order_num, money)
            return redirect(pay_url)
    else:
        # 如果没收到post，那么返回  网页404错误
        raise Http404("网页出问题了，请重试!!")


# 处理电费充值
def czElec(request):
    # 存放错误集合
    errors = []
    # html传参对象, csrf格式化是用于处理cookie问题
    context = csrf(request)
    # 初始化一个字典
    Dict = dict()
    
    if request.method == 'POST':
        # 获取post过来的表单数据
        # 寝室楼
        drom = request.POST.get('drom')
        # 寝室区
        apart = request.POST.get('apart')
        # 寝室号
        dromNum = request.POST.get('dromNumber')
        # 充值人学号
        stuID = request.POST.get('studentID')
        # 充值金额
        money = request.POST.get('money')
        # 订单号
        order_num = request.POST.get('trade_no')

        
        
        # 存入查询网页的地址,这个用于error网页里，按钮点击返回查询网页
        Dict['window'] = '/pay/'

        # 所有值不能为空
        if not dromNum and not money:
            # 当有值为空时, 报错，跳转到报错页面
            errors.append("\t\t参数错误, 请重新输入")
            Dict['errors'] = errors
            context.update(Dict)
            return render(request, 'error.html', context)
        else:
            # 合成寝室编号
            dromID = drom+apart+dromNum
            # 判断数据库中是否有这些数据，没有就告知错误
            try:
                # 查询是否有该寝室编号
                dormObj = DormsInfo.objects.get(住址编号=dromID)
                # 查询学号是否属于该寝室
                student = StudentsInfo.objects.get(学号=stuID)
                if student.住址编号.住址编号 != dromID:
                    errors.append("\t\t\t学生不属于该寝室")
                    Dict['errors'] = errors
                    context.update(Dict)
                    return render(request, 'error.html', context)
                
            except ObjectDoesNotExist:
                errors.append("\t\t\t输入信息有误\n\t\t  没该学生信息!!")
                Dict['errors'] = errors
                context.update(Dict)
                return render(request, 'error.html', context)
            except:
                errors.append("\t\t\t发生错误!!")
                Dict['errors'] = errors
                context.update(Dict)
                return render(request, 'error.html', context)
				
            subject = '电费充值'
            order_num = dromID+order_num+stuID
            
            # 获取支付授权url
            pay_url = pay(subject, order_num, money)
            return redirect(pay_url)
    else:
        # 如果没收到post，那么返回  网页404错误
        raise Http404("网页出问题了，请重试!!")




# 支付函数，进入支付宝支付
def pay(subject, out_trade_no, total_amount):
    # 创建alipay对象
    alipay = create_alipay()
    # 构建订单信息
    order_string = alipay.api_alipay_trade_wap_pay(
        out_trade_no = out_trade_no,
        total_amount = total_amount,
        subject = subject,
        notify_url= NOTIFY_URL,
        return_url = RETURN_URL
    )
    # 这个是沙盒测试----------------正式使用修改处
    pay_url = "https://openapi.alipaydev.com/gateway.do?" + order_string
    return pay_url





#============================================================================

# 异步回调
@csrf_exempt
def solve(request):
    if request.method == 'POST':
        status = request.POST.get('trade_status', 'result')
        if status in ("TRADE_SUCCESS", "TRADE_FINISHED" ):
            # 获取必要的参数
            
            # 获取充值类型
            subject = request.POST.get('subject', None)
            subject = urllib.parse.unquote(subject)
            # 商户订单号
            order_id = request.POST.get('out_trade_no')
            # 充值金额
            money = request.POST.get('total_amount')
            # 学号
            studentID = order_id[-12:]
            
            # 根据充值类型，增更数据库数据, 如果开头不为s那么一定是电费充值
            if order_id[0] != 's':
                # 地址编号
                dromID = re.findall('.*?df', order_id)[0][:-2]
                if writeToOrders(order_id, subject, money) and writeToDorm(order_id, dromID):
                    result = updateElec(dromID, money)
                    updateStatus(order_id, result)
            else:
                # 加入订单号# 加入订单的学生信息
                if writeToOrders(order_id, subject, money) and writeToSOW(order_id, studentID):
                    # 更新学生的金额
                    result = updateSOW(subject, studentID, money)
                    updateStatus(order_id, result)
                
            Log(status)
            Log("result", "lin")
        return HttpResponse('success')
    return HttpResponse('error')

# 同步调用
def get(request):
    alipay = create_alipay()
    # 存放错误集合
    errors = []
    # html传参对象, csrf格式化是用于处理cookie问题
    context = csrf(request)
    # 初始化一个字典
    Dict = dict()
    Dict['window'] = '/pay/'
    
    if request.method == 'GET':
        params = request.GET.dict()
        sign = params.pop('sign', None)
        status = alipay.verify(params, sign)
        if status == True:
            errors.append("\t\t你已经充值成功！")
            html = 'success.html'
        else:
            errors.append("\t\t返回时出现问题")
            html = 'error.html'
        Dict['errors'] = errors
        context.update(Dict)
        return render(request, html, context)
# 写入日志
def Log(string, ty='lin'):
    if ty == 'win':
        with open(r'D:\文档堆\文档\码源世界\代码练习\python\momosite\pay\logs.txt', 'a+') as f:
            f.write(string+'\n')
    else:
        with open(r"/var/www/momosite/pay/logs.txt", "a+") as f:
            f.write(string+'\n')

# 测试页面
def test(request):
    result = writeToDorm('123456', 'X4B105')
    #result = writeToSOW('123456', '201655110215')
    return HttpResponse(result)



