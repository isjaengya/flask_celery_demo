import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(mail_host, mail_user, mail_password, sender, to_receivers, cc_receivers=None, subject=None, filepath=None, filename=None):

    if cc_receivers:
        receivers = to_receivers + cc_receivers
    else:
        receivers = to_receivers

    message = MIMEMultipart()

    message['From'] = sender
    message['To'] = ';'.join(to_receivers)
    if cc_receivers:
        message['Cc'] = ';'.join(cc_receivers)
    message['Subject'] = subject

    attach = MIMEText(open(filepath).read(), 'base64', 'utf-8')
    attach["Content-Type"] = 'application/octet-stream'
    attach["Content-Disposition"] = 'attachment; filename="{}"'.format(filename)
    message.attach(attach)
    try:
        smtp = smtplib.SMTP_SSL()
        smtp.connect(mail_host, 465)
        smtp.login(mail_user, mail_password)
        smtp.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print(e)
        print("Error: 无法发送邮件")
    return {}
