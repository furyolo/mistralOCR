"""
MistralOCR包初始化文件
"""
from .ocr import process_file
from .gui import main as run_gui
from .config import Config

__version__ = "0.1.0"
__all__ = ["process_file", "run_gui", "Config"] 