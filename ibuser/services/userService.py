import random
import string
from django.core.mail import send_mail
from configs.settings import DEFAULT_FROM_EMAIL

def generate_verification_code():
    """生成6位数字的验证码"""
    return ''.join(random.choices(string.digits, k=6))

def send_verification_email(email, code):
    subject = '图库系统验证码'
    message = f'欢迎注册图库系统\n你的验证码是：{code}'
    email_from = DEFAULT_FROM_EMAIL
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)