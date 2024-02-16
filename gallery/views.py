from utils.oss_utils import Cos
from utils.sd_utils import SD
from configs.settings import COS_CONFIG, SD_CONFIG
from configs.base import SuccessResponse, FailureResponse
from django.http import JsonResponse, FileResponse
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User
from gallery.models import Image, Album, Gallery, Secret
import hashlib, time, os, json, datetime, requests, random
from django.db.models import F, Q
import PIL.Image as pImage

# 对象存储初始化
cos = Cos(secret_id=COS_CONFIG['secret_id'], secret_key=COS_CONFIG['secret_key'], region=COS_CONFIG['region'])
sd = SD(baseurl=SD_CONFIG['baseurl'], username=SD_CONFIG['username'], password=SD_CONFIG['password'])

# 上传图片
def upload_image(request):
    # 获取文件
    file = request.FILES['file']
    # 将文件临时存储到本地
    with open(os.path.join('/tmp', file.name), 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    # 获取图片的宽和高
    img = pImage.open(os.path.join('/tmp', file.name))
    width, height = img.size
    # 将文件上传到存储桶中
    oss_image_url = cos.get_url(bucket=COS_CONFIG["bucket"], key=cos.upload_file(bucket=COS_CONFIG["bucket"], key="imgbuilder/{}/{}/{}".format(request.username if request.username!=None else "public", str(int(time.time())), file.name), local_path="/tmp/{}".format(file.name)))

    return SuccessResponse({
        "url": oss_image_url,
        "height": height,
        "width": width
    })

# 将图片添加到相册
def upload_image_to_album(request):
    # 获取相册，并在相册下添加图片
    album = Album.objects.get(id=request.params["album_id"] if request.params.get("album_id") != None else 1)
    # 添加图片
    image = Image()
    image.album = album
    image.height = request.params.get("height")
    image.width = request.params.get("width")
    image.url = request.params.get("url")
    image.tag = request.params.get("tag")
    image.save()
    # 更新相册的图片数
    album.image_num = album.image_num + 1
    album.save()

    return SuccessResponse(image.get_json())

# 获取相册下的图片
def get_album_image_list(request):
    album = Album.objects.get(id=request.params["album_id"])
    images = Image.objects.filter(album=album).order_by("-id")
    imageList = []
    for image in images:
        imageList.append(image.get_json())

    return SuccessResponse(imageList)

# 搜索图库下所有图片
def get_gallery_image_list(request):
    gallery_id = request.params["gallery_id"]

    gallery = Gallery.objects.get(id=gallery_id)
    albums = Album.objects.get(gallery=gallery)
    imageList = []
    for album in albums:
        images = Image.objects.filter(album=album).order_by("-id")
        for image in images:
            imageList.append(image.get_json())

    return SuccessResponse(imageList)

# 删除图片
def delete_image(request):
    Image.objects.get(id=request.GET.get("imageId")).delete()
    return SuccessResponse([])

# 下载图片
def download_image(request):
    # 获取目标图片 URL
    img_url = request.GET.get('imgUrl')
    # 使用 requests 库获取图片数据
    response = requests.get(img_url, stream=True)
    # 创建并返回一个 Django FileResponse
    return FileResponse(response.raw, content_type='image/jpeg')




# 获取某个图库下的相册
def get_album_list(request):
    gallery = Gallery.objects.get(id=request.GET.get("galleryId"))
    albums = Album.objects.filter(gallery=gallery).order_by("-id")
    albumList = []
    for album in albums:
        albumInfo = album.get_json()
        imageList = []
        # 添加相册包含的图片列表
        images = Image.objects.filter(album=album).exclude(status="delete").order_by("-id")
        for image in images:
            imageList.append(image.get_json())

        albumInfo["imageList"] = imageList
        albumList.append(albumInfo)
    return SuccessResponse(albumList)

# 获取单个相册信息
def get_album(request):
    album = Album.objects.get(id=request.params["album_id"])
    return SuccessResponse(album.get_json())

# 创建相册
def create_album(request):
    # 如果图库下存在一个同名相册，就返回这个相册的信息
    gallery = Gallery.objects.get(id=request.params.get("gallery_id"))
    albums = Album.objects.filter(album_name=request.params.get("album_name"), gallery=gallery)
    for album in albums:
        return SuccessResponse(album.get_json())
    # 不存在同名相册，则创建相册
    album = Album()
    album.gallery = gallery
    album.album_name = request.params.get("album_name")
    album.title = request.params.get("title")
    album.desc = request.params.get("desc")
    album.image_num = 0
    album.status = "public"
    album.save()
    return SuccessResponse(album.get_json())

# 删除相册
def delete_album(request):
    Album.objects.get(id=request.GET.get("albumId")).delete()
    return SuccessResponse([])

# 更新相册
def update_album(request):
    album = Album.objects.get(id=request.params["id"])
    album.album_name = request.params["album_name"]
    album.title = request.params["title"]
    album.desc = request.params["desc"]
    album.save()
    return SuccessResponse(album.get_json())

# 搜索相册
def search_album(request):
    albums = Album.objects.filter(Q(title__contains=request.params.get('searchText')) | Q(album_name__contains=request.params.get('searchText')))
    albumList = []
    for album in albums:
        albumList.append(album.get_json())
    return SuccessResponse(albumList)

# 批量生成卡密
def gen_secret(request):
    params = json.loads(request.body.decode("utf-8"))

    try:
        num = int(params["num"])
        size = int(params["size"])
        expiration = int(params["expiration"])
        for i in range(num):
            secret = Secret()
            secret.user = User.objects.filter(username="dcgallery")[0]
            secret.secret = "dcgallery" + genRandomStr(9)
            secret.size = size
            secret.status = 'init'
            secret.expiration = expiration
            secret.save()
        return JsonResponse({
            "status": 'ok',
            "msg": '卡密生成成功',
            "code": 20000,
        })
    except:
        return JsonResponse({
            "status": 'fail',
            "msg": '数据异常',
            "code": 40000,
        })

# 获取卡密
def get_secret(request):
    secrets = Secret.objects.filter(status="init")
    data = []
    for secret in secrets:
        data.append({
            "id": secret.id,
            "secret": secret.secret
        })
    return JsonResponse({
        "status": 'ok',
        "msg": '请求成功',
        "code": 20000,
        "data": data
    })

# 随机生成字符串
def genRandomStr(length):
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    random_str = ''
    for i in range(length):
        random_str += base_str[random.randint(0, len(base_str)-1)]
    return random_str

# 兑换卡密
def exchange_secret(request):
    params = json.loads(request.body.decode("utf-8"))
    token = request.headers.get("Authorization")[7:]
    jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
    payload = jwt_decode_handler(token)
    user = User.objects.filter(username=payload.get('username'))[0]
    secrets = Secret.objects.filter(secret=params["secret"], status='init')
    for secret in secrets:
        # 更改图库有效期
        galleries = Gallery.objects.filter(user=user)
        for gallery in galleries:
            gallery.expired_time = gallery.expired_time + datetime.timedelta(days=secret.expiration)
            gallery.total_memory = gallery.total_memory + secret.size
            gallery.save()
            secret.user=user
            secret.status = "bound"
            secret.save()
            return JsonResponse({
                "status": 'ok',
                "msg": '卡密兑换成功',
                "code": 20000,
            })

    return JsonResponse({
        "status": 'fail',
        "msg": '卡密无效',
        "code": 40000,
    })
