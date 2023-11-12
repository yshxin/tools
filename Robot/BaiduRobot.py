import logging

from Robot import BaseRobot


class BaiduWXYY(BaseRobot):
    def __init__(self):
        super().__init__("实例化文新一言实例完成", 'wxyy', 'https://yiyan.baidu.com/')
        logging.info('实例化文新一言实例完成')

    def send_mag(self, text) -> str:
        logging.info(text)
        return ''
