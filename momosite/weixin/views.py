# 这是我加的
from django.shortcuts import render, get_object_or_404
from django.template.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist

from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .func.weixinSolve import *
from weixin import models
from .models import *

#django默认开启csrf防护，这里使用@csrf_exempt去掉防护
@csrf_exempt
def main(request):
    try:
        # 设置微信平台的TOKEN
        TOKEN = 'test'
        # new 一个weixinSolve对象，传入token
        weixin = weixinSolve(TOKEN)
        # 判断是进行签名验证，还是处理客户的操作信息
        # 如果是GET请求，那么就是验证签名
        if request.method == "GET":
            # 接收微信服务器get请求发过来的参数
            signature = request.GET.get('signature', None)
            timestamp = request.GET.get('timestamp', None)
            nonce = request.GET.get('nonce', None)
            echostr = request.GET.get('echostr', None)

            # 判断数字签名是否正确，通过类包装好的方法
            result = weixin.valid(signature, timestamp, nonce)
            # 如果是正确的签名，返回echostr
            if result == True:
              return HttpResponse(echostr)
            else:
              return HttpResponse(echostr)
        # 开始响应客户的操作
        else:
            # 获取整个请求无论是get还是post还是其他的方式发来的数据，构建webData
            webData = request.body
            # 通过包装好的类的方法，进行处理，获取要发送的信息
            content = weixin.responseMsg(webData)
            # 把信息发送到微信平台上
            return HttpResponse(content)
    except:
        return HttpResponse("hello, world!!")

# 显示查询页面
def query(request):
    return render(request, 'chaxun.html')

# 显示查询结果页面
def ShowQuery(request):
    # 存放错误集合
    errors = []
    # html传参对象, csrf格式化是用于处理cookie问题
    context = csrf(request)
    # 初始化一个字典
    Dict = dict()
    
    # 如果收到的是POST请求
    if request.method == 'POST':
        # 获取学号框里的数据
        ids = request.POST.get('id', '')
        # 获取姓名框里的数据
        name = request.POST.get('name', '')

        # 存入查询网页的地址,这个用于error网页里，按钮点击返回查询网页
        Dict['window'] = '/query/'
        
        try:
            # 向数据库中的 学生信息表 查询符合条件的学生
            student = StudentsInfo.objects.get(学号=ids, 姓名=name)
        # 如果查不到，抛出错误
        except ObjectDoesNotExist:
            errors.append("\t\t\t输入信息不对\n\t\t查不到该学生信息!!")
            Dict['errors'] = errors
            context.update(Dict)
            return render(request, 'error.html', context)
        except:
            return render(request, 'chaxun.html')
        
        try:
            # 向数据库中的 学生账户数据表 查询符合条件的账户信息
            balance = student.studentsbalance
        # 如果查不到，抛出错误
        except ObjectDoesNotExist:
            errors.append("\t\t\t查无此讯\n\t\t请及时反馈您的问题给我们!")
            Dict['errors'] = errors
            context.update(Dict)
            return render(request, 'error.html', context)
        except:
            return render(request, 'chaxun.html')

        # 抛出错误的，不会走到这一步来，那么只有正确的会执行到这一步
        Dict['dorm'] = student.住址编号.剩余电量
        Dict['balance'] = balance
        
    context.update(Dict)
    # 调用查询结果表，并把查询到的值以字典的形式传参给html网页
    return render(request, 'chaxunform.html', context)


# 显示问题反馈页面
def question(request):
    return render(request, 'wenti.html')

# 处理问题反馈信息
def showQuestion(request):
    # 存放错误集合
    errors = []
    # 参数字典
    context = csrf(request)
    # 初始化一个字典
    Dict = dict()

    
    # 如果收到的是POST请求
    if request.method == 'POST':
        # 获取联系人姓名
        name = request.POST.get('name', None)
        # 获取联系方式
        phone = request.POST.get('phone', None)
        # 获取反馈的问题
        question =request.POST.get('message', None)

        # 存入查询网页的地址,这个用于error网页里，按钮点击返回查询网页
        Dict['window'] = '/question/'
        
        # 联系方式或问题内容为空时，不允许
        if not question or not phone:
            if not question :
                errors.append('\t\t\t请输入您的联系方式\n')
            if not phone:
                errors.append('\t\t\t请输入您要反馈的问题\n')
            Dict['errors'] = errors
            context.update(Dict)
            return render(request, 'error.html', context)
        try:
            # 把获取的数据存入数据库中Questions表中
            Questions.objects.create(联系人=name, 联系方式=phone, 问题=question)
            
        except ObjectDoesNotExist:
            errors.append("\t\t\t输入信息错误\n\t\t\t请重新输入!!")
            Dict['errors'] = errors
            context.update(Dict)
            return render(request, 'error.html', context)
        except:
            return render(request, 'wenti.html')
            
        errors.append("\t\t\t问题已经传达\n\t\t我们会尽快处理好您的问题\n\t\t\t请保持联系")
        Dict['errors'] = errors
        
    context.update(Dict)

    return render(request, 'success.html', context)


def czStudentOrWater(request):
    return render(request, 'chongzhi1.html')

# 处理充值学生卡和水卡
def showCzStudentOrWater(request):
    # 存放错误集合
    errors = []
    # 参数字典
    context = csrf(request)
    # 初始化一个字典
    Dict = dict()
    # 如果收到的是POST请求
    if request.method == 'POST':
        # 获取充值的类型
        select = request.POST.get('select', '')
        # 获取学号
        ids = request.POST.get('id', '')
        # 获取姓名
        name = request.POST.get('name', '')
        # 获取充值的钱
        money =request.POST.get('money', '')

        # 存入查询网页的地址,这个用于error网页里，按钮点击返回查询网页
        Dict['window'] = '/chongzhi/'
        
        try:
            errors.append(select)
            errors.append(ids)
            errors.append(name)
            errors.append(money)
            
        except ObjectDoesNotExist:
            errors.append("\t\t\t输入信息错误\n\t\t\t请重新输入!!")
            Dict['errors'] = errors
            context.update(Dict)
            return render(request, 'error.html', context)
        except:
            return render(request, 'chongzhi1.html')
            
        Dict['errors'] = errors
        
    context.update(Dict)

    return render(request, 'error.html', context)
