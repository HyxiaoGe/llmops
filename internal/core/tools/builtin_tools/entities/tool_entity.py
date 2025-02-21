from pydantic import BaseModel


class ToolEntity(BaseModel):
    """工具实体，映射的数据是tools.yaml里的每条记录"""
    name: str
    label: str
    description: str
    params: list = []
