from django.urls import path
from robot.views import wxView
from robot.views import larkView

urlpatterns = [
    # 微信机器人
    # 机器人通用逻辑
    path("addWxBot", wxView.add_wx_bot),
    path("uploadWxImage", wxView.upload_wximage),
    path("uploadWxVoice", wxView.upload_wxvoice),
    path("moveWxImageToAlbum", wxView.move_wximage_to_album),
    path("getWxBotDefaultConfig", wxView.get_wxbot_default_config),
    # sd相关逻辑
    path("createWxSdTask", wxView.create_wx_sd_task),
    path("executeWxSdTask", wxView.execute_wx_sd_task),
    path("getDoneWxSdTask", wxView.get_done_wx_sd_task),
    # mj相关逻辑
    path("createWxMjTask", wxView.create_wx_mj_task),
    path("executeWxMjTask", wxView.execute_wx_mj_task),
    path("getDoneWxMjTask", wxView.get_done_wx_mj_task),
    # gpt相关逻辑
    path("getWxGptMsg", wxView.get_wx_gpt_msg),

    # 飞书机器人
    path("addLarkBot", larkView.add_lark_bot),
    path("larkBotListener", larkView.lark_bot_listener),
    path("executeLarkTask", larkView.execute_lark_task),

]