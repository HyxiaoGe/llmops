import os
import uuid
from dataclasses import dataclass
from operator import itemgetter
from typing import Dict, Any

from injector import inject
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.memory import BaseMemory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableConfig
from langchain_core.tracers import Run
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

    @classmethod
    def _load_memory_variables(cls, input: Dict[str, Any], config: RunnableConfig) -> Dict[str, Any]:
        configurable = config.get("configurable", {})
        configurable_memory = configurable.get("memory", None)
        if configurable_memory is not None and isinstance(configurable_memory, BaseMemory):
            return configurable_memory.load_memory_variables(input)
        return {"history": []}

    @classmethod
    def _save_context(cls, run: Run, config: RunnableConfig) -> None:
        configurable = config.get("configurable", {})
        configurable_memory = configurable.get("memory", None)
        if configurable_memory is not None and isinstance(configurable_memory, BaseMemory):
            configurable_memory.save_context(run.inputs, run.outputs)

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

        chain = (RunnablePassthrough.assign(
            history=RunnableLambda(memory.load_memory_variables) | itemgetter(
                "history")) | prompt | llm | StrOutputParser()).with_listeners(on_end=self._save_context)

        chain_input = {"query": req.query.data}
        content = chain.invoke(chain_input, config={"configurable": {"memory": memory}})

        return success_json({"content": content})
