import datetime
import json
import random
import time
from enum import Enum

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from MyTools import Mail163
from Robot import BaseRobot


class UserOpt:

    def __init__(self, name, opt, count):
        self.name = name
        self.opt = opt
        self.count = count


class OptType(Enum):
    COMMON = "来了"
    CLICK = "点赞"
    FOLLOW = "关注"


class Djt(BaseRobot):

    def __init__(self):
        super().__init__("毒鸡汤", None, "https://djt.cool/", False)

    def get_djt(self):
        home_page = BeautifulSoup(self.driver.page_source, 'lxml')
        if not home_page:
            return "暂时没有鸡汤"
        text = home_page.find('p', attrs={'class', 'content-main'})
        self.driver.quit()
        return text.text


class DouyinRoomRobot(BaseRobot):
    __user_opt_list = {}

    def __init__(self, id):
        super().__init__('抖音', 'douyin', 'https://live.douyin.com/{}'.format(id))
        self.room_name = None
        self.is_welcome = True
        self.is_say_time = False

    def send(self, content, out=2):
        text_box = self.driver.find_element(By.CSS_SELECTOR, ".webcast-chatroom___textarea")
        if not text_box:
            return
        text_box.send_keys(content)
        send_button = self.driver.find_element(By.CSS_SELECTOR, ".webcast-chatroom___send-btn")
        send_button.click()
        print(content)
        time.sleep(out)

    def __check_max__(self, user, ty, max, context, is_send=True):
        if (user.opt and ty in user.opt) or ty is None:
            if user.count >= max:
                return
            user.count += 1
            if is_send:
                for one in context:
                    self.send(one)

    def __user_opt__(self, user_opt):
        # -----------------------------------------------------------------------------------
        # 用户的进入的操作
        element_user = user_opt.find_next('span', attrs={'class': 'rc30lnLh'})
        if not element_user:
            return
        opt_user = element_user.text
        opt_type = user_opt.find_next('span', attrs={'class': 'b76LkBHq'}).text
        user = opt_user.replace('：', '')
        opt_key = "{}-{}".format(user.strip(), opt_type.strip())
        if not self.__user_opt_list.get(opt_key):
            self.__user_opt_list[opt_key] = UserOpt(user, opt_type, 0)
        ############################################################################
        if OptType.COMMON.value in opt_type:
            self.__check_max__(self.__user_opt_list[opt_key], OptType.COMMON.value, 1,
                               ["欢迎“{}”大哥进入直播间[鼓掌][鼓掌][鼓掌]喜欢主播的可以点点关注哦[来看我]".format(
                                   user)])

        if OptType.CLICK.value in opt_type:
            self.__check_max__(self.__user_opt_list[opt_key], OptType.CLICK.value, 1,
                               [
                                   "感谢“{}”大哥的点赞[灵机一动]可以给可爱的主播完成一下心愿单吗拜托拜托[不失礼貌的微笑]".format(
                                       user)])

        if OptType.FOLLOW.value in opt_type:
            self.__check_max__(self.__user_opt_list[opt_key], OptType.FOLLOW.value, 1,
                               "感谢“{}”大哥的关注[赞]，顺便加一下粉丝团呗[送心]".format(user))

    def __user_msg__(self, msg_elements):
        try:
            # 获取用户输入的弹幕
            for message in msg_elements[-5:]:
                user = message.find_next('span', attrs={'class': 'rc30lnLh'})
                if not user:
                    return
                user_name = user.text.replace('：', '').strip()
                user_say = message.find_next('span', attrs={'class': 'b76LkBHq'}).text.strip()
                msg_key = "{}-{}".format(user_name, user_say)
                if not self.__user_opt_list.get(msg_key):
                    if "k爆你的狗头" in user_name or "小星的剪辑" in user_name or "喻喻" in user_name:
                        if "close" in user_say:
                            self.is_welcome = False
                            self.send("小的我先去歇会，有需要对我说打开的英文我就来了哦[害羞]")
                        elif "open" in user_say:
                            self.is_welcome = True
                            self.send("我回来了，继续加油，冲冲冲[奋斗]")
                        elif "clear" in user_say:
                            d_key = []
                            for key in list(self.__user_opt_list.keys()):
                                if "k爆你的狗头" in key:
                                    d_key.append(key)
                            for k in d_key:
                                if self.__user_opt_list.get(k):
                                    self.__user_opt_list.pop(k)
                    if "@k爆你的狗头" in user_say:
                        self.__call_me__(user_name, user_say)
                    self.__user_opt_list[msg_key] = True
        except Exception:
            pass

    def __call_me__(self, user, say):
        if "?" in say or "？" in say:
            self.send("{} @{}".format(Djt().get_djt(), user))
        else:
            self.send("艾特你爸爸干啥[看] @{}，可以对我发问号加数字触发技能".format(user))

    def __lock__(self):
        # 获取当前时间
        now = datetime.datetime.now()
        with open('D:/yshxin/IT/pro/py_demo/data/lock_msg.json', 'r') as fp:
            msg = json.load(fp)[random.randint(0, 6)]
        # 判断是否到了整点
        if now.minute == 0 and now.second < 5:
            self.send('现在{}点了，加油加油，{}[看]'.format(now.strftime('%H'), msg), 5)
        if now.minute == 30 and now.second < 5:
            self.send('现在{}了，加油加油，{}[看]'.format(now.strftime('%H:%M'), msg), 5)

    def check_is_on(self):
        while True:
            html_room = BeautifulSoup(self.driver.page_source, 'lxml')
            self.room_name = html_room.find('div', attrs={'class', '__leftContainer'}).find('div', attrs={'class',
                                                                                                          'st8eGKi4'}).text
            if html_room.find('div', attrs={'class', 'nGRbwTB3'}):
                Mail163().send('17693512081@163.com', '抖音机器人',
                               '主人“{}”当前没有开播，继续观察'.format(self.room_name))
                time.sleep(300)
                self.driver.refresh()
            else:
                break

    def loop_watch(self):

        while True:
            try:
                self.check_is_on()
                # 清理，如果弹幕过多，就删除醉经的一百条
                if len(self.__user_opt_list) > 300:
                    for k in list(self.__user_opt_list.keys())[:-100]:
                        self.__user_opt_list.pop(k)
                # 当前房间
                html_room = BeautifulSoup(self.driver.page_source, 'lxml')
                self.room_name = html_room.find('div', attrs={'class', '__leftContainer'}).find('div', attrs={'class',
                                                                                                              'st8eGKi4'}).text
                messages = html_room.find("div", attrs={'class': "webcast-chatroom___items"}).find_all('div',
                                                                                                       attrs={'class',
                                                                                                              'webcast-chatroom___enter-done'})
                user_opt = html_room.find('div', attrs={'class', 'webcast-chatroom___bottom-message'})

                # 用户弹幕操作
                self.__user_msg__(messages)

                # 用户进入房间操作
                if self.is_welcome:
                    self.__user_opt__(user_opt)

                # 报时
                self.__lock__()

                time.sleep(2)
            except Exception as e:
                pass

    def test(self, **keys):
        text = keys['keys']['text']
        self.send(text)
