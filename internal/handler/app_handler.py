import uuid
from dataclasses import dataclass

from injector import inject
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

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

        prompt = ChatPromptTemplate.from_template("{query}")

        llm = ChatOpenAI(model_name="gpt-4o-mini")

        ai_message = llm.invoke(prompt.invoke({"query": req.query.data}))

        parser = StrOutputParser()

        content = parser.invoke(ai_message)

        return success_json({"content": content})
