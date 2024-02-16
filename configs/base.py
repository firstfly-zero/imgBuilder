from django.db import models
from django.utils import timezone
from django.http import JsonResponse
from rest_framework_jwt.settings import api_settings
from configs.settings import NO_AUTH_API_LIST
import json

# 表基础结构
class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        abstract = True

# 定义成功的响应
class SuccessResponse(JsonResponse):
    def __init__(self, data, encoder=None, safe=True, json_dumps_params=None, **kwargs):
        response_data = {
            "status": 'ok',
            "msg": 'success',
            "code": 20000,
            "data": data
        }
        super().__init__(response_data, encoder=encoder, safe=safe, json_dumps_params=json_dumps_params, **kwargs)

# 定义失败的响应
class FailureResponse(JsonResponse):
    def __init__(self, msg, encoder=None, safe=True, json_dumps_params=None, **kwargs):
        response_data = {
            "status": 'fail',
            "msg": msg,
            "code": 40000,
        }
        super().__init__(response_data, encoder=encoder, safe=safe, json_dumps_params=json_dumps_params, **kwargs)

# 请求初始化
class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 静态资源、API 白名单访问不需要获取用户信息
        if request.path.startswith("/static") or request.path in NO_AUTH_API_LIST:
            return self.get_response(request)

        # 封装请求体
        try:
            request.params = json.loads(request.body.decode("utf-8"))
        except:
            request.params = json.loads("{}")

        # 获取用户相关数据
        try:
            token = request.headers.get("Authorization")[7:]
            request.username = api_settings.JWT_DECODE_HANDLER(token).get('username')
        except:
            request.username = None

        return self.get_response(request)
