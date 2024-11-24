# convert2img

是一个被重新发明的轮子，用于将PDF文档转换为图像。我为了将PDF拆成图片用来微调模型而写了这个脚本。

他利用[pdf2image库](https://github.com/Belval/pdf2image)，简单来说就是给库套了一个可以直接在CLI中运行的壳。

特别是给pdf2image套了一个简单的多线程处理，使得处理多页PDF文件时的性能有所提升。

## 使用说明

1. 安装依赖：
    ```bash
    pip install -r requirements.txt
    ```

2. 运行转换命令：
    ```bash
    python convert2img.py <pdf_file> [--dpi=DPI]
    ```

生成的图片文件（每页一个PNG）会被保存到一个自动生成的文件夹中，偷懒偷到烂

# English

A tool for converting PDF documents to images. I wrote this script to split PDFs into images for fine-tuning models.

Using [pdf2image library](https://github.com/Belval/pdf2image), it provides a CLI wrapper for the pdf2image library.

Simple multi-thread, improving performance for large PDF files.

## Quick Start

1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Run the conversion command:
    ```bash
    python convert2img.py <pdf_file> [--dpi=DPI]
    ```

Image files (one PNG per page) will be saved in an automatically generated folder.