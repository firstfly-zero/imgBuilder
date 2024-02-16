from handler.wechat import WeixinMjRobot
from config import conf, load_config
from common.log import logger
import time

def run():
    try:
        load_config()
        wx_mj_robot = WeixinMjRobot()
        wx_mj_robot.start()

    except Exception as e:
        logger.error("App startup failed!")
        logger.exception(e)

def timed_function():
    while True:
        print("This function runs independently from the main process.")
        time.sleep(5)  # The function will wait for 5 seconds between prints



if __name__ == '__main__':
    run()