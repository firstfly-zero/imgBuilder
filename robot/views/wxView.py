from configs.settings import COS_CONFIG, SD_CONFIG, BD_TRANS_CONFIG, MJ_CONFIG, BASE_DIR, WORKSPACE, GPT_CONFIG
from configs.base import SuccessResponse, FailureResponse
from gallery.models import Album, Image, Gallery
from ibuser.models import IBUser
from robot.models import WxImage, WxSdtask, WxMjtask, Config
from utils.gpt_utils import ChatGpt
from utils.entities import cos, bdtrans, sd, gpts, ali, mjsender, mjreceiver
from django.db.models import F
from bs4 import BeautifulSoup
import PIL.Image as pImage
import os, time, re, json, requests, copy

# 对象存储初始化
default_params = {"prompt": "", "steps": 20, "seed": -1, "cfg_scale": 12, "batch_size": 1, "sampler_name": "Euler a", "negative_prompt": "(worst quality:2),(low quality:2),(normal quality:2),lowres,watermark,"}

# 添加微信机器人
def add_wx_bot(request):
    # 将机器人代码复制到对应的目录下
    time_now = str(int(time.time()))
    code_path = "{}wxbot{}".format(WORKSPACE, time_now)
    os.makedirs(code_path)
    os.system(
        "cp -r {} {}/".format(
            os.path.join(BASE_DIR, "static/wxbot/*"),
            code_path
        )
    )

    # 更改配置文件内容
    with open(os.path.join(code_path, "config.json"), 'w') as f:
        f.write(json.dumps(request.params, ensure_ascii=False))

    # 启动项目
    os.system("cd {} && nohup python3 app.py &".format(code_path))

    # 检查二维码是否生成
    wait_time=0
    wait_tag = True
    while wait_tag:
        wait_time=wait_time+1
        time.sleep(1)
        if os.path.exists(os.path.join(code_path, "QR.png")):
            wait_tag=False

    # 将文件中的内容返回给用户
    os.system("cp {} {}".format(
        os.path.join(code_path, "QR.png"),
        os.path.join(BASE_DIR, "static/wxbot{}.png".format(time_now))
    ))

    # 暂停 1s
    time.sleep(1)

    return SuccessResponse({
        "QRcode": "/static/wxbot{}.png".format(time_now)
    })

# 机器人上传图片
def upload_wximage(request):
    try:
        # 获取文件
        file = request.FILES['file']
        # 上传文件
        with open(os.path.join('/tmp', file.name), 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # 获取图片的宽和高
        img = pImage.open(os.path.join('/tmp', file.name))
        width, height = img.size

        # 将文件上传到存储桶中
        oss_image_url = cos.get_url(
            bucket=COS_CONFIG["bucket"],
            key=cos.upload_file(
                bucket=COS_CONFIG["bucket"],
                key="imgbuilder/{}/{}/{}".format("public", str(int(time.time())), file.name),
                local_path="/tmp/{}".format(file.name)
            )
        )

        wximage = WxImage()
        wximage.size = file.size / (1024 * 1024)
        wximage.url=oss_image_url
        wximage.from_user=request.POST.get("from_user")
        wximage.height=height
        wximage.width=width
        wximage.status="inited"
        wximage.save()
        return SuccessResponse({
            "id": wximage.id,
            "url": oss_image_url,
            "height": height,
            "width": width
        })
    except:
        return FailureResponse("数据异常")

# 机器人上传语音
def upload_wxvoice(request):
    # 获取文件
    file = request.FILES['file']
    # 上传文件
    with open(os.path.join('/tmp', file.name), 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    # 将文件上传到存储桶中
    voice_text = ali.fileTrans(cos.get_url(
        bucket=COS_CONFIG["bucket"],
        key=cos.upload_file(
            bucket=COS_CONFIG["bucket"],
            key="voice/{}/{}".format(str(int(time.time())), file.name),
            local_path=os.path.join('/tmp', file.name)
        )
    ))["Result"]["Sentences"][0]["Text"]

    response = requests.request(
        method="POST",
        url="https://api.dify.ai/v1/chat-messages",
        headers={
            'Authorization': 'Bearer app-VTmbSFD5E43bVcno0lB6KNnv',
            'Content-Type': 'application/json'
        }, json={
            "inputs": {},
            "query": voice_text,
            "response_mode": "blocking",
            "conversation_id": "",
            "user": "abc-123"
        })

    return SuccessResponse(response.json()["answer"])

# 将图片移动到指定相册
def move_wximage_to_album(request):
    # 获取相册
    album = Album.objects.get(album_name=request.params.get("album_name") if request.params.get("album_name")!="" else "default")
    wxImage = WxImage.objects.filter(from_user=request.params.get("from_user")).order_by(F("create_time").desc(nulls_last=True)).first()

    if wxImage != None:
        image = Image()
        image.album = album
        image.url = wxImage.url
        image.height = wxImage.height
        image.width = wxImage.width
        image.tag = "wxupload"
        image.status = "public"
        image.save()
        imageInfo = image.get_json()
        imageInfo["head_msg"] = Config.objects.get(key="head_msg").value if Config.objects.get(key="head_msg").value != None else ""
        imageInfo["tail_msg"] = Config.objects.get(key="tail_msg").value if Config.objects.get(key="tail_msg").value != None else ""
        return SuccessResponse(imageInfo)
    else:
        return FailureResponse("数据异常")

# 获取微信机器人默认配置
def get_wxbot_default_config(request):
    return SuccessResponse(Config.objects.get(key="config_wxbot_default").content)

# 创建微信sd任务
def create_wx_sd_task(request):
    user = IBUser.objects.get(username=request.params.get("ib_username"))
    if user == None:
        return SuccessResponse({
            "head_msg": Config.objects.get(key="head_msg").value if Config.objects.get(key="head_msg").value != None else "",
            "tail_msg": Config.objects.get(key="tail_msg").value if Config.objects.get(key="tail_msg").value != None else "",
            "id": "请注册用户后重试"
        })

    wxSdtask = WxSdtask()
    wxSdtask.user = user
    # 任务基础信息
    wxSdtask.wx_msg = request.params.get("wx_msg")
    wxSdtask.wx_user_id = request.params.get("wx_user_id")
    wxSdtask.wx_nickname = request.params.get("wx_nickname")
    wxSdtask.wx_bot = request.params.get("wx_bot")
    wxSdtask.status = "init"
    # 根据微信消息内容，创建sd任务，首先检测是否包含链接
    url_list = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', wxSdtask.wx_msg)

    params = {}

    if len(url_list) == 0:
        # 无链接，走文生图逻辑
        wxSdtask.type = "txt2img"

        # 模版选择
        if "--template" in wxSdtask.wx_msg:
            # 有模版的逻辑
            custom_configs = wxSdtask.wx_msg.split('--')
            for custom_config in custom_configs:
                # 找到自定义配置中的模版
                if custom_config.startswith("template"):
                    key = custom_config.replace("template", "").strip()
                    bot_config = Config.objects.get(key=key)
                    if bot_config == None:
                        bot_config = Config.objects.get(key="default", type="template_sd_txt2img")
                    params = bot_config.content
        else:
            bot_config = Config.objects.get(key="default", type="template_sd_txt2img")
            params = bot_config.content
        # 预置尺寸
        if params.get("width") == None:
            params["width"] = 1024
            params["height"] = 1024
        # 提示词处理
        params["prompt"] = bdtrans.translate(wxSdtask.wx_msg.split('--')[0]).get("result").get('trans_result')[0]['dst'] + params["prompt"]

    elif len(url_list) == 1:
        # 下载图片，并获取图片的 image_data
        image_url = url_list[0]
        respone = requests.get(image_url)
        filename = image_url.split("/")[-1]
        filepath = os.path.join("/tmp", filename)
        with open(filepath, 'wb') as image_file:
            image_file.write(respone.content)
        image_data = sd.file_to_image_data(filepath)
        width, height = pImage.open(filepath).size

        # 模版选择
        if "--template" in wxSdtask.wx_msg:
            # 有模版的逻辑
            custom_configs = wxSdtask.wx_msg.split('--')
            for custom_config in custom_configs:
                # 找到自定义配置中的模版
                if custom_config.startswith("template"):
                    key = custom_config.replace("template", "").strip()
                    bot_config = Config.objects.get(key=key)
                    if bot_config == None:
                        bot_config = Config.objects.get(key="default", type="template_sd_img2img")
                    wxSdtask.type = "img2img" if bot_config.type == "template_sd_img2img" else "txt2img"
                    params = bot_config.content
        else:
            bot_config = Config.objects.get(key="default", type="template_sd_img2img")
            wxSdtask.type = "img2img"
            params = bot_config.content

        # 设置图片数据
        if wxSdtask.type == "img2img":
            params["init_images"] = [image_data]
        if wxSdtask.type == "txt2img":
            params["alwayson_scripts"]["ControlNet"]["args"][0]["image"] = image_data

        # 设置宽高
        if params.get("width") == None:
            params["width"] = width
            params["height"] = height
        if len(wxSdtask.wx_msg.split('--')[0].replace(image_url, "").strip()) == 0:
            pass
        else:
            # 提示词处理
            params["prompt"] = bdtrans.translate(wxSdtask.wx_msg.split('--')[0].replace(image_url, "").strip()).get("result").get('trans_result')[0]['dst'] + params["prompt"]

    elif len(url_list) == 2:
        # 2个图片链接，走融图逻辑
        wxSdtask.type = "txt2imgByCN"
        pass

    # 参数处理
    if "--" in wxSdtask.wx_msg:
        configs = wxSdtask.wx_msg.split('--')
        for config in configs:
            # 宽高比逻辑
            if config.startswith("ar"):
                try:
                    args = config.lower().replace("ar", "").replace("：", ":").replace(" ", "").split(":")
                    # 宽度固定 1024
                    params["width"] = 1024
                    params["height"] = int(1024 * int(args[1]) / int(args[0]))
                except:
                    params["width"] = 1024
                    params["height"] = 1024
            # 随机种子逻辑
            if config.startswith("seed"):
                try:
                    params["seed"] = int(config.replace("seed", ""))
                except:
                    params["seed"] = -1
            # 采样器逻辑
            if config.startswith("sampler"):
                try:
                    params["sampler_name"] = config.replace("sampler", "").strip()
                except:
                    params["sampler_name"] = "DPM++ SDE Karras"

    wxSdtask.params = json.loads(json.dumps(params))
    wxSdtask.save()
    taskInfo = wxSdtask.get_json()
    taskInfo["head_msg"] = Config.objects.get(key="head_msg").value if Config.objects.get(key="head_msg").value != None else ""
    taskInfo["tail_msg"] = Config.objects.get(key="tail_msg").value if Config.objects.get(key="tail_msg").value != None else ""
    return SuccessResponse(taskInfo)

# 执行微信sd任务
def execute_wx_sd_task(request):
    wxSdtasks = WxSdtask.objects.filter(status="init")
    for wxSdtask in wxSdtasks:
        album = get_album(
            username=wxSdtask.user.username,
            album_name="stable diffusion"
        )
        # 根据任务类型执行操作，枚举见 model
        if wxSdtask.type == "txt2img":
            filename = "{}.png".format(str(int(time.time())))
            target_filepath = os.path.join("/tmp", filename)
            # 执行文生图，并保存到本地
            sd.image_data_to_file(
                sd.txt2img(params=wxSdtask.params)["images"][0],
                target_filepath
            )
            # 上传并保存图片
            oss_image_url = cos.get_url(
                bucket=COS_CONFIG["bucket"],
                key=cos.upload_file(
                    bucket=COS_CONFIG["bucket"],
                    key="imgbuilder/{}/{}/{}".format(wxSdtask.id, str(int(time.time())), filename),
                    local_path=target_filepath
                )
            )
            # 保存生成的图片信息
            image = Image()
            image.album = album
            image.url = oss_image_url
            image.width = wxSdtask.params["width"]
            image.height = wxSdtask.params["height"]
            image.tag = "sdtxt2img"
            image.status = "public"
            image.save()
            # 更改任务状态
            wxSdtask.status = "done"
            wxSdtask.image_url = oss_image_url
            wxSdtask.save()

        if wxSdtask.type == "img2img":
            filename = "{}.png".format(str(int(time.time())))
            target_filepath = os.path.join("/tmp", filename)
            # 执行文生图，并保存到本地
            sd.image_data_to_file(
                sd.img2img(params=wxSdtask.params)["images"][0],
                target_filepath
            )
            # 上传并保存图片
            oss_image_url = cos.get_url(
                bucket=COS_CONFIG["bucket"],
                key=cos.upload_file(
                    bucket=COS_CONFIG["bucket"],
                    key="imgbuilder/{}/{}/{}".format(wxSdtask.id, str(int(time.time())), filename),
                    local_path=target_filepath
                )
            )
            # 保存生成的图片信息
            image = Image()
            image.album = album
            image.url = oss_image_url
            image.width = wxSdtask.params["width"]
            image.height = wxSdtask.params["height"]
            image.tag = "sdimg2img"
            image.status = "public"
            image.save()
            # 更改任务状态
            wxSdtask.status = "done"
            wxSdtask.image_url = oss_image_url
            wxSdtask.save()

    return SuccessResponse("任务执行成功")

# 获取完成的微信sd任务
def get_done_wx_sd_task(request):
    doneList = []
    wxSdtasks = WxSdtask.objects.filter(status="done", wx_bot=request.params["wx_bot"])
    for wxSdtask in wxSdtasks:
        taskInfo = wxSdtask.get_json()
        taskInfo["head_msg"] = Config.objects.get(key="head_msg").value if Config.objects.get(key="head_msg").value != None else ""
        taskInfo["tail_msg"] = Config.objects.get(key="tail_msg").value if Config.objects.get(key="tail_msg").value != None else ""
        doneList.append(taskInfo)
        wxSdtask.status = "sent"
        wxSdtask.save()
    # todo 格式转换
    return SuccessResponse(doneList)

# 创建微信mj任务
def create_wx_mj_task(request):
    user = IBUser.objects.get(username=request.params.get("ib_username"))
    if user == None:
        return SuccessResponse({
            "head_msg": Config.objects.get(key="head_msg").value if Config.objects.get(key="head_msg").value != None else "",
            "tail_msg": Config.objects.get(key="tail_msg").value if Config.objects.get(key="tail_msg").value != None else "",
            "id": "请注册用户后重试"
        })

    wxMjtask = WxMjtask()
    wxMjtask.user = user
    # 任务基础信息
    wxMjtask.status = "init"
    wxMjtask.wx_msg = request.params["wx_msg"]
    wxMjtask.wx_user_id = request.params["wx_user_id"]
    wxMjtask.wx_nickname = request.params["wx_nickname"]
    wxMjtask.wx_bot = request.params["wx_bot"]
    wxMjtask.mj_done_msg = {}

    # 根据微信消息，构造传递给 mj 的数据
    if wxMjtask.wx_msg.startswith("/imagine"):
        wxMjtask.type = "imagine"
        # 生图逻辑
        url_list = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', wxMjtask.wx_msg)
        if len(url_list) == 0:
            # 无链接
            wxMjtask.origin_prompt = wxMjtask.wx_msg.replace("/imagine", "").strip()
            wxMjtask.final_prompt = bdtrans.translate(wxMjtask.origin_prompt.split("--")[0]).get("result").get('trans_result')[0]['dst'] + wxMjtask.origin_prompt.replace(wxMjtask.origin_prompt.split("--")[0], "")
        else:
            # 有链接
            origin_prompt_without_pic = wxMjtask.wx_msg.replace("/imagine", "").strip()
            # 将图片链接过滤掉再翻译
            for url in url_list:
                origin_prompt_without_pic = origin_prompt_without_pic.replace(url, "")
            wxMjtask.origin_prompt = wxMjtask.wx_msg.replace("/imagine", "").strip()
            wxMjtask.final_prompt = " ".join(url_list) + " " + bdtrans.translate(origin_prompt_without_pic.split("--")[0]).get("result").get('trans_result')[0]['dst'] + origin_prompt_without_pic.replace(origin_prompt_without_pic.split("--")[0], "")

    if wxMjtask.wx_msg.startswith("/up"):
        wxMjtask.type = "UVX"
        # 变换逻辑，origin_prompt 储存原始任务 id，final_prompt 储存变换类型
        up_info = re.sub(' +', ' ', wxMjtask.wx_msg.replace("/up", "").strip()).split(" ")
        wxMjtask.origin_prompt = "{}_{}".format(up_info[0], up_info[1])

        wxMjtask.final_prompt = WxMjtask.objects.get(id=up_info[0]).final_prompt

    wxMjtask.save()
    taskInfo = wxMjtask.get_json()
    taskInfo["head_msg"] = Config.objects.get(key="head_msg").value if Config.objects.get(key="head_msg").value != None else ""
    taskInfo["tail_msg"] = Config.objects.get(key="tail_msg").value if Config.objects.get(key="tail_msg").value != None else ""
    return SuccessResponse(taskInfo)

# 执行mj任务
def execute_wx_mj_task(request):
    # 发送 mj 消息
    init_wxMjtasks = WxMjtask.objects.filter(status="init")
    for init_wxMjtask in init_wxMjtasks:
        # 如果是生图任务
        if init_wxMjtask.type == "imagine":
            mjsender.send(init_wxMjtask.final_prompt)
            init_wxMjtask.status = "starting"
            init_wxMjtask.save()
        elif init_wxMjtask.type == "UVX":
            # 筛选原始任务
            origin_wxMjtask = WxMjtask.objects.get(id=init_wxMjtask.origin_prompt.split("_")[0])
            origin_mj_done_msg = json.loads(origin_wxMjtask.mj_done_msg)
            components = origin_mj_done_msg["components"][0]["components"] + origin_mj_done_msg["components"][1]["components"]
            for component in components:
                if component.get("label") == init_wxMjtask.origin_prompt.split("_")[1]:
                    mjsender.send_UVX(
                        message_id=origin_mj_done_msg["id"],
                        custom_id=component["custom_id"],
                        component_type=component["type"]
                    )
                    init_wxMjtask.status = "starting"
                    init_wxMjtask.save()
        else:
            continue

    # 获取 mj 消息
    mjreceiver.collecting_results()
    for df_id in mjreceiver.df.index:
        prompt = mjreceiver.df.loc[df_id][0]
        mj_image_url = mjreceiver.df.loc[df_id][2]
        mj_done_msg = mjreceiver.df.loc[df_id][5]

        # 过滤 mj_image_url 是否发送过，如果发送过，则跳过
        if len(WxMjtask.objects.filter(mj_image_url=mj_image_url)) != 0:
            continue

        if mjreceiver.df.loc[df_id][5].get('type') == 19 and ("Variations" in mj_done_msg['content'] or "Image #" in mj_done_msg['content']):
            if "Variations" in mj_done_msg['content']:
                v_starting_wxMjtasks = WxMjtask.objects.filter(status="starting", origin_prompt__contains="V")
                for v_starting_wxMjtask in v_starting_wxMjtasks:
                    album = get_album(
                        username=v_starting_wxMjtask.user.username,
                        album_name="midjourney"
                    )
                    if v_starting_wxMjtask.final_prompt.strip() in prompt:
                        # 将图片上传到图库
                        pic_res = requests.get(
                            url=mj_image_url,
                            proxies={'http': 'http://' + MJ_CONFIG["proxy"],
                                     'https': 'http://' + MJ_CONFIG["proxy"]} if MJ_CONFIG.get("proxy") else {},
                        )
                        png_file_path = "/tmp/{}.png".format(str(int(1000 * time.time())))
                        with open(png_file_path, "wb") as f:
                            f.write(pic_res.content)

                        width, height = pImage.open(png_file_path).size

                        oss_image_url = cos.get_url(
                            bucket=COS_CONFIG["bucket"],
                            key=cos.upload_file(
                                bucket=COS_CONFIG["bucket"],
                                key="imgbuilder/{}/{}{}".format(v_starting_wxMjtask.id, str(int(time.time())),
                                                                png_file_path),
                                local_path=png_file_path
                            )
                        )
                        # 保存生成的图片信息
                        image = Image()
                        image.album = album
                        image.url = oss_image_url
                        image.width = width
                        image.height = height
                        image.tag = "mjtxt2img"
                        image.status = "public"
                        image.save()

                        v_starting_wxMjtask.mj_image_url = mj_image_url
                        v_starting_wxMjtask.oss_image_url = oss_image_url
                        v_starting_wxMjtask.mj_done_msg = json.dumps(mj_done_msg)
                        v_starting_wxMjtask.status = "done"
                        v_starting_wxMjtask.save()

            else:
                u_starting_wxMjtasks = WxMjtask.objects.filter(status="starting", origin_prompt__contains="U")
                for u_starting_wxMjtask in u_starting_wxMjtasks:
                    album = get_album(
                        username=u_starting_wxMjtask.user.username,
                        album_name="midjourney"
                    )
                    if u_starting_wxMjtask.final_prompt.strip() in prompt and (mj_done_msg['content'].split("Image #")[1][0] in u_starting_wxMjtask.origin_prompt):
                        # 将图片上传到图库
                        pic_res = requests.get(
                            url=mj_image_url,
                            proxies={'http': 'http://' + MJ_CONFIG["proxy"],
                                     'https': 'http://' + MJ_CONFIG["proxy"]} if MJ_CONFIG.get("proxy") else {},
                        )
                        png_file_path = "/tmp/{}.png".format(str(int(1000 * time.time())))
                        with open(png_file_path, "wb") as f:
                            f.write(pic_res.content)

                        width, height = pImage.open(png_file_path).size

                        oss_image_url = cos.get_url(
                            bucket=COS_CONFIG["bucket"],
                            key=cos.upload_file(
                                bucket=COS_CONFIG["bucket"],
                                key="imgbuilder/{}/{}{}".format(u_starting_wxMjtask.id, str(int(time.time())),
                                                                png_file_path),
                                local_path=png_file_path
                            )
                        )
                        # 保存生成的图片信息
                        image = Image()
                        image.album = album
                        image.url = oss_image_url
                        image.width = width
                        image.height = height
                        image.tag = "mjtxt2img"
                        image.status = "public"
                        image.save()

                        u_starting_wxMjtask.mj_image_url = mj_image_url
                        u_starting_wxMjtask.oss_image_url = oss_image_url
                        u_starting_wxMjtask.mj_done_msg = json.dumps(mj_done_msg)
                        u_starting_wxMjtask.status = "done"
                        u_starting_wxMjtask.save()

        else:
            starting_wxMjtasks = WxMjtask.objects.filter(status="starting")
            for starting_wxMjtask in starting_wxMjtasks:
                album = get_album(
                    username=starting_wxMjtask.user.username,
                    album_name="midjourney"
                )
                if starting_wxMjtask.final_prompt.strip() in prompt:
                    # 将图片上传到图库
                    pic_res = requests.get(
                        url=mj_image_url,
                        proxies={'http': 'http://' + MJ_CONFIG["proxy"], 'https': 'http://' + MJ_CONFIG["proxy"]} if MJ_CONFIG.get("proxy") else {},
                    )
                    png_file_path = "/tmp/{}.png".format(str(int(1000 * time.time())))
                    with open(png_file_path, "wb") as f:
                        f.write(pic_res.content)

                    width, height = pImage.open(png_file_path).size

                    oss_image_url = cos.get_url(
                        bucket=COS_CONFIG["bucket"],
                        key=cos.upload_file(
                            bucket=COS_CONFIG["bucket"],
                            key="imgbuilder/{}/{}{}".format(starting_wxMjtask.id, str(int(time.time())), png_file_path),
                            local_path=png_file_path
                        )
                    )
                    # 保存生成的图片信息
                    image = Image()
                    image.album = album
                    image.url = oss_image_url
                    image.width = width
                    image.height = height
                    image.tag = "mjtxt2img"
                    image.status = "public"
                    image.save()

                    starting_wxMjtask.mj_image_url = mj_image_url
                    starting_wxMjtask.oss_image_url = oss_image_url
                    starting_wxMjtask.mj_done_msg = json.dumps(mj_done_msg)
                    starting_wxMjtask.status = "done"
                    starting_wxMjtask.save()

    return SuccessResponse("任务执行成功")

# 获取完成的微信mj任务
def get_done_wx_mj_task(request):
    doneList = []
    wxMjtasks = WxMjtask.objects.filter(wx_bot=request.params["wx_bot"], status="done")
    for wxMjtask in wxMjtasks:
        taskInfo = wxMjtask.get_json()
        taskInfo["head_msg"] = Config.objects.get(key="head_msg").value if Config.objects.get(key="head_msg").value != None else ""
        taskInfo["tail_msg"] = Config.objects.get(key="tail_msg").value if Config.objects.get(key="tail_msg").value != None else ""
        doneList.append(taskInfo)
        wxMjtask.status = "sent"
        wxMjtask.save()
    # todo 格式转换
    return SuccessResponse(doneList)

# gpt聊天
def get_wx_gpt_msg(request):
    ib_username = request.params.get("ib_username")
    wx_msg = request.params.get("wx_msg")
    wx_user_id = request.params.get("wx_user_id")
    wx_nickname = request.params.get("wx_nickname")
    wx_bot = request.params.get("wx_bot")
    if ib_username!=None:
        if gpts.get(wx_user_id) == None:
            gpts[wx_user_id] = ChatGpt(
                base_url=GPT_CONFIG["base_url"],
                api_key=GPT_CONFIG["api_key"],
                system_message=GPT_CONFIG["system_message"],
                model=GPT_CONFIG["model"],
                open_history=True
            )
        if wx_msg.startswith("/问"):
            return SuccessResponse({
                "head_msg": Config.objects.get(key="head_msg").value if Config.objects.get(key="head_msg").value != None else "",
                "answer": gpts[wx_user_id].chatCompletions({"role": "user", "content": wx_msg.replace("/问", "")}),
                "tail_msg": Config.objects.get(key="tail_msg").value if Config.objects.get(key="tail_msg").value != None else ""
            })

        elif wx_msg.startswith("/总结"):
            # 获取网页链接
            url_list = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', wx_msg)
            if len(url_list) > 0:
                try:
                    res = requests.request(
                        method="GET",
                        url=url_list[0]
                        # proxies={'http': 'http://' + MJ_CONFIG["proxy"], 'https': 'http://' + MJ_CONFIG["proxy"]} if MJ_CONFIG.get("proxy") else {},
                    )
                    return SuccessResponse({
                        "head_msg": Config.objects.get(key="head_msg").value if Config.objects.get(key="head_msg").value != None else "",
                        "answer": gpts["summary_gpt"].chatCompletions({"role": "user", "content": extract_text_from_html(res.text)}),
                        "tail_msg": Config.objects.get(key="tail_msg").value if Config.objects.get(key="tail_msg").value != None else ""
                    })
                except:
                    return SuccessResponse({
                        "head_msg": Config.objects.get(key="head_msg").value if Config.objects.get(key="head_msg").value != None else "",
                        "answer": "未能获取到内容，请联系管理员～",
                        "tail_msg": Config.objects.get(key="tail_msg").value if Config.objects.get(key="tail_msg").value != None else ""
                    })
            else:
                return SuccessResponse({
                    "head_msg": Config.objects.get(key="head_msg").value if Config.objects.get(key="head_msg").value != None else "",
                    "answer": "网页链接无效或未定义～",
                    "tail_msg": Config.objects.get(key="tail_msg").value if Config.objects.get(key="tail_msg").value != None else ""
                })

        else:
            return SuccessResponse("内容未定义")

    return SuccessResponse({
        "head_msg": Config.objects.get(key="head_msg").value if Config.objects.get(key="head_msg").value != None else "",
        "answer": "用户未定义，请联系管理员创建用户哦～",
        "tail_msg": Config.objects.get(key="tail_msg").value if Config.objects.get(key="tail_msg").value != None else ""
    })

def extract_text_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    # 移除脚本和样式标签
    for script in soup(["script", "style"]):
        script.extract()
    # 获取纯文本内容
    text = soup.get_text()
    # 去除多余的空行和空格
    lines = (line.strip() for line in text.splitlines())
    text = ' '.join(line for line in lines if line)
    return text

# 获取相册
def get_album(username, album_name):
    user = IBUser.objects.get(username=username)
    gallery = Gallery.objects.get(user=user)
    album = Album.objects.get(gallery=gallery, album_name=album_name)
    return album


