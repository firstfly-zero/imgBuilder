from configs.base import SuccessResponse, FailureResponse, JsonResponse
from robot.services.larkService import handler_lark_msg, execute_lark_sd_task, execute_lark_mj_task
from robot.models import LarkBotInfo
from ibuser.models import IBUser

# 添加飞书机器人
def add_lark_bot(request):
    user = IBUser.objects.get(username=request.username)
    larkBotInfos = LarkBotInfo.objects.filter(app_id=request.params.get("app_id"))
    if len(larkBotInfos) == 0:
        LarkBotInfo.objects.create(
            user=user,
            app_id=request.params.get("app_id"),
            app_secret=request.params.get("app_secret"),
            type="mj&sd&gpt",
            extra_config={
                "mj_config": {
                    "help_command": "/mjhelp",
                    "help_text": "[玫瑰]绘图机器人使用指南[玫瑰]\n------------------------------\n🎨 生成图片命令 \n输入: /imagine prompt\n<prompt> 即你提的绘画需求\n------------------------------\n🌈 变换图片命令 ️\n输入: /up asdf1234567 U1\n输入: /up asdf1234567 V1\n<asdf1234567> 代表消息ID，<U>代表放大，<V>代表细致变化，<1>代表第几张图\n------------------------------\n📕 附加参数\n1.解释：附加参数指的是在prompt后携带的参数，可以使你的绘画更加别具一格· 输入 /imagine prompt --v 5 --ar 16:9\n2.使用：需要使用--key value ，key和value之间需要空格隔开，每个附加参数之间也需要空格隔开\n3.详解：上述附加参数解释 <v>版本key <5>版本号 <ar>比例key，<16:9>比例value\n------------------------------\n📗 附加参数列表\n1.(--version) 或 (--v) 《版本》 参数 1，2，3，4，5 默认5，不可与niji同用\n2.(--niji)《卡通版本》 参数 空或 5 默认空，不可与版本同用\n3.(--aspect) 或 (--ar) 《横纵比》 参数 n:n ，默认1:1 ，不同版本略有差异，具体详见机器人提示\n4.(--chaos) 或 (--c) 《噪点》参数 0-100 默认0\n5.(--quality) 或 (--q) 《清晰度》参数 .25 .5 1 2 分别代表，一般，清晰，高清，超高清，默认1\n6.(--style) 《风格》参数 4a,4b,4c (v4)版本可用，参数 expressive,cute (niji5)版本可用\n7.(--stylize) 或 (--s)) 《风格化》参数 1-1000 v3 625-60000\n8.(--seed) 《种子》参数 0-4294967295 可自定义一个数值配合(sameseed)使用\n9.(--sameseed) 《相同种子》参数 0-4294967295 可自定义一个数值配合(seed)使用\n10.(--tile) 《重复模式》参数 空",
                },
                "sd_config": {
                    "help_command": "/sdhelp",
                    "help_text": "[玫瑰]绘图机器人使用指南[玫瑰]\n-------------------------------------\n[礼物] 使用方法[礼物]\n[庆祝]@机器人+图片ID+关键词+参数\n-------------------------------------\n📕 附加参数\n1.解释：附加参数指的是在prompt后携带的参数，可以使你的绘画更加别具一格\n2.使用：需要使用--key value ，key和value之间需要空格隔开，每个附加参数之间也需要空格隔开\n3.详解：上述附加参数解释<ar>比例key，<16:9>比例value\n-------------------------------------\n📕附加参数列表\n1.（--ar) 《宽高比》 格式： --ar16：9 ，默认1:1\n2.（--seed）《种子数》格式：--seed555648，默认-1，种子数值-1到无限大，-1等于随机生成一个种子数，种子数不同画图就不同。",
                },
                "gpt_config": {
                    "model": "gpt-3.5-turbo",
                    "api_key": "sk-BFeWGkbTkBi8SQDyIlccQBYJGeAGgNAbVZHbUoqzMn4h40x7",
                    "base_url": "https://api.chatanywhere.com.cn",
                    "help_text": "格式 @机器人 + 问题",
                    "multi_mode": 0,
                    "help_command": "/gpthelp"
                }
            }
        )
    else:
        for larkBotInfo in larkBotInfos:
            larkBotInfo.app_secret = request.params.get("app_secret")
            larkBotInfo.type = "mj&sd&gpt"
            larkBotInfo.user = user
            larkBotInfo.extra_config = {
                "mj_config": {
                    "help_command": "/mjhelp",
                    "help_text": "[玫瑰]绘图机器人使用指南[玫瑰]\n------------------------------\n🎨 生成图片命令 \n输入: /imagine prompt\n<prompt> 即你提的绘画需求\n------------------------------\n🌈 变换图片命令 ️\n输入: /up asdf1234567 U1\n输入: /up asdf1234567 V1\n<asdf1234567> 代表消息ID，<U>代表放大，<V>代表细致变化，<1>代表第几张图\n------------------------------\n📕 附加参数\n1.解释：附加参数指的是在prompt后携带的参数，可以使你的绘画更加别具一格· 输入 /imagine prompt --v 5 --ar 16:9\n2.使用：需要使用--key value ，key和value之间需要空格隔开，每个附加参数之间也需要空格隔开\n3.详解：上述附加参数解释 <v>版本key <5>版本号 <ar>比例key，<16:9>比例value\n------------------------------\n📗 附加参数列表\n1.(--version) 或 (--v) 《版本》 参数 1，2，3，4，5 默认5，不可与niji同用\n2.(--niji)《卡通版本》 参数 空或 5 默认空，不可与版本同用\n3.(--aspect) 或 (--ar) 《横纵比》 参数 n:n ，默认1:1 ，不同版本略有差异，具体详见机器人提示\n4.(--chaos) 或 (--c) 《噪点》参数 0-100 默认0\n5.(--quality) 或 (--q) 《清晰度》参数 .25 .5 1 2 分别代表，一般，清晰，高清，超高清，默认1\n6.(--style) 《风格》参数 4a,4b,4c (v4)版本可用，参数 expressive,cute (niji5)版本可用\n7.(--stylize) 或 (--s)) 《风格化》参数 1-1000 v3 625-60000\n8.(--seed) 《种子》参数 0-4294967295 可自定义一个数值配合(sameseed)使用\n9.(--sameseed) 《相同种子》参数 0-4294967295 可自定义一个数值配合(seed)使用\n10.(--tile) 《重复模式》参数 空",
                },
                "sd_config": {
                    "help_command": "/sdhelp",
                    "help_text": "[玫瑰]绘图机器人使用指南[玫瑰]\n-------------------------------------\n[礼物] 使用方法[礼物]\n[庆祝]@机器人+图片ID+关键词+参数\n-------------------------------------\n📕 附加参数\n1.解释：附加参数指的是在prompt后携带的参数，可以使你的绘画更加别具一格\n2.使用：需要使用--key value ，key和value之间需要空格隔开，每个附加参数之间也需要空格隔开\n3.详解：上述附加参数解释<ar>比例key，<16:9>比例value\n-------------------------------------\n📕附加参数列表\n1.（--ar) 《宽高比》 格式： --ar16：9 ，默认1:1\n2.（--seed）《种子数》格式：--seed555648，默认-1，种子数值-1到无限大，-1等于随机生成一个种子数，种子数不同画图就不同。",
                },
                "gpt_config": {
                    "model": "gpt-3.5-turbo",
                    "api_key": "sk-BFeWGkbTkBi8SQDyIlccQBYJGeAGgNAbVZHbUoqzMn4h40x7",
                    "base_url": "https://api.chatanywhere.com.cn",
                    "help_text": "格式 @机器人 + 问题",
                    "multi_mode": 0,
                    "help_command": "/gpthelp"
                }
            }
            larkBotInfo.save()

    return SuccessResponse("机器人添加成功")

# 飞书机器人监听方法
def lark_bot_listener(request):
    handler_lark_msg(params=request.params)
    if request.params.get("challenge"):
        return JsonResponse({
            "challenge": request.params.get("challenge")
        })
    return SuccessResponse("")

# 执行飞书机器人相关任务
def execute_lark_task(request):
    try:
        execute_lark_sd_task()
        execute_lark_mj_task()
        return SuccessResponse("执行成功")
    except:
        return FailureResponse("执行失败")






























