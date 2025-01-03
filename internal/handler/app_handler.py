import os
import uuid
from dataclasses import dataclass
from operator import itemgetter

from injector import inject
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_openai import ChatOpenAI

from internal.schema.app_schema import CompletionRequestForm
from internal.service import AppService
from pkg.response import success_json, success_message

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
storage_path = os.path.join(BASE_DIR, "storage", "memory")
os.makedirs(storage_path, exist_ok=True)


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

    def debug(self, app_id: uuid.UUID):
        req = CompletionRequestForm()
        if not req.validate():
            return {"error": req.errors}

        prompt = ChatPromptTemplate.from_messages([
            ("system", "你是一个强大的聊天机器人，能根据用户的提问回复对应的问题"),
            MessagesPlaceholder("history"),
            ("human", "{query}")
        ])

        storage_path = "./storage/memory"
        os.makedirs(storage_path, exist_ok=True)

        memory = ConversationBufferWindowMemory(
            k=3,
            input_key="query",
            output_key="output",
            return_messages=True,
            chat_memory=FileChatMessageHistory(os.path.join(storage_path, "chat_history.txt"))
        )

        llm = ChatOpenAI(model_name="gpt-4o-mini")

        chain = RunnablePassthrough.assign(
            history=RunnableLambda(memory.load_memory_variables) | itemgetter(
                "history")) | prompt | llm | StrOutputParser()

        chain_input = {"query": req.query.data}
        content = chain.invoke(chain_input)

        memory.save_context(chain_input, {"output": content})

        return success_json({"content": content})
