import datetime
import random

from django.core.mail import EmailMessage
from django.core.mail import send_mail  # 发送邮件模块
from django.conf import settings    # setting.py添加的的配置信息
from django.template import loader

from user_web.models import Code


def random_code():
    lis = []
    res1 = ""
    for i in range(6):
        num = random.randint(0, 9)
        res1 += str(num)
    lis.append(res1)
    return res1


def send_sms_code(to_mail, send_type="register"):
    # 生成邮箱验证码
    email_record = Code()
    code = random_code()
    email_record.code = code
    email_record.mail = to_mail
    email_record.send_type = send_type
    email_record.send_time = datetime.datetime.now()
    email_record.save()

    email_title = ""
    email_body = ""

    if send_type == "register":
        email_title = "用户注册验证"

        # email_body = "欢迎使用墨书，您的邮箱注册验证码为：{0}，该验证码有效时间为五分钟，请及时验证。".format(code)
        # send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [to_mail])
        # if not send_status:
        #     return False

        context = {'code1': code[0],
                   'code2': code[1],
                   'code3': code[2],
                   'code4': code[3],
                   'code5': code[4],
                   'code6': code[5]}
        email_template_name = 'code_mail.html'
        t = loader.get_template(email_template_name)
        html_content = t.render(context)

        msg = EmailMessage(email_title, html_content, settings.EMAIL_FROM, [to_mail])
        msg.content_subtype = 'html'
        send_status = msg.send()
        if not send_status:
            return False

    return True
