from robot.models import WxImage, WxSdtask, WxMjtask, Config, LarkMjtask, LarkSdtask, LarkBotInfo
from gallery.models import Image, Album, Gallery
from configs.settings import COS_CONFIG
from utils.lark_utils import LarkRobot
from utils.gpt_utils import ChatGpt
from utils.entities import cos, bdtrans, sd, gpts, ali
import json, requests, os, re, time
import PIL.Image as pImage
from mutagen.oggopus import OggOpus

# 飞书机器人消息处理总入口
def handler_lark_msg(params):
    # 解析请求体
    try:
        msg_type = params["event"]["msg_type"]
        if msg_type == "text":
            handler_lark_text_msg(params)

        if msg_type == "image":
            handler_lark_image_msg(params)

        if msg_type == "audio":
            handler_lark_audio_msg(params)

        if msg_type == "media":
            handler_lark_media_msg(params)

        if msg_type == "sticker":
            handler_lark_sticker_msg(params)

        if msg_type == "post":
            handler_lark_post_msg(params)
    except:
        return None

# 文本消息处理
def handler_lark_text_msg(params):
    # 获取文本信息
    app_id = params["event"]["app_id"]
    open_id = params["event"]["open_id"]
    open_chat_id = params["event"]["open_chat_id"]
    text_without_at_bot = params["event"]["text_without_at_bot"]
    # 获取机器人信息
    larkBotInfo = LarkBotInfo.objects.get(app_id=app_id)
    larkRobot = LarkRobot(larkBotInfo.app_id, larkBotInfo.app_secret)

    if "sd" in larkBotInfo.type:
        sd_config = larkBotInfo.extra_config["sd_config"]
        print(sd_config)
        # 帮助命令
        if text_without_at_bot.strip().startswith(sd_config["help_command"]):
            larkRobot.sendRichtextToChat(
                chat_id=open_chat_id,
                rich_text={
                    "content": [
                        [
                            {
                                "tag": "text",
                                "un_escape": True,
                                "text": sd_config["help_text"]
                            }
                        ]
                    ]
                }
            )
            return None
        # sd 生图逻辑
        elif text_without_at_bot.lstrip().startswith("/sd"):
            larkSdtask = LarkSdtask()
            # 任务基础信息
            larkSdtask.lark_msg = text_without_at_bot.replace("/sd", "").strip()
            larkSdtask.lark_app_id = app_id
            larkSdtask.open_id = open_id
            larkSdtask.open_chat_id = open_chat_id
            larkSdtask.status = "init"

            # 根据微信消息内容，创建sd任务，首先检测是否包含链接
            url_list = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', larkSdtask.lark_msg)
            params = {}

            print(url_list)
            if len(url_list) == 0:
                # 无链接，走文生图逻辑
                larkSdtask.type = "txt2img"

                # 模版选择
                if "--template" in larkSdtask.lark_msg:
                    # 有模版的逻辑
                    custom_configs = larkSdtask.lark_msg.split('--')
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
                params["prompt"] = bdtrans.translate(larkSdtask.lark_msg.split('--')[0]).get("result").get('trans_result')[0]['dst'] + params["prompt"]

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
                if "--template" in larkSdtask.lark_msg:
                    # 有模版的逻辑
                    custom_configs = larkSdtask.lark_msg.split('--')
                    for custom_config in custom_configs:
                        # 找到自定义配置中的模版
                        if custom_config.startswith("template"):
                            key = custom_config.replace("template", "").strip()
                            bot_config = Config.objects.get(key=key)
                            if bot_config == None:
                                bot_config = Config.objects.get(key="default", type="template_sd_img2img")
                            larkSdtask.type = "img2img" if bot_config.type == "template_sd_img2img" else "txt2img"
                            params = bot_config.content
                else:
                    bot_config = Config.objects.get(key="default", type="template_sd_img2img")
                    larkSdtask.type = "img2img"
                    params = bot_config.content

                # 设置图片数据
                if larkSdtask.type == "img2img":
                    params["init_images"] = [image_data]
                if larkSdtask.type == "txt2img":
                    params["alwayson_scripts"]["ControlNet"]["args"][0]["image"] = image_data

                # 设置宽高
                if params.get("width") == None:
                    params["width"] = width
                    params["height"] = height
                if len(larkSdtask.lark_msg.split('--')[0].replace(image_url, "").strip()) == 0:
                    pass
                else:
                    # 提示词处理
                    params["prompt"] = bdtrans.translate(larkSdtask.lark_msg.split('--')[0].replace(image_url, "").strip()).get("result").get('trans_result')[0]['dst'] + params["prompt"]

            elif len(url_list) == 2:
                # 2个图片链接，走融图逻辑
                larkSdtask.type = "txt2imgByCN"
                pass

            # 参数处理
            if "--" in larkSdtask.lark_msg:
                configs = larkSdtask.lark_msg.split('--')
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

            larkSdtask.params = json.loads(json.dumps(params))
            larkSdtask.save()
            larkRobot.sendRichtextToChat(
                chat_id=open_chat_id,
                rich_text={
                    "content": [
                        [
                            {
                                "tag": "at",
                                "user_id": open_id
                            },
                            {
                                "tag": "text",
                                "un_escape": True,
                                "text": "\n🚀SD画图任务已经创建\n🌟任务 ID：{}".format(larkSdtask.id)
                            }
                        ]
                    ]
                }
            )

            return None

    if "mj" in larkBotInfo.type:
        mj_config = larkBotInfo.extra_config["mj_config"]
        if text_without_at_bot.strip().startswith(mj_config["help_command"]):
            larkRobot.sendRichtextToChat(
                chat_id=open_chat_id,
                rich_text={
                    "content": [
                        [
                            {
                                "tag": "text",
                                "un_escape": True,
                                "text": mj_config["help_text"]
                            }
                        ]
                    ]
                }
            )

    if "gpt" in larkBotInfo.type:
        gpt_config = larkBotInfo.extra_config["gpt_config"]
        # 给对应群聊添加 gpt
        if gpts.get(open_chat_id) == None:
            gpts[open_chat_id] = ChatGpt(
                base_url=gpt_config["base_url"],
                api_key=gpt_config["api_key"],
                model=gpt_config["model"],
                open_history=True
            )
        # 清理记忆
        if text_without_at_bot.strip() == "记忆清除":
            gpts[open_chat_id] = None
            larkRobot.sendRichtextToChat(
                chat_id=open_chat_id,
                rich_text={
                    "content": [
                        [
                            {
                                "tag": "text",
                                "un_escape": True,
                                "text": "记忆已清理"
                            }
                        ]
                    ]
                }
            )
            return None
        # 帮助命令
        if text_without_at_bot.strip().startswith(gpt_config["help_command"]):
            larkRobot.sendRichtextToChat(
                chat_id=open_chat_id,
                rich_text={
                    "content": [
                        [
                            {
                                "tag": "text",
                                "un_escape": True,
                                "text": gpt_config["help_text"]
                            }
                        ]
                    ]
                }
            )
            return None
        # multi_mode 多模态枚举：0 文本回答；1 语音回答；2 待定；10 自动识别意图
        # 文本回复
        if gpt_config["multi_mode"] == 0:
            answer = gpts[open_chat_id].chatCompletions({
                "role": "user",
                "content": text_without_at_bot
            })
            larkRobot.sendRichtextToChat(
                chat_id=open_chat_id,
                rich_text={
                    "content": [
                        [
                            {
                                "tag": "text",
                                "un_escape": True,
                                "text": answer
                            }
                        ]
                    ]
                }
            )
            return None
        # 语音回复
        if gpt_config["multi_mode"] == 1:
            answer = gpts[open_chat_id].chatCompletions({
                "role": "user",
                "content": text_without_at_bot
            })
            audio_filename = "{}.opus".format(str(int(time.time())))
            audio_filepath = os.path.join("/tmp", audio_filename)
            gpts[open_chat_id].audioSpeech(text=answer, audiopath=audio_filepath)

            larkRobot.sendAudioToChat(
                file_key=larkRobot.uploadAudio(
                    filename=audio_filename,
                    filepath=audio_filepath,
                    duration=str(int(1000 * OggOpus(audio_filepath).info.length))
                )["data"]["file_key"],
                chat_id=open_chat_id
            )
            return None
        # todo 意图识别

# 语音消息处理
def handler_lark_audio_msg(params):
    # 获取文本信息
    app_id = params["event"]["app_id"]
    audio_key = params["event"]["audio_key"]
    open_message_id = params["event"]["open_message_id"]
    open_chat_id = params["event"]["open_chat_id"]
    # 获取机器人信息
    larkBotInfo = LarkBotInfo.objects.get(app_id=app_id)
    larkRobot = LarkRobot(larkBotInfo.app_id, larkBotInfo.app_secret)

    if "gpt" in larkBotInfo.type:
        gpt_config = larkBotInfo.extra_config["gpt_config"]
        # 给对应群聊添加 gpt
        if gpts.get(open_chat_id) == None:
            gpts[open_chat_id] = ChatGpt(
                base_url=gpt_config["base_url"],
                api_key=gpt_config["api_key"],
                model=gpt_config["model"],
                open_history=True
            )

        # 语音转文本
        opus_audio_filepath = "/tmp/{}.opus".format(str(int(time.time())))
        mp3_audio_filepath = "/tmp/{}.mp3".format(str(int(time.time())))
        with open(opus_audio_filepath, 'wb') as audio_file:
            audio_file.write(larkRobot.getMessageAudio(open_message_id, audio_key).content)
        os.system("ffmpeg -i {} -ar 8000 {}".format(opus_audio_filepath, mp3_audio_filepath))
        # 将文件上传到存储桶中
        oss_audio_url = cos.get_url(
            bucket=COS_CONFIG["bucket"],
            key=cos.upload_file(
                bucket=COS_CONFIG["bucket"],
                key="imgbuilder/{}{}".format("public", mp3_audio_filepath),
                local_path=mp3_audio_filepath
            )
        )
        text_without_at_bot = ali.fileTrans(oss_audio_url)["Result"]["Sentences"][0]["Text"]
        # 使用语音进行回答
        answer = gpts[open_chat_id].chatCompletions({
            "role": "user",
            "content": text_without_at_bot
        })
        audio_filename = "{}.opus".format(str(int(time.time())))
        audio_filepath = os.path.join("/tmp", audio_filename)
        gpts[open_chat_id].audioSpeech(text=answer, audiopath=audio_filepath)
        larkRobot.sendAudioToChat(
            file_key=larkRobot.uploadAudio(
                filename=audio_filename,
                filepath=audio_filepath,
                duration=str(int(1000 * OggOpus(audio_filepath).info.length))
            )["data"]["file_key"],
            chat_id=open_chat_id
        )
        return None

# 图片消息处理
def handler_lark_image_msg(params):
    # 查询机器人信息

    # 查询
    pass

def handler_lark_media_msg(params):
    pass

def handler_lark_sticker_msg(params):
    pass

def handler_lark_post_msg(params):
    pass

def execute_lark_mj_task():
    return None

# 执行 sd 生图任务
def execute_lark_sd_task():
    larkSdtasks = LarkSdtask.objects.filter(status="init")
    for larkSdtask in larkSdtasks:
        # 获取机器人信息
        larkBotInfo = LarkBotInfo.objects.get(app_id=larkSdtask.lark_app_id)
        album = get_album(larkBotInfo.user, "stable diffusion")
        larkRobot = LarkRobot(larkBotInfo.app_id, larkBotInfo.app_secret)
        # 根据任务类型执行操作，枚举见 model
        if larkSdtask.type == "txt2img":
            filename = "{}.png".format(str(int(time.time())))
            target_filepath = os.path.join("/tmp", filename)
            # 执行文生图，并保存到本地
            sd.image_data_to_file(
                sd.txt2img(params=larkSdtask.params)["images"][0],
                target_filepath
            )
            # 上传并保存图片
            oss_image_url = cos.get_url(
                bucket=COS_CONFIG["bucket"],
                key=cos.upload_file(
                    bucket=COS_CONFIG["bucket"],
                    key="imgbuilder/{}/{}/{}".format(larkSdtask.id, str(int(time.time())), filename),
                    local_path=target_filepath
                )
            )
            # 保存生成的图片信息
            image = Image()
            image.album = album
            image.url = oss_image_url
            image.width = larkSdtask.params["width"]
            image.height = larkSdtask.params["height"]
            image.tag = "sdtxt2img"
            image.status = "public"
            image.save()
            # 更改任务状态
            larkSdtask.status = "done"
            larkSdtask.image_url = oss_image_url
            image_key = larkRobot.uploadImage(target_filepath)["data"]["image_key"]
            larkSdtask.save()

            # 上传图片
            larkRobot.sendRichtextToChat(
                chat_id=larkSdtask.open_chat_id,
                rich_text={
                    "content": [
                        [
                            {
                                "tag": "at",
                                "user_id": larkSdtask.open_id
                            },
                            {
                                "tag": "text",
                                "un_escape": True,
                                "text": "\n✅任务已经完成\n🌟任务 ID：{}\n✨作品已自动存储到图库中\n🔗图片链接：{}".format(
                                    larkSdtask.id,
                                    oss_image_url
                                )
                            },
                            {
                                "tag": "img",
                                "image_key": image_key
                            }
                        ]
                    ]
                }
            )
        if larkSdtask.type == "img2img":
            filename = "{}.png".format(str(int(time.time())))
            target_filepath = os.path.join("/tmp", filename)
            # 执行文生图，并保存到本地
            sd.image_data_to_file(
                sd.img2img(params=larkSdtask.params)["images"][0],
                target_filepath
            )
            # 上传并保存图片
            oss_image_url = cos.get_url(
                bucket=COS_CONFIG["bucket"],
                key=cos.upload_file(
                    bucket=COS_CONFIG["bucket"],
                    key="imgbuilder/{}/{}/{}".format(larkSdtask.id, str(int(time.time())), filename),
                    local_path=target_filepath
                )
            )
            # 保存生成的图片信息
            image = Image()
            image.album = album
            image.url = oss_image_url
            image.width = larkSdtask.params["width"]
            image.height = larkSdtask.params["height"]
            image.tag = "sdimg2img"
            image.status = "public"
            image.save()
            # 更改任务状态
            larkSdtask.status = "done"
            larkSdtask.image_url = oss_image_url
            larkSdtask.save()

    return None

# 获取相册
def get_album(user, album_name):
    gallery = Gallery.objects.get(user=user)
    album = Album.objects.get(gallery=gallery, album_name=album_name)
    return album