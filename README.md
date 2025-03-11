# Mistral OCR 文档识别工具

基于 Mistral API 的文档识别工具，支持处理 PDF 和图片文件。

## 功能特点

- 支持处理 PDF 文件和图片文件（JPG、JPEG、PNG）
- 提供图形用户界面和命令行界面
- 自动保存处理结果为 Markdown 格式
- 支持配置文件管理
- 支持批量处理文件

## 安装

1. 克隆项目代码：

```bash
git clone https://github.com/yourusername/mistralOCR.git
cd mistralOCR
```

2. 安装依赖：

```bash
pip install -r requirements.txt
```

## 使用方法

### 图形界面

运行以下命令启动图形界面：

```bash
python -m src.main --gui
```

### 命令行界面

使用命令行处理文件：

```bash
python -m src.main --file <文件路径> --api-key <API密钥>
```

## 项目结构

```
mistralOCR/
├── src/                # 源代码目录
│   ├── __init__.py    # 包初始化文件
│   ├── main.py        # 主程序入口
│   ├── ocr.py         # OCR核心功能
│   ├── gui.py         # 图形界面
│   └── config.py      # 配置管理
├── tests/             # 测试目录
├── docs/              # 文档目录
├── results_pdf/       # PDF处理结果
├── results_image/     # 图片处理结果
├── README.md          # 项目说明
├── requirements.txt   # 依赖列表
└── config.json        # 配置文件
```

## 配置文件

配置文件 `config.json` 用于存储常用设置：

```json
{
    "api_key": "your-api-key"
}
```

## 开发说明

### 环境要求

- Python 3.7+
- 依赖包见 requirements.txt

### 开发设置

1. 创建虚拟环境：

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. 安装开发依赖：

```bash
pip install -r requirements-dev.txt
```

### 运行测试

```bash
python -m pytest tests/
```

## 许可证

MIT License

## 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 问题反馈

如果您在使用过程中遇到任何问题，请在 GitHub Issues 页面提交问题。 