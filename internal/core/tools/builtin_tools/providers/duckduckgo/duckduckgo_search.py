from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from internal.lib.helper import add_attribute


class DuckDuckGoInput(BaseModel):
    query: str = Field(description="搜索关键词")


@add_attribute("args_schema", DuckDuckGoInput)
def duckduckgo_search(**kwargs) -> BaseTool:
    """返回DuckDuckGo搜索工具"""
    return DuckDuckGoSearchRun(
        description="DuckDuckGo搜索工具",
        args_schema=DuckDuckGoInput,
    )
