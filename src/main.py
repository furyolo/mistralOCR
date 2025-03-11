"""
主程序入口文件
"""
import sys
import argparse
from pathlib import Path

from .ocr import process_file
from .gui import main as run_gui

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="Mistral OCR 文档识别工具")
    parser.add_argument("--gui", action="store_true", help="启动图形界面")
    parser.add_argument("--file", type=str, help="要处理的文件路径")
    parser.add_argument("--api-key", type=str, help="Mistral API密钥")
    return parser.parse_args()

def main():
    """主程序入口"""
    args = parse_args()
    
    if args.gui:
        run_gui()
    elif args.file and args.api_key:
        try:
            output_dir = process_file(args.file, args.api_key)
            print(f"处理完成！结果保存在: {output_dir}")
        except Exception as e:
            print(f"处理失败: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print("请提供文件路径和API密钥，或使用--gui参数启动图形界面", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 