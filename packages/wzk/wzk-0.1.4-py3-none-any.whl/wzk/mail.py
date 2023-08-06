import smtplib
from email.mime.text import MIMEText
from email.header import Header


mail_host = None  #设置SMTP服务器，如smtp.qq.com
mail_user = None  #发送邮箱的用户名，如xxxxxx@qq.com
mail_pass = None  #发送邮箱的密码（注：QQ邮箱需要开启SMTP服务后在此填写授权码）
sender = None  #发件邮箱，如xxxxxx@qq.com


class MailNotInitializeError(Exception):
    def __str__(self):
        return "you should initialize send_mail by calling wzk.email.init(host, addr, password)"


def init(host, mail_addr, password):
    global mail_host, mail_user, mail_pass, sender
    mail_host = host
    mail_user = mail_addr
    mail_pass = password
    sender = mail_addr


def send_mail(title, content, receiver=mail_user):
    # 第三方 SMTP 服务

    if not (mail_host and mail_user and mail_pass and sender):
        raise MailNotInitializeError

    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = Header(sender, 'utf-8')  #发件人
    message['To'] = Header(receiver, 'utf-8')  #收件人
    subject = title  #主题
    message['Subject'] = Header(subject, 'utf-8')
    print('Prepare success')
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        print('Connect success')
        smtpObj.login(mail_user, mail_pass)
        print('Login success')
        smtpObj.sendmail(sender, receiver, str(message))
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("ERROR：无法发送邮件")