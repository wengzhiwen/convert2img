import os
import sys
import argparse
import time
from pdf2image import convert_from_path
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

def save_images(images, output_folder, start_index, progress_bar):
    for i, image in enumerate(images):
        image.save(os.path.join(output_folder, f'{output_folder}_{start_index + i}.png'), 'PNG')
        progress_bar.update(1)

def convert_pdf_to_images(pdf_file, dpi):
    images = convert_from_path(pdf_file, dpi=dpi)
    return images

def process_images(images, output_folder):
    total_pages = len(images)
    print(f'Total {total_pages} pages to save')
    
    output_folder = os.path.splitext(os.path.basename(pdf_file))[0] + time.strftime('%Y%m%d%H%M%S')
    os.mkdir(output_folder)

    max_workers = max(1, os.cpu_count() - 1)
    print(f'Using {max_workers} threads for conversion')

    chunk_size = (total_pages + max_workers - 1) // max_workers
    chunks = [images[i:i + chunk_size] for i in range(0, total_pages, chunk_size)]

    futures = []
    progress_bars = [tqdm(total=len(chunk), desc=f'Thread {i+1}', position=i) for i, chunk in enumerate(chunks)]
    
    try:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for i, chunk in enumerate(chunks):
                futures.append(executor.submit(save_images, chunk, output_folder, i * chunk_size, progress_bars[i]))
            
            for future in as_completed(futures):
                future.result()
    finally:
        for progress_bar in progress_bars:
            progress_bar.close()

    print(f'Saved to folder: {output_folder}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert PDF to images.')
    parser.add_argument('pdf_file', help='The PDF file to convert.')
    parser.add_argument('--dpi', type=int, default=72, help='The DPI for the conversion (default: 72).')
    args = parser.parse_args()

    pdf_file = args.pdf_file
    dpi = args.dpi

    if not os.path.exists(pdf_file):
        print(f'File {pdf_file} not exists')
        print('Usage: python convert2img.py <pdf_file> [--dpi=DPI]')
        sys.exit(1)
    
    if not isinstance(dpi, int) or dpi < 10 or dpi > 1000:
        print(f'DPI {dpi} is not valid (10 <= DPI <= 1000)')
        sys.exit(1)
    
    print(f'Converting {pdf_file} to images with DPI {dpi}...')
    images = convert_pdf_to_images(pdf_file, dpi)
    
    process_images(images, pdf_file)

