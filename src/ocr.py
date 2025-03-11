"""
OCR核心功能模块，提供文档识别相关功能
"""
from mistralai import Mistral
from pathlib import Path
import os
import base64
from mistralai import DocumentURLChunk, ImageURLChunk
from mistralai.models import OCRResponse
from typing import Union, Literal

def replace_images_in_markdown(markdown_str: str, images_dict: dict) -> str:
    """
    替换Markdown中的图片引用
    
    Args:
        markdown_str: Markdown文本
        images_dict: 图片映射字典
        
    Returns:
        替换后的Markdown文本
    """
    for img_name, img_path in images_dict.items():
        markdown_str = markdown_str.replace(f"![{img_name}]({img_name})", f"![{img_name}]({img_path})")
    return markdown_str

def save_ocr_results(ocr_response: OCRResponse, original_file: Path, file_type: Literal['pdf', 'image']) -> str:
    """
    保存OCR结果
    
    Args:
        ocr_response: OCR响应结果
        original_file: 原始文件路径
        file_type: 文件类型 ('pdf' 或 'image')
        
    Returns:
        输出目录路径
    """
    base_dir = 'results_pdf' if file_type == 'pdf' else 'results_image'
    os.makedirs(base_dir, exist_ok=True)
    
    original_name = original_file.stem
    
    if file_type == 'pdf':
        output_dir = os.path.join(base_dir, original_name)
        os.makedirs(output_dir, exist_ok=True)
        images_dir = os.path.join(output_dir, "images")
        os.makedirs(images_dir, exist_ok=True)
        
        all_markdowns = []
        for page in ocr_response.pages:
            page_images = {}
            for img in page.images:
                img_data = base64.b64decode(img.image_base64.split(',')[1])
                img_path = os.path.join(images_dir, f"{img.id}.png")
                with open(img_path, 'wb') as f:
                    f.write(img_data)
                page_images[img.id] = f"images/{img.id}.png"
            
            page_markdown = replace_images_in_markdown(page.markdown, page_images)
            all_markdowns.append(page_markdown)
        
        output_file = os.path.join(output_dir, f"{original_name}.md")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("\n\n".join(all_markdowns))
    
    else:
        output_file = os.path.join(base_dir, f"{original_name}.md")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(ocr_response.pages[0].markdown)
    
    return base_dir

def process_image(file_path: str, client: Mistral) -> OCRResponse:
    """
    处理图片文件
    
    Args:
        file_path: 图片文件路径
        client: Mistral客户端实例
        
    Returns:
        OCR处理结果
    """
    file = Path(file_path)
    
    uploaded_file = client.files.upload(
        file={
            "file_name": file.name,
            "content": file.read_bytes(),
        },
        purpose="ocr",
    )
    
    signed_url = client.files.get_signed_url(file_id=uploaded_file.id, expiry=1)
    
    response = client.ocr.process(
        document=ImageURLChunk(image_url=signed_url.url),
        model="mistral-ocr-latest",
        include_image_base64=True
    )
    
    return response

def process_pdf(file_path: str, client: Mistral) -> OCRResponse:
    """
    处理PDF文件
    
    Args:
        file_path: PDF文件路径
        client: Mistral客户端实例
        
    Returns:
        OCR处理结果
    """
    file = Path(file_path)
    
    uploaded_file = client.files.upload(
        file={
            "file_name": file.name,
            "content": file.read_bytes(),
        },
        purpose="ocr",
    )
    
    signed_url = client.files.get_signed_url(file_id=uploaded_file.id, expiry=1)
    
    response = client.ocr.process(
        document=DocumentURLChunk(document_url=signed_url.url),
        model="mistral-ocr-latest",
        include_image_base64=True
    )
    
    return response

def process_file(file_path: str, api_key: str) -> str:
    """
    处理PDF或图片文件
    
    Args:
        file_path: 文件路径
        api_key: Mistral API密钥
        
    Returns:
        输出目录路径
    """
    client = Mistral(api_key=api_key)
    
    file = Path(file_path)
    if not file.is_file():
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    file_extension = file.suffix.lower()
    supported_extensions = {'.pdf', '.jpg', '.jpeg', '.png'}
    
    if file_extension not in supported_extensions:
        raise ValueError(f"不支持的文件类型: {file_extension}。支持的类型: {', '.join(supported_extensions)}")
    
    if file_extension == '.pdf':
        response = process_pdf(file_path, client)
        output_dir = save_ocr_results(response, file, 'pdf')
    else:
        response = process_image(file_path, client)
        output_dir = save_ocr_results(response, file, 'image')
    
    return output_dir 