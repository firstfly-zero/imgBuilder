from django.db import models
from configs.base import BaseModel
from django.contrib.auth.models import AbstractUser

# 系统的用户
class IBUser(BaseModel, AbstractUser):
    ROLES = [
        ('admin', '管理员(机器人+图库+邀请人)'),
        ('userVip4', '用户(机器人+图库)——留作扩展'),
        ('userVip3', '用户(机器人+图库)——留作扩展'),
        ('userVip2', '用户(机器人+图库)'),
        ('userVip1', '用户(机器人)'),
        ('userVip0', '用户(仅登录)'),
    ]
    avatar = models.CharField(max_length=1000, default="")
    role = models.CharField(max_length=1000, default="userVip0", choices=ROLES)

    class Meta:
        db_table = 'ib_user'
        verbose_name = '用户信息表'
        verbose_name_plural = verbose_name

# 邀请信息表
class IBUserInviter(BaseModel):
    user = models.ForeignKey(IBUser, on_delete=models.DO_NOTHING, default=None, related_name='inviter_user')
    inviter = models.ForeignKey(IBUser, on_delete=models.DO_NOTHING, default=None, related_name='inviter_inviter')

    class Meta:
        db_table = 'ib_user_inviter'
        verbose_name = '用户邀请信息表'
        verbose_name_plural = verbose_name

# 验证码
class IBVerificationCode(BaseModel):
    VERIFICATION_CODE_STATUS = [
        ('valid', '有效'),
        ('invalid', '无效')
    ]
    email = models.CharField(max_length=1000, default="")
    code = models.CharField(max_length=6)
    status = models.CharField(max_length=20, default="valid", choices=VERIFICATION_CODE_STATUS)

    class Meta:
        db_table = 'ib_user_verification_code'
        verbose_name = '用户验证码'
        verbose_name_plural = verbose_name

# 用户分享
class IBUserShare(BaseModel):
    SHARE_TYPE = [
        ('image', '图片'),
        ('mjImage', 'mj图片'),
        ('sdImage', 'sd图片'),
        ('video', '视频'),
        ('voice', '音频'),
        ('file', '文件'),
    ]
    user = models.ForeignKey(IBUser, on_delete=models.DO_NOTHING, default=None)
    share_type = models.CharField(max_length=20, default="mjImage", choices=SHARE_TYPE)
    share_info = models.JSONField(verbose_name='分享相关信息')

    class Meta:
        db_table = 'ib_user_share'
        verbose_name = '用户分享内容'
        verbose_name_plural = verbose_name
