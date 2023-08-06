import os
import socket
import sys
from urllib.request import Request, urlopen


def get_public_ip():
    """获取公网IP"""
    url = 'http://ipv4.icanhazip.com/'
    request = Request(url)
    response = urlopen(request)
    public_ip = response.read().decode('utf-8')
    return public_ip.rstrip()


def get_host_ip():
    """获取局域网IP"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def get_host_name():
    """获取主机名"""
    return socket.gethostname()


def get_app_path():
    """获取程序执行入口所在的目录"""
    if getattr(sys, 'frozen', False):
        app_path = os.path.dirname(os.path.abspath(sys.executable))
    elif sys.argv and sys.argv[0]:
        app_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    elif __file__:
        app_path = os.path.dirname(os.path.abspath(__file__))
    else:
        app_path = os.path.abspath('.')

    return app_path
