from django.shortcuts import render, HttpResponse
from .forms import TextEmailForm, FileMailForm  # 定义的表单类
from django.core.mail import send_mail  # 发送单封邮件
from django.core.mail import send_mass_mail  # 发送多封邮件
from django.core.mail import EmailMultiAlternatives  # 发送带有附件邮件
from django.conf import settings  # 配置文件
import os

def write_email(request):
    email_form = FileMailForm()
    return render(request, 'email.html', {'email_form': email_form})

def upload_handler(file, file_name):
    path = os.path.join(settings.BASE_DIR, 'uploads/')  # 项目根目录下的附件上传目录
    if not os.path.exists(path):  # 如果目录不存在
        os.makedirs(path)  # 创建目录
    with open(path + file_name, 'wb+') as f:  # 打开文件
        for chunk in file.chunks():  # 读取上传文件
            f.write(chunk)  # 写入文件
    return path + file_name  # 返回文件路径

def file_mail_send(subject, message, sender, addressees, file):
    email = EmailMultiAlternatives(subject, message, sender, addressees)  # 创建邮件对象
    file_path = upload_handler(file, str(file))  # 上传附件并获取文件路径
    email.attach_file(file_path)  # 附加文件到邮件对象
    email.send()  # 发送邮件

def send_email(request):
    if request.method == 'POST':  # 如果表单为“POST”方法提交，则进行邮件发送。
        if request.FILES:  # 如果包含附件
            email_form = FileMailForm(request.POST, request.FILES)  # 创建包含附件的表单对象
            file = request.FILES['file']  # 获取附件信息
        else:
            email_form = TextEmailForm(request.POST)  # 创建不包含附件的表单对象
            file = None
        if email_form.is_valid():  # 如果验证有效
            addressees = email_form.cleaned_data['addressees'].split(',')  # 获取所有收件地址的列表
            subject = email_form.cleaned_data['subject']  # 获取邮件标题
            message = email_form.cleaned_data['message']  # 获取邮件内容
            cc_myself = email_form.cleaned_data['cc_myself']  # 获取是否抄送发件人
            if cc_myself:  # 如果抄送发件人
                addressees.append(settings.EMAIL_HOST_USER)  # 添加发件人的邮件地址到收件地址列表
            count = len(addressees)  # 获取发件数量
            email = [subject, message, settings.DEFAULT_FROM_EMAIL, addressees]  # 保存所有发件信息到变量
            try:
                if file:  # 如果包含附件
                    file_mail_send(*email, file)  # 调用发送带有附件邮件的函数
                    file_name = '(附件：%s)' % str(file)  # 发送成功信息中的附件信息
                else:  # 如果不包含附件
                    if count > 1:  # 如果有多个收件地址
                        send_mass_mail((email,))  # 调用适合发送多封邮件的方法
                    else:  # 否则
                        send_mail(*email)  # 调用适合发送单封邮件的方法
                    file_name = ''
            except:
                # raise  # 编写代码时获取异常信息
                return HttpResponse('Failed！Please check the ')  # 如果发送邮件发生异常，则给出提示。
            return render(request, 'thanks.html',
                          {'count': count, 'to': addressees, 'file': file_name})  # 正常发送邮件后，页面显示发送邮件的相关信息。
        else:  # 如果验证失败，则进行提示。
            return HttpResponse('验证失败！')
    else:  # 如果表单不是“POST”方法提交，则回到撰写邮件的页面。
        email_form = FileMailForm()
        return render(request, 'email.html', {'email_form': email_form})