import os
import uuid
from dataclasses import dataclass

from flask import request
from injector import inject
from openai import OpenAI

from internal.schema.app_schema import CompletionRequestForm
from internal.service import AppService
from pkg.response import success_json, success_message


@inject
@dataclass
class AppHandler:
    """应用控制器"""
    app_service: AppService

    def create_app(self):
        app = self.app_service.create_app()
        return success_message(f"应用已经成功创建，id为{app.id}")

    def get_app(self, id: uuid.UUID):
        app = self.app_service.get_app(id)
        return success_message(f"应用已经成功获取，名字是{app.name}")

    def update_app(self, id: uuid.UUID):
        app = self.app_service.update_app(id)
        return success_message(f"应用已经成功修改，修改的名字是:{app.name}")

    def delete_app(self, id: uuid.UUID):
        app = self.app_service.delete_app(id)
        return success_message(f"应用已经成功删除，id为:{app.id}")

    def ping(self):
        return {"ping": "pong"}

    def completion(self):
        req = CompletionRequestForm()
        if not req.validate():
            return {"error": req.errors}

        query = request.json.get("query")
        client = OpenAI(base_url=os.getenv("OPENAI_BASE_URL"))
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一个OpenAI开发的聊天机器人，请根据用户的输入回复对应的信息"},
                {"role": "user", "content": query}
            ]
        )
        content = completion.choices[0].message.content

        return success_json({"content": content})
