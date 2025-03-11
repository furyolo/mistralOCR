"""
配置管理模块，提供配置文件读写功能
"""
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

class Config:
    """配置管理类"""
    
    def __init__(self, config_file: str = "config.json"):
        """
        初始化配置管理器
        
        Args:
            config_file: 配置文件路径
        """
        self.config_file = config_file
        self.config: Dict[str, Any] = {}
        self.load()
    
    def load(self) -> None:
        """
        加载配置文件
        如果配置文件不存在，将创建一个空配置
        """
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            self.config = {}
    
    def save(self) -> None:
        """
        保存配置到文件
        """
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"保存配置文件失败: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置项
        
        Args:
            key: 配置项键名
            default: 默认值
            
        Returns:
            配置项值
        """
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        设置配置项
        
        Args:
            key: 配置项键名
            value: 配置项值
        """
        self.config[key] = value
        self.save()
    
    def delete(self, key: str) -> None:
        """
        删除配置项
        
        Args:
            key: 配置项键名
        """
        if key in self.config:
            del self.config[key]
            self.save()
    
    def clear(self) -> None:
        """清空所有配置"""
        self.config = {}
        self.save() 