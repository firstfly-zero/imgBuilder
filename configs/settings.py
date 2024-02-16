from pathlib import Path
import datetime, os

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = ""

DEBUG = False
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework_jwt",
    "ibuser",
    "robot",
    "gallery",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "configs.base.CustomMiddleware",
]

ROOT_URLCONF = "configs.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates']
        ,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "configs.wsgi.application"

DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "zh-hans"

TIME_ZONE = "Asia/Shanghai"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = []
STATIC_ROOT=os.path.join(BASE_DIR,'static')

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# token 过期时间
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=30),
}

# 自定义用户
AUTH_USER_MODEL = 'ibuser.IBUser'

# 定义路由白名单
NO_AUTH_API_LIST = [
    "api/v1/user/login",
    "api/v1/user/register"
]

# 腾讯云对象存储默认配置
COS_CONFIG = {
    "secret_id" : "",
    "secret_key" : "",
    "region" : '',
    "bucket" : "",
}

SD_CONFIG = {
    "baseurl" : "",
    "username" : "",
    "password" : '',
}

BD_TRANS_CONFIG = {
    "appId": "",
    "apiKey": "",
    "secretKey": ""
}

# myself
MJ_CONFIG = {
    "authorization": "MTIwMjg2OTgxODkwMzEwOTYzMg.GNA15v.iYnNKLICvv_03FJVCmmpVXhZiWYocfEs8f7Jn0",
    "channel_id": "1207303887707705367",
    "application_id": "936929561302675456",
    "guild_id": "1207303887707705364",
    "session_id": "2ec0e481dd52de514dc7ab5b696776f9",
    "version": "1166847114203123795",
    "id": "938956540159881230",
    "flags": "",
    "proxy": "127.0.0.1:7890"
}


# GPT设置
GPT_CONFIG = {
    "base_url": "https://api.chatanywhere.com.cn",
    "api_key": "",
    "model": "gpt-4-1106-preview",
    "system_message": {
        "role": "system",
        "content": "你是图著系统的机器人，叫做小图。"
    }
}

INTENT_DETECT_CONFIG = {
    "base_url": "https://api.chatanywhere.com.cn",
    "api_key": "",
    "model": "gpt-4-1106-preview",
    "system_message": {
        "role": "system",
        "content": "你好 gpt，你现在是一个意图识别器，你的回答只能是“文本”、“图片”、“语音”、“其他”这四个选项。你会根据我的输入判断我期望的你的回答的形式，现在给你几个例子：我想看看蓝天你要输出图片，我想听听你的建议你要输出语音，解释一下模态你要输出文本，跟前面意思关联不大的你就输出其他。"
    }
}

SUMMARY_GPT_CONFIG = {
    "base_url": "https://api.chatanywhere.com.cn",
    "api_key": "",
    "model": "gpt-3.5-turbo",
    "system_message": {
        "role": "system",
        "content": "你具有强大的知识获取和整合能力，拥有广泛的知识库，掌握提问和回答的技巧，拥有排版审美，会利用序号、缩进、分隔线和换行符等等来美化信息排版，擅长使用比喻的方式来让用户理解知识，惜字如金，不说废话。请帮我总结这个网页的所有正文内容，最多用300字"
    }
}

# 工作目录
# WORKSPACE = "/app/workspace/"
WORKSPACE = "/Users/jiayifei/workspace/"

# 电子邮件相关
# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = '916457600@qq.com'
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

