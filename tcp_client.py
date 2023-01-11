# coding=utf-8
import socket
import logging

# 日志 -> 时间 线程名 日志
DATE_FMT = "%H:%M:%S"
FORMAT = "[%(asctime)s]\t [%(threadName)s,%(thread)d] %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt=DATE_FMT)

# 服务器地址
ip = '127.0.0.1'
port = 1000

# 短信内容
phone = '17760470049'
message = 'test'
msg = '{0}:{1}:{2}'.format(phone, 0, message)
logging.info("The message is : [{0}]".format(msg))

# 创建客户端套接字
sms_client = socket.socket()
# 连接服务器
sms_client.connect((ip, port))
# 发送数据
sms_client.send(msg.encode('gkb'))
sms_client.close()

logging.info('Send ok')
