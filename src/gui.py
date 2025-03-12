"""
GUI模块，提供图形用户界面功能
"""
import tkinter as tk
import traceback
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import os

from .config import Config
from .ocr import process_file

class OCRGUI:
    """OCR图形界面类"""
    
    def __init__(self, root: tk.Tk):
        """
        初始化GUI
        
        Args:
            root: Tkinter根窗口
        """
        self.root = root
        self.root.title("Mistral OCR 处理工具")
        self.root.geometry("600x400")
        
        self.config = Config()
        
        self._init_ui()
        self._load_saved_config()
    
    def _init_ui(self) -> None:
        """初始化用户界面"""
        # 创建主框架
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # API Key 输入
        ttk.Label(self.main_frame, text="API Key:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.api_key_var = tk.StringVar()
        self.api_key_entry = ttk.Entry(self.main_frame, textvariable=self.api_key_var, width=50)
        self.api_key_entry.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # 文件选择
        ttk.Label(self.main_frame, text="选择文件:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.file_path_var = tk.StringVar()
        self.file_path_entry = ttk.Entry(self.main_frame, textvariable=self.file_path_var, width=40)
        self.file_path_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        ttk.Button(self.main_frame, text="浏览", command=self._select_file).grid(row=1, column=2, padx=5, pady=5)
        
        # 支持的文件类型提示
        ttk.Label(self.main_frame, text="支持的文件类型: PDF, JPG, JPEG, PNG", 
                 font=("", 8)).grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=(0,10))
        
        # 处理按钮
        self.process_button = ttk.Button(self.main_frame, text="开始处理", command=self._process_document)
        self.process_button.grid(row=3, column=0, columnspan=3, pady=20)
        
        # 状态显示
        self.status_var = tk.StringVar()
        ttk.Label(self.main_frame, textvariable=self.status_var).grid(row=4, column=0, columnspan=3, pady=5)
        
        # 结果显示区域
        self.result_text = tk.Text(self.main_frame, height=8, width=50)
        self.result_text.grid(row=5, column=0, columnspan=3, pady=5)
        self.result_text.insert('1.0', '处理结果将显示在这里...\n')
        self.result_text.config(state='disabled')
    
    def _load_saved_config(self) -> None:
        """加载保存的配置"""
        api_key = self.config.get('api_key', '')
        self.api_key_var.set(api_key)

    def _select_file(self) -> None:
        """选择要处理的文件"""
        try:
            # 明确指定每个文件类型的独立元组
            filetypes = [
                ("PDF Documents", "*.pdf"),
                ("JPEG Images", "*.jpg"),
                ("JPEG Images", "*.jpeg"),
                ("PNG Images", "*.png"),
                ("All Files", "*")
            ]

            # 添加防御性空值检查
            initialdir = os.path.expanduser("~/Documents") if Path("~/Documents").exists() else None

            filename = filedialog.askopenfilename(
                title="选择文件",
                filetypes=filetypes,
                defaultextension=".pdf",
                initialdir=initialdir
            )

            if filename:
                self.file_path_var.set(filename)

        except Exception as e:
            self.status_var.set("文件选择失败")
            error_msg = f"无法选择文件: {str(e)}"
            self._update_result_text(error_msg)
            messagebox.showerror("文件错误", error_msg)
            print(f"DEBUG - 文件对话框错误: {traceback.format_exc()}")

    def _update_result_text(self, text: str) -> None:
        """
        更新结果显示区域的文本
        
        Args:
            text: 要显示的文本
        """
        self.result_text.config(state='normal')
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert('1.0', text)
        self.result_text.config(state='disabled')
    
    def _process_document(self) -> None:
        """处理文档"""
        api_key = self.api_key_var.get().strip()
        file_path = self.file_path_var.get().strip()
        
        if not api_key:
            messagebox.showerror("错误", "请输入API Key")
            return
        
        if not file_path:
            messagebox.showerror("错误", "请选择要处理的文件")
            return
        
        try:
            self.status_var.set("正在处理中...")
            self.process_button.state(['disabled'])
            self._update_result_text("处理中，请稍候...")
            self.root.update()
            
            # 保存API Key
            self.config.set('api_key', api_key)
            
            # 处理文档
            output_dir = process_file(file_path, api_key)
            
            # 获取文件类型和名称
            file = Path(file_path)
            is_pdf = file.suffix.lower() == '.pdf'
            result_dir = 'results_pdf' if is_pdf else 'results_image'
            
            if is_pdf:
                result_file = os.path.join(result_dir, file.stem, f"{file.stem}.md")
            else:
                result_file = os.path.join(result_dir, f"{file.stem}.md")
            
            if os.path.exists(result_file):
                with open(result_file, 'r', encoding='utf-8') as f:
                    result_text = f"处理完成！\n\n结果保存在: {result_file}\n\n"
                    result_text += "文件内容预览:\n" + "-" * 40 + "\n"
                    result_text += f.read()[:500] + "..."  # 只显示前500个字符
                self._update_result_text(result_text)
            
            self.status_var.set("处理完成！")
            messagebox.showinfo("成功", f"文档处理完成！\n结果保存在: {result_file}")
        except Exception as e:
            self.status_var.set("处理失败")
            error_message = f"处理过程中出现错误：{str(e)}"
            self._update_result_text(error_message)
            messagebox.showerror("错误", error_message)
        finally:
            self.process_button.state(['!disabled'])

def main():
    """启动GUI应用"""
    root = tk.Tk()
    app = OCRGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 