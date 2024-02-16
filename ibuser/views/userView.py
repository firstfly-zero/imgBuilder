import json
from django.contrib.auth import authenticate
from rest_framework_jwt.settings import api_settings
from ibuser.models import IBUser, IBVerificationCode, IBUserShare, IBUserInviter
from configs.base import SuccessResponse, FailureResponse
from gallery.models import Gallery, Album, Image
from robot.models import WxMjtask, WxSdtask
from ibuser.services.userService import send_verification_email, generate_verification_code
from datetime import datetime, timedelta
from django.db.models import Q

# 发送验证码，后期再考虑使用 redis
def verify(request):
    try:
        email = request.params.get("email")
        code = generate_verification_code()
        if "@" not in email:
            return FailureResponse("邮箱格式错误")
        IBVerificationCode.objects.create(
            email=email,
            code=code,
            status='valid'
        )
        send_verification_email(
            email=email,
            code=code
        )
        return SuccessResponse("验证码发送成功")
    except:
        return FailureResponse("验证码发送失败")

# 注册
def register(request):
    try:
        username = request.params.get("username")
        password = request.params.get("password")
        email = request.params.get("email")
        code = request.params.get("code")

        # 检查用户名是否被占用
        if len(IBUser.objects.filter(Q(username=username)|Q(email=email))) > 0:
            return FailureResponse('用户/邮箱已被注册')

        # 检查验证码是否正确
        current_time = datetime.now()
        time_range = current_time - timedelta(minutes=10)
        iBVerificationCodes = IBVerificationCode.objects.filter(email=email, code=code, status="valid", create_time__gte=time_range)
        if len(iBVerificationCodes) == 0:
            return FailureResponse('验证码已过期')
        for iBVerificationCode in iBVerificationCodes:
            iBVerificationCode.status = "invalid"
            iBVerificationCode.save()

        # 创建用户及对应的图库及默认相册
        iBUser = IBUser.objects.create_user(
            username=username,
            password=password,
            email=email,
            avatar="https://aiclub-1311445709.cos.ap-guangzhou.myqcloud.com/imgbuilder/80/1706088211/tmp/1706088211004.png"
        )
        gallery = Gallery.objects.create(
            user=iBUser,
            gallery_name=iBUser.username
        )
        Album.objects.create(
            gallery=gallery,
            album_name="midjourney",
            title="midjourney",
            desc="midjourney 默认相册，删除后无法使用 Midjourney 生图"
        )
        Album.objects.create(
            gallery=gallery,
            album_name="stable diffusion",
            title="stable diffusion",
            desc="stable diffusion 默认相册，删除后无法使用 stable diffusion 生图"
        )
        return SuccessResponse("注册成功")
    except:
        return FailureResponse('用户创建失败')

# 登录
def login(request):
    try:
        username = request.params.get('username')
        password = request.params.get('password')

        return SuccessResponse({
            'token': api_settings.JWT_ENCODE_HANDLER(api_settings.JWT_PAYLOAD_HANDLER(authenticate(request, username=username, password=password)))
        })
    except:
        return FailureResponse('数据异常')

# 获取用户信息
def info(request):
    user = IBUser.objects.get(username=request.username)
    from_users = IBUserInviter.objects.filter(user=user)
    invite_users = IBUserInviter.objects.filter(inviter=user)

    gallery = Gallery.objects.get(user=user)
    albums = Album.objects.filter(gallery=gallery)
    album_list = []
    for album in albums:
        album_list.append(album.get_json())

    return SuccessResponse({
        "accountId": user.id,
        "name": user.username,
        "avatar": user.avatar,
        "role": user.role,
        "email": user.email,
        "albumList": album_list,
        "galleryId": Gallery.objects.get(user=user).id,
        "registrationDate": user.create_time.strftime("%Y年%m月%d日%H:%M"),
        "inviter": None if len(from_users)==0 else from_users[0].inviter.username,
        "inviteNum": len(invite_users),
        "certification": 1,
        "job": "qa",
        "jobName": '质量管理大师',
        "organization": 'Quality',
        "organizationName": '测开',
        "location": 'beijing',
        "locationName": '北京',
        "introduction": '人潇洒，性温存',
        "personalWebsite": 'https://www.arco.design',
        "phone": '1',
    })

# 更新用户邀请人信息
def update_inviter(request):
    user = IBUser.objects.get(username=request.username)
    inviter = IBUser.objects.get(username=request.params.get("inviter"))

    inviterInfos = IBUserInviter.objects.filter(user=user)
    if len(inviterInfos) == 0:
        # 创建
        IBUserInviter.objects.create(
            user=user,
            inviter=inviter
        )
        # 更改用户与邀请者的 VIP 等级
        user.role = "userVip1"
        inviter.role = "userVip2"
        user.save()
        inviter.save()
    else:
        for inviterInfo in inviterInfos:
            inviterInfo.inviter = inviter
            inviterInfo.save()

    return SuccessResponse("更新成功")

# 更新用户信息
def update(request):
    return SuccessResponse("")

# 退出登录
def logout(request):
    return SuccessResponse("")

# 创建用户分享
def create_share(request):
    # 获取分享类型
    share_type = request.params.get("share_type")
    iBUserShare = IBUserShare()
    iBUserShare.user = IBUser.objects.get(username=request.username)

    if share_type == None:
        return FailureResponse("请传入分享类型")

    # 获取分享内容
    if share_type == "image":
        image_url = request.params.get("image_url")
        # 检查是否是 mj 任务
        wxMjtasks = WxMjtask.objects.filter(oss_image_url=image_url)
        if len(wxMjtasks) > 0:
            wxMjtask = wxMjtasks[0]
            iBUserShare.share_type = "mjImage"
            iBUserShare.share_info = json.dumps({
                "image": image_url,
                "origin_prompt": wxMjtask.origin_prompt,
                "final_prompt": wxMjtask.final_prompt,
                "mj_image_url": wxMjtask.mj_image_url
            })
            iBUserShare.save()

        # 检查是否是 sd 任务
        wxSdtasks = WxSdtask.objects.filter(image_url=image_url)
        if len(wxSdtasks) > 0:
            wxSdtask = wxSdtasks[0]
            iBUserShare.share_type = "sdImage"
            iBUserShare.share_info = json.dumps({
                "image": image_url,
                "params": wxSdtask.params
            })
            iBUserShare.save()

        # 既不是 sd 又不是 mj，作为普通分享
        if len(wxMjtasks)==0 and len(wxSdtasks)==0:
            iBUserShare.share_type = "image"
            iBUserShare.share_info = json.dumps({
                "image": image_url
            })
            iBUserShare.save()

        return SuccessResponse({
            "share_id": iBUserShare.id
        })

    return SuccessResponse("")

# 获取用户分享信息
def get_share(request):
    share_id = request.GET.get("share_id")
    if share_id == None:
        return FailureResponse("请传入分享 id")

    iBUserShare = IBUserShare.objects.get(id=share_id)
    if iBUserShare == None:
        return FailureResponse("分享信息缺失")

    # 获取分享内容
    return SuccessResponse({
        "user": {
            "username": iBUserShare.user.username,
            "avatar": iBUserShare.user.avatar
        },
        "share": {
            "share_type": iBUserShare.share_type,
            "share_info": iBUserShare.share_info
        }
    })
