from configs.settings import COS_CONFIG, SD_CONFIG, BD_TRANS_CONFIG, MJ_CONFIG, INTENT_DETECT_CONFIG, GPT_CONFIG, SUMMARY_GPT_CONFIG
from utils.trans_utils import BaiduTranslate
from utils.mj_utils import Sender, Receiver
from utils.oss_utils import Cos
from utils.sd_utils import SD
from utils.ali_utils import AliVoiceRecog
from utils.gpt_utils import ChatGpt

# 项目内置依赖实例化
cos = Cos(
    secret_id=COS_CONFIG['secret_id'],
    secret_key=COS_CONFIG['secret_key'],
    region=COS_CONFIG['region']
)
sd = SD(
    baseurl=SD_CONFIG['baseurl'],
    username=SD_CONFIG['username'],
    password=SD_CONFIG['password']
)
bdtrans = BaiduTranslate(
    appId=BD_TRANS_CONFIG["appId"],
    apiKey=BD_TRANS_CONFIG["apiKey"],
    secretKey=BD_TRANS_CONFIG["secretKey"]
)
mjsender = Sender(
    authorization=MJ_CONFIG["authorization"],
    channel_id=MJ_CONFIG["channel_id"],
    application_id=MJ_CONFIG["application_id"],
    guild_id=MJ_CONFIG["guild_id"],
    session_id=MJ_CONFIG["session_id"],
    version=MJ_CONFIG["version"],
    id=MJ_CONFIG["id"],
    flags=MJ_CONFIG["flags"],
    proxy=MJ_CONFIG["proxy"]
)
mjreceiver = Receiver(
    channel_id=MJ_CONFIG["channel_id"],
    authorization=MJ_CONFIG["authorization"],
    proxy=MJ_CONFIG["proxy"]
)
gpt = ChatGpt(
    base_url=GPT_CONFIG["base_url"],
    api_key=GPT_CONFIG["api_key"],
    system_message=GPT_CONFIG["system_message"],
    model=GPT_CONFIG["model"]
)
id_gpt = ChatGpt(
    base_url=INTENT_DETECT_CONFIG["base_url"],
    api_key=INTENT_DETECT_CONFIG["api_key"],
    system_message=INTENT_DETECT_CONFIG["system_message"],
    model=INTENT_DETECT_CONFIG["model"]
)
summary_gpt = ChatGpt(
    base_url=SUMMARY_GPT_CONFIG["base_url"],
    api_key=SUMMARY_GPT_CONFIG["api_key"],
    system_message=SUMMARY_GPT_CONFIG["system_message"],
    model=SUMMARY_GPT_CONFIG["model"]
)

gpts = {
    "summary_gpt": summary_gpt
}
ali = AliVoiceRecog()
