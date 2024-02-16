from django.db import models
from django.utils import timezone
from ibuser.models import IBUser
from configs.base import BaseModel


# 密钥表
SECRET_STATUS = [
    ('init', '初始化'),
    ('actived', '已激活'),
    ('bound', '已兑换'),
    ('expired', '已过期'),
    ('invalid', '失效'),
]
class Secret(BaseModel):
    secret = models.CharField(max_length=1000, default="")
    status = models.CharField(max_length=20, default="init", choices=SECRET_STATUS)
    user = models.ForeignKey(IBUser, on_delete=models.DO_NOTHING, default=None)
    size = models.FloatField(default=0.0, verbose_name='卡密兑换空间大小')
    expiration = models.IntegerField()

    class Meta:
        db_table = 'ib_secret'
        verbose_name = '卡密信息表'
        verbose_name_plural = verbose_name

# 代理人邀请信息表
class AgentInviteInfo(BaseModel):
    agentcode = models.CharField(max_length=1000, default="")
    user = models.ForeignKey(IBUser, on_delete=models.DO_NOTHING, default=None)

    class Meta:
        db_table = 'ib_agent_invite'
        verbose_name = '代理人邀请信息表'
        verbose_name_plural = verbose_name

# 图库信息表——图库只需要标记属于哪个用户
GALLERY_STATUS = [
    ('生效中', '生效中'),
    ('已删除', '已删除'),
    ('未生效', '未生效')
]
class Gallery(BaseModel):
    user = models.ForeignKey(IBUser, on_delete=models.DO_NOTHING, default=None)
    invite_code = models.CharField(max_length=1000, default="")
    gallery_name = models.CharField(max_length=1000, default="")
    image_num = models.IntegerField(default=0, verbose_name='当前图片数')
    max_image_num = models.IntegerField(default=0, verbose_name='最大图片数')
    expired_time = models.DateTimeField(default=timezone.now, verbose_name='会员过期时间')
    status = models.CharField(max_length=20, default="valid", choices=GALLERY_STATUS)

    class Meta:
        db_table = 'ib_gallery'
        verbose_name = '图库信息表'
        verbose_name_plural = verbose_name

# 相册信息表——相册只需要标记属于哪个图库
ALBUM_STATUS = [
    ('delete', '已删除'),
    ('public', '公开'),
    ('private', '私有')
]
class Album(BaseModel):
    gallery = models.ForeignKey(Gallery, on_delete=models.DO_NOTHING, default=None)
    album_name = models.CharField(max_length=1000, default="")
    title = models.CharField(max_length=1000, default="")
    desc = models.CharField(max_length=1000, default="")
    image_num = models.IntegerField(default=0, verbose_name='图片数')
    status = models.CharField(max_length=20, default="public", choices=ALBUM_STATUS)

    def get_json(self):
        images = Image.objects.filter(album=self)
        image_list = []
        for image in images:
            image_list.append(image.get_json())
        self.image_num = len(image_list)
        cover = image_list[0].get("url") if len(image_list) > 0 else "https://aiclub-1311445709.cos.ap-guangzhou.myqcloud.com/imgbuilder/80/1706088211/tmp/1706088211004.png"
        return {
            "id": self.id,
            "album_name": self.album_name,
            "title": self.title,
            "cover": cover,
            "desc": self.desc,
            "image_num": len(image_list),
            "image_list": image_list,
            "status": self.status,
        }

    class Meta:
        db_table = 'ib_album'
        verbose_name = '相册信息表'
        verbose_name_plural = verbose_name

# 图片信息表——图片只需要标记属于哪个相册
IMAGE_STATUS = [
    ('delete', '已删除'),
    ('public', '公开'),
    ('private', '私有')
]
IMAGE_TAG = [
    ('sd', 'sd 生成'),
    ('mj', 'mj 生成'),
    ('upload', '用户上传'),
    ('wxupload', '用户微信上传'),
]
class Image(BaseModel):
    album = models.ForeignKey(Album, on_delete=models.DO_NOTHING, default=None)
    url = models.CharField(max_length=1000, default="")
    height = models.FloatField(default=0.0, verbose_name='图片高度')
    width = models.FloatField(default=0.0, verbose_name='图片宽度')
    tag = models.CharField(max_length=20, default="upload", choices=IMAGE_TAG)
    status = models.CharField(max_length=20, default="public", choices=IMAGE_STATUS)

    def get_json(self):
        return {
            "id": self.id,
            "url": self.url,
            "height": self.height,
            "width": self.width,
            "tag": self.tag,
            "status": self.status,
        }

    class Meta:
        db_table = 'ib_image'
        verbose_name = '图片信息表'
        verbose_name_plural = verbose_name
