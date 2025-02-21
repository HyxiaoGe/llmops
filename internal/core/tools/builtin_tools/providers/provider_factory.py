import os.path
from typing import Any

import yaml
from injector import singleton, inject

from internal.core.tools.builtin_tools.entities import ProviderEntity, Provider


@singleton
@inject
class ProviderFactory:
    """服务提供商工厂类"""
    provider_map: dict[str, Provider] = {}

    def __init__(self):
        """构造函数，初始化对应的provider_tool_map"""
        self._get_provider_tool_map()

    def get_provider(self, provider_name: str) -> Provider:
        """根据传递的名字来获取服务提供商"""
        return self.provider_map.get(provider_name)

    def get_providers(self) -> list[Provider]:
        """获取所有的服务提供商列表"""
        return list(self.provider_map.values())

    def get_provider_entities(self) -> list[ProviderEntity]:
        """获取所有服务提供商实体列表信息"""
        return [provider.provider_entity for provider in self.provider_map.values()]

    def get_tool(self, provider_name: str, tool_name: str) -> Any:
        """根据服务提供商的名字+工具名字，来获取特定的工具实体"""
        provider = self.get_provider(provider_name)
        if provider is None:
            return None
        return provider.get_tool(tool_name)

    def _get_provider_tool_map(self):
        """项目初始化的时候获取服务提供商、工具的映射关系并填充到provider_tool_map"""
        # 如果provider_map已经初始化，则直接返回
        if self.provider_map:
            return

        # 获取当前文件/类所在的文件夹路径
        current_path = os.path.abspath(__file__)
        providers_path = os.path.dirname(current_path)
        providers_yaml_path = os.path.join(providers_path, "providers.yaml")

        # 读取providers.yaml文件的内容
        with open(providers_yaml_path, encoding="utf-8") as f:
            provider_yaml_data = yaml.safe_load(f)

        # 循环遍历providers.yaml文件中的内容
        for idx, provider_data in enumerate(provider_yaml_data):
            provider_entity = ProviderEntity(**provider_data)
            self.provider_map[provider_entity.name] = Provider(
                name=provider_entity.name,
                position=idx + 1,
                provider_entity=provider_entity
            )
