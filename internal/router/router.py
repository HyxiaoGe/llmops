from flask import Flask, Blueprint

from internal.handler import app_handler


class Router:
    """路由"""

    def register_router(self, app: Flask):
        """注册路由"""
        # 1. 创建一个蓝图
        bp = Blueprint('llmops', __name__, url_prefix='')

        # 2. 将url与对应的控制器方法做绑定
        bp.add_url_rule("/ping", view_func=app_handler.ping())
