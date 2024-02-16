from django.db import models
from configs.base import BaseModel
from ibuser.models import IBUser

# sd相关
SDTASK_STATUS=[
    ("init", "初始化"),
    ("starting", "进行中"),
    ("done", "已完成"),
    ("sent", "完成信息已发送"),
    ("cancel", "已取消")
]
SDTASK_TYPE=[
    ("txt2img", "文生图"),
    ("img2img", "图生图"),
    ("txt2imgByCN", "controlNet生图"),
]

# 微信sd任务表
class WxSdtask(BaseModel):
    user = models.ForeignKey(IBUser, on_delete=models.DO_NOTHING, default=1)

    params = models.JSONField(verbose_name='参数')
    status = models.CharField(max_length=20, default="init", verbose_name='任务状态', choices=SDTASK_STATUS)
    type = models.CharField(max_length=20, default="init", verbose_name='任务类型', choices=SDTASK_TYPE)
    image_url = models.CharField(max_length=1000, default="", verbose_name='生成图片路径')

    wx_msg = models.CharField(max_length=1000, default="", verbose_name='微信消息')
    wx_user_id = models.CharField(max_length=1000, default="", verbose_name='微信用户id')
    wx_nickname = models.CharField(max_length=1000, default="", verbose_name='微信昵称')
    wx_bot = models.CharField(max_length=1000, default="", verbose_name='微信机器人id')

    def get_json(self):
        return {
            "id": self.id,
            "type": self.type,
            "image_url": self.image_url,
            "wx_msg": self.wx_msg,
            "wx_user_id": self.wx_user_id,
            "wx_nickname": self.wx_nickname,
            "wx_bot": self.wx_bot
        }

    class Meta:
        db_table = 'ib_wxsdtask'
        verbose_name = '微信机器人SD任务表'
        verbose_name_plural = verbose_name

# 飞书sd任务表
class LarkSdtask(BaseModel):
    user = models.ForeignKey(IBUser, on_delete=models.DO_NOTHING, default=1)

    params = models.JSONField(verbose_name='参数')
    status = models.CharField(max_length=20, default="init", verbose_name='任务状态', choices=SDTASK_STATUS)
    type = models.CharField(max_length=20, default="init", verbose_name='任务类型', choices=SDTASK_TYPE)
    image_url = models.CharField(max_length=1000, default="", verbose_name='生成图片路径')

    lark_msg = models.JSONField(verbose_name='飞书消息', default=dict, null=True, blank=True)
    lark_app_id = models.CharField(max_length=1000, default="", verbose_name='飞书机器人id')
    open_id = models.CharField(max_length=1000, default="", verbose_name='对应的用户id')
    open_chat_id = models.CharField(max_length=1000, default="", verbose_name='飞书对话id')

    def get_json(self):
        return {
            "id": self.id,
            "type": self.type,
            "image_url": self.image_url,
            "lark_msg": self.lark_msg,
            "lark_app_id": self.lark_app_id
        }

    class Meta:
        db_table = 'ib_larksdtask'
        verbose_name = '飞书机器人SD任务表'
        verbose_name_plural = verbose_name

# mj相关
MJTASK_STATUS=[
    ("init", "初始化"),
    ("starting", "已发送至mj"),
    ("done", "已完成"),
    ("sent", "完成信息已发送"),
    ("cancel", "已取消")
]
MJTASK_TYPE=[
    ("imagine", "生图"),
    ("UVX", "UV变换"),
    ("blend", "融图"),
]

# 微信mj任务表
class WxMjtask(BaseModel):
    user = models.ForeignKey(IBUser, on_delete=models.DO_NOTHING, default=1)

    origin_prompt = models.CharField(max_length=1000, default="")
    final_prompt = models.CharField(max_length=1000, default="")

    status = models.CharField(max_length=20, default="init", choices=MJTASK_STATUS)
    type = models.CharField(max_length=20, default="init", verbose_name='任务类型', choices=MJTASK_TYPE)
    mj_image_url = models.CharField(max_length=1000, default="", verbose_name='mj原图片路径')
    oss_image_url = models.CharField(max_length=1000, default="", verbose_name='腾讯云图片路径')
    mj_done_msg = models.JSONField(verbose_name='完成信息')

    wx_msg = models.CharField(max_length=1000, default="", verbose_name='微信消息')
    wx_user_id = models.CharField(max_length=1000, default="", verbose_name='微信用户id')
    wx_nickname = models.CharField(max_length=1000, default="", verbose_name='微信昵称')
    wx_bot = models.CharField(max_length=1000, default="", verbose_name='微信机器人id')

    def get_json(self):
        return {
            "id": self.id,
            "mj_image_url": self.mj_image_url,
            "oss_image_url": self.oss_image_url,
            "wx_msg": self.wx_msg,
            "wx_user_id": self.wx_user_id,
            "wx_nickname": self.wx_nickname,
            "wx_bot": self.wx_bot,
        }

    class Meta:
        db_table = 'ib_wxmjtask'
        verbose_name = '微信机器人MJ任务表'
        verbose_name_plural = verbose_name

# 飞书mj任务表
class LarkMjtask(BaseModel):
    user = models.ForeignKey(IBUser, on_delete=models.DO_NOTHING, default=1)

    origin_prompt = models.CharField(max_length=1000, default="")
    final_prompt = models.CharField(max_length=1000, default="")

    status = models.CharField(max_length=20, default="init", choices=MJTASK_STATUS)
    type = models.CharField(max_length=20, default="init", verbose_name='任务类型', choices=MJTASK_TYPE)
    mj_image_url = models.CharField(max_length=1000, default="", verbose_name='mj原图片路径')
    oss_image_url = models.CharField(max_length=1000, default="", verbose_name='腾讯云图片路径')
    mj_done_msg = models.JSONField(verbose_name='完成信息')

    lark_msg = models.JSONField(verbose_name='飞书消息', default=dict, null=True, blank=True)
    lark_app_id = models.CharField(max_length=1000, default="", verbose_name='飞书机器人id')

    def get_json(self):
        return {
            "id": self.id,
            "mj_image_url": self.mj_image_url,
            "oss_image_url": self.oss_image_url,
            "lark_msg": self.lark_msg,
            "lark_app_id": self.lark_app_id,
        }

    class Meta:
        db_table = 'ib_larkmjtask'
        verbose_name = '飞书机器人MJ任务表'
        verbose_name_plural = verbose_name

# 微信图片消息表
WX_IMAGE_STATUS = [
    ('inited', '已上传'),
    ('saved', '已保存'),
    ('delete', '已删除')
]
class WxImage(BaseModel):
    user = models.ForeignKey(IBUser, on_delete=models.DO_NOTHING, default=1)

    url = models.CharField(max_length=1000, default="")
    height = models.FloatField(default=0.0, verbose_name='图片高度')
    width = models.FloatField(default=0.0, verbose_name='图片宽度')
    size = models.FloatField(default=0.0, verbose_name='图片大小')
    status = models.CharField(max_length=20, default="public", choices=WX_IMAGE_STATUS)
    from_user = models.CharField(max_length=1000, default="")

    class Meta:
        db_table = 'ib_wximage'
        verbose_name = '微信图片消息表'
        verbose_name_plural = verbose_name

# 机器人配置信息表
CONFIG_TYPE = [
    ('common', '通用配置'),
    ('template_sd_txt2img', 'sd文生图模版'),
    ('template_sd_img2img', 'sd图生图模版'),
    ('template_sd_txt2imgbycn', 'sd文生图 controlnet 模版'),
]
class Config(BaseModel):
    key = models.CharField(max_length=1000, default="")
    value = models.CharField(verbose_name='文本类配置内容', max_length=1000, default="", null=True, blank=True)
    content = models.JSONField(verbose_name='json类配置内容', default=dict, null=True, blank=True)
    desc = models.CharField(max_length=1000, verbose_name='描述', default="", null=True, blank=True)
    type = models.CharField(max_length=100, verbose_name='配置类型', default="common", choices=CONFIG_TYPE)

    class Meta:
        db_table = 'ib_botconfig'
        verbose_name = '机器人配置信息表'
        verbose_name_plural = verbose_name

# 飞书机器人信息表
LARK_BOT_STATUS = [
    ('valid', '生效中'),
    ('invalid', '已失效'),
    ('delete', '已删除'),
]
LARK_BOT_TYPE = [
    ('mj', 'mj机器人'),
    ('sd', 'sd机器人'),
    ('gpt', 'gpt机器人'),
    ('mj&sd', 'mj和sd机器人'),
    ('mj&gpt', 'mj和gpt机器人'),
    ('sd&gpt', 'sd和gpt机器人'),
    ('mj&sd&gpt', 'mj、sd、gpt机器人'),
]
class LarkBotInfo(BaseModel):
    user = models.ForeignKey(IBUser, on_delete=models.DO_NOTHING, default=1)

    app_id = models.CharField(max_length=1000, default="")
    app_secret = models.CharField(max_length=1000, default="")
    status = models.CharField(max_length=20, default="valid", choices=LARK_BOT_STATUS)
    type = models.CharField(max_length=20, default="mj&sd&gpt", choices=LARK_BOT_TYPE)
    desc = models.CharField(max_length=1000, default="")
    extra_config = models.JSONField(verbose_name='额外配置', default=dict, null=True, blank=True)

    class Meta:
        db_table = 'ib_larkbot'
        verbose_name = '飞书机器人信息表'
        verbose_name_plural = verbose_name



