import json
import os.path
import time
import tkinter as tk
from tkinter import messagebox

from selenium import webdriver


class BaseRobot:
    __local_json = ''

    def __init__(self, name, en_name, url, cookies: bool = True, quick: bool = False):
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options)
        # self.driver = webdriver.Edge()
        self.driver.set_window_rect(0, 0, 1709, 1094)
        self.driver.get(url)
        if cookies:
            self.__local_json = "D:/yshxin/IT/pro/py_demo/data/cookies-{}.json".format(en_name)
            if os.path.exists(self.__local_json):
                with open(self.__local_json, 'r') as fp_json_r:
                    c_list = json.load(fp_json_r)
                    for v in c_list:
                        self.driver.add_cookie(v)
                self.driver.refresh()
            else:
                root = tk.Tk()
                root.withdraw()
                result = messagebox.showinfo("提示", "请通过扫码登录{}继续".format(name))
                with open(self.__local_json, 'a') as fp_json:
                    fp_json.write(json.dumps(self.driver.get_cookies()))
        if not quick:
            time.sleep(5)

    def test(self, **info):
        pass


if __name__ == '__main__':
    print("Robot")
